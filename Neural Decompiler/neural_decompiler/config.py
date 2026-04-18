"""Configuration for the neural decompiler (aligned with the original design sketch)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EnhancedDecompilerConfig:
    # Model geometry
    hidden_size: int = 256
    intermediate_size: int = 1024
    num_encoder_layers: int = 4
    num_decoder_layers: int = 4
    num_heads: int = 8
    dropout: float = 0.1

    # Memory
    num_memory_slots: int = 64
    compressed_memory_size: int = 64
    hierarchical_levels: int = 2

    # Mixture-of-experts (binary vs language families)
    num_binary_experts: int = 8
    num_language_experts: int = 8
    num_experts_per_token: int = 2
    expert_capacity_factor: float = 1.0
    moe_aux_loss_weight: float = 0.01

    # Vocabulary / sequence
    max_sequence_length: int = 512
    max_src_len: int = 256
    max_tgt_len: int = 256

    # Training
    batch_size: int = 16
    learning_rate: float = 3e-4
    weight_decay: float = 0.01
    num_epochs: int = 5
    label_smoothing: float = 0.1
    warmup_steps: int = 100

    # Multi-task weights (reserved for future losses)
    task_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "decompilation": 1.0,
            "bug_detection": 0.0,
            "vulnerability_analysis": 0.0,
            "type_inference": 0.0,
            "control_flow": 0.0,
        }
    )

    # Device / precision
    mixed_precision: bool = False
    gradient_clip: float = 1.0

    @property
    def total_experts(self) -> int:
        return self.num_binary_experts + self.num_language_experts

    def expert_counts(self) -> List[int]:
        return [self.num_binary_experts, self.num_language_experts]
