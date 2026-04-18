"""Compressed slot memory and hierarchical memory transformer (core from design sketch)."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import EnhancedDecompilerConfig


class AdvancedMemoryManager(nn.Module):
    """Attention over learnable memory slots + gated fusion (robust, batched)."""

    def __init__(self, config: EnhancedDecompilerConfig):
        super().__init__()
        self.config = config
        h = config.hidden_size
        self.memory_slots = nn.Parameter(torch.randn(config.compressed_memory_size, h) * 0.02)

        self.compressor = nn.Sequential(
            nn.Linear(h, h),
            nn.LayerNorm(h),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(h, h),
            nn.LayerNorm(h),
        )

        self.context_aggregator = nn.MultiheadAttention(
            embed_dim=h,
            num_heads=max(1, config.num_heads // 2),
            dropout=config.dropout,
            batch_first=True,
        )

        self.update_gate = nn.Sequential(
            nn.Linear(h * 2, h),
            nn.LayerNorm(h),
            nn.Sigmoid(),
        )

        self.compression_gate = nn.Sequential(nn.Linear(h, 1), nn.Sigmoid())
        self.update_rate = nn.Sequential(nn.Linear(h, 1), nn.Sigmoid())

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        context_window: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        b, s, h = hidden_states.shape
        kv = context_window if context_window is not None else self.memory_slots.unsqueeze(0).expand(b, -1, -1)
        compressed = self.compressor(hidden_states)

        # Padding mask applies to KV only when KV is sequence-shaped (context_window); memory slots use no mask.
        key_padding = None
        if context_window is not None and attention_mask is not None:
            key_padding = attention_mask == 0

        ctx, attn_w = self.context_aggregator(
            query=compressed,
            key=kv,
            value=kv,
            key_padding_mask=key_padding,
            need_weights=True,
        )

        gate = self.update_gate(torch.cat([compressed, ctx], dim=-1))
        fused = gate * compressed + (1.0 - gate) * ctx

        comp_score = self.compression_gate(fused)
        ur = self.update_rate(fused)
        mixed = ur * fused + (1.0 - ur) * hidden_states

        return mixed * comp_score + hidden_states * (1.0 - comp_score), {
            "compression_scores": comp_score,
            "update_rate": ur,
            "attention_weights": attn_w,
        }

    def get_memory_stats(self) -> Dict[str, torch.Tensor]:
        n = torch.norm(self.memory_slots, dim=-1)
        return {
            "mean_norm": n.mean(),
            "max_norm": n.max(),
            "min_norm": n.min(),
            "std_norm": n.std(),
        }


class HierarchicalMemoryTransformer(nn.Module):
    """Stacks memory-augmented transformer levels and fuses them."""

    def __init__(self, config: EnhancedDecompilerConfig):
        super().__init__()
        self.config = config
        h = config.hidden_size
        self.memory_managers = nn.ModuleList([AdvancedMemoryManager(config) for _ in range(config.hierarchical_levels)])

        self.level_transformers = nn.ModuleList(
            [
                nn.TransformerEncoderLayer(
                    d_model=h,
                    nhead=config.num_heads,
                    dim_feedforward=config.intermediate_size,
                    dropout=config.dropout,
                    batch_first=True,
                    activation="gelu",
                    norm_first=True,
                )
                for _ in range(config.hierarchical_levels)
            ]
        )

        self.cross_attention = nn.ModuleList(
            [
                nn.MultiheadAttention(
                    embed_dim=h,
                    num_heads=config.num_heads,
                    dropout=config.dropout,
                    batch_first=True,
                )
                for _ in range(max(0, config.hierarchical_levels - 1))
            ]
        )

        self.fusion_layer = nn.Sequential(
            nn.Linear(h * config.hierarchical_levels, h),
            nn.LayerNorm(h),
            nn.GELU(),
        )

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        level_outputs = []
        memory_stats = []
        current = hidden_states

        pad = None
        if attention_mask is not None:
            pad = attention_mask == 0

        for level in range(self.config.hierarchical_levels):
            mem_out, stats = self.memory_managers[level](current, attention_mask=attention_mask)
            memory_stats.append(stats)
            transformed = self.level_transformers[level](mem_out, src_key_padding_mask=pad)
            level_outputs.append(transformed)

            if level < len(self.cross_attention):
                cross_out, _ = self.cross_attention[level](
                    query=transformed,
                    key=mem_out,
                    value=mem_out,
                    key_padding_mask=pad,
                )
                current = F.layer_norm(cross_out + transformed, (self.config.hidden_size,))

        combined = torch.cat(level_outputs, dim=-1)
        final_output = self.fusion_layer(combined)
        return final_output, {"level_outputs": level_outputs, "memory_stats": memory_stats}
