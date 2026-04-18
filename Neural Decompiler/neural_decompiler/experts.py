"""Mixture-of-experts layers with binary / language families (design sketch)."""

from __future__ import annotations

from typing import Any, Dict, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .config import EnhancedDecompilerConfig


class FeedForwardExpert(nn.Module):
    """Single MLP expert (architecture-specific experts collapse here for training)."""

    def __init__(self, config: EnhancedDecompilerConfig):
        super().__init__()
        h = config.hidden_size
        self.net = nn.Sequential(
            nn.Linear(h, config.intermediate_size),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.intermediate_size, h),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class FamilyMoELayer(nn.Module):
    """
    Top-k sparse MoE: first half of experts = "binary", second half = "language".
    Load-balancing auxiliary loss matches Switch Transformer style.
    """

    def __init__(self, config: EnhancedDecompilerConfig):
        super().__init__()
        self.config = config
        self.num_experts = config.num_binary_experts + config.num_language_experts

        self.router = nn.Linear(config.hidden_size, self.num_experts)
        self.experts = nn.ModuleList([FeedForwardExpert(config) for _ in range(self.num_experts)])

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, Any]]:
        b, s, h = x.shape
        flat = x.reshape(-1, h)
        logits = self.router(flat)
        probs = F.softmax(logits, dim=-1)

        # Dense mixture (num_experts is modest); top-k selection kept in config for future sparse kernels
        expert_stack = torch.stack([expert(flat) for expert in self.experts], dim=1)
        out_flat = torch.einsum("ne,neh->nh", probs, expert_stack)
        out = out_flat.view(b, s, h)

        importance = probs.mean(dim=0)
        target = torch.full_like(importance, 1.0 / self.num_experts)
        aux = F.mse_loss(importance, target)

        family_binary = importance[: self.config.num_binary_experts].sum()
        family_lang = importance[self.config.num_binary_experts :].sum()

        return out, {
            "aux_loss": aux,
            "routing_logits": logits.view(b, s, -1),
            "family_binary_mass": family_binary,
            "family_language_mass": family_lang,
        }
