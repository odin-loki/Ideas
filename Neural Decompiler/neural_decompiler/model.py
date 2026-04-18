"""Encoder–decoder transformer with hierarchical memory and MoE (neural decompiler core)."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import torch
import torch.nn as nn

from .config import EnhancedDecompilerConfig
from .experts import FamilyMoELayer
from .memory import HierarchicalMemoryTransformer


class NeuralDecompilerModel(nn.Module):
    """
    Maps a sequence of source (assembly-like) token ids to target (high-level language) token ids.
    Encoder uses a hierarchical memory tower; a family MoE refines representations; decoder is causal.
    """

    def __init__(
        self,
        config: EnhancedDecompilerConfig,
        src_vocab_size: int,
        tgt_vocab_size: int,
        pad_id: int = 0,
    ):
        super().__init__()
        self.config = config
        self.pad_id = pad_id
        h = config.hidden_size

        self.src_tok = nn.Embedding(src_vocab_size, h)
        self.tgt_tok = nn.Embedding(tgt_vocab_size, h)
        self.src_pos = nn.Embedding(config.max_sequence_length, h)
        self.tgt_pos = nn.Embedding(config.max_sequence_length, h)

        self.hier_memory = HierarchicalMemoryTransformer(config)
        enc_layer = nn.TransformerEncoderLayer(
            d_model=h,
            nhead=config.num_heads,
            dim_feedforward=config.intermediate_size,
            dropout=config.dropout,
            batch_first=True,
            activation="gelu",
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=config.num_encoder_layers)

        self.moe = FamilyMoELayer(config)
        self.post_moe = nn.LayerNorm(h)

        dec_layer = nn.TransformerDecoderLayer(
            d_model=h,
            nhead=config.num_heads,
            dim_feedforward=config.intermediate_size,
            dropout=config.dropout,
            batch_first=True,
            activation="gelu",
            norm_first=True,
        )
        self.decoder = nn.TransformerDecoder(dec_layer, num_layers=config.num_decoder_layers)

        self.out_proj = nn.Linear(h, tgt_vocab_size)

    def _src_key_padding(self, src: torch.Tensor) -> Optional[torch.Tensor]:
        return src == self.pad_id

    def _tgt_key_padding(self, tgt: torch.Tensor) -> Optional[torch.Tensor]:
        return tgt == self.pad_id

    def encode(self, src: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, Any]]:
        b, s = src.shape
        device = src.device
        pos = torch.arange(s, device=device).clamp(max=self.config.max_sequence_length - 1)
        x = self.src_tok(src) + self.src_pos(pos).unsqueeze(0)

        x, mem_info = self.hier_memory(x, attention_mask=(src != self.pad_id).long())
        pad = self._src_key_padding(src)
        x = self.encoder(x, src_key_padding_mask=pad)

        moe_out, moe_info = self.moe(x)
        x = self.post_moe(x + moe_out)

        return x, {"memory": mem_info, "moe": moe_info}

    def decode(
        self,
        tgt: torch.Tensor,
        memory: torch.Tensor,
        src_padding: Optional[torch.Tensor],
    ) -> Tuple[torch.Tensor, Dict[str, Any]]:
        b, t = tgt.shape
        device = tgt.device
        pos = torch.arange(t, device=device).clamp(max=self.config.max_sequence_length - 1)
        y = self.tgt_tok(tgt) + self.tgt_pos(pos).unsqueeze(0)

        causal = nn.Transformer.generate_square_subsequent_mask(t, device=device)
        tgt_pad = self._tgt_key_padding(tgt)

        logits = self.decoder(
            y,
            memory,
            tgt_mask=causal,
            tgt_key_padding_mask=tgt_pad,
            memory_key_padding_mask=src_padding,
        )
        return self.out_proj(logits), {}

    def forward(
        self,
        src: torch.Tensor,
        tgt: torch.Tensor,
    ) -> Tuple[torch.Tensor, Dict[str, Any]]:
        """tgt includes <sos> ... <eos>; decoder consumes tgt[:, :-1], logits align with tgt[:, 1:]."""
        mem, enc_info = self.encode(src)
        src_pad = self._src_key_padding(src)
        logits, dec_info = self.decode(tgt[:, :-1], mem, src_pad)
        aux = enc_info.get("moe", {}).get("aux_loss", torch.tensor(0.0, device=src.device))
        return logits, {"aux_loss": aux, "encode": enc_info, "decode": dec_info}

    @torch.no_grad()
    def greedy_decode(
        self,
        src: torch.Tensor,
        max_len: int,
        bos_id: int,
        eos_id: int,
    ) -> torch.Tensor:
        self.eval()
        mem, _ = self.encode(src)
        src_pad = self._src_key_padding(src)
        out = torch.full((src.size(0), 1), bos_id, dtype=torch.long, device=src.device)

        for _ in range(max_len - 1):
            logits, _ = self.decode(out, mem, src_pad)
            next_tok = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            out = torch.cat([out, next_tok], dim=1)
            if (next_tok == eos_id).all():
                break

        return out
