"""
Neural Decompiler — entry point for the runnable implementation.

The previous monolithic file (design sketch with markdown fences and partial stubs) is preserved
under `archive/Neural_Decompiler_design_sketch.py.txt` for reference.

This module re-exports the implemented package. Train from the project directory, for example:

    python -m neural_decompiler.train --epochs 3 --device cpu

Or import programmatically:

    from neural_decompiler import NeuralDecompilerModel, EnhancedDecompilerConfig, train_main
"""

from neural_decompiler import (
    EnhancedDecompilerConfig,
    NeuralDecompilerModel,
    SyntheticDecompilerDataset,
    build_vocab,
    collate_fn,
)
from neural_decompiler.infer import infer_main
from neural_decompiler.train import train_main

__all__ = [
    "EnhancedDecompilerConfig",
    "NeuralDecompilerModel",
    "SyntheticDecompilerDataset",
    "build_vocab",
    "collate_fn",
    "train_main",
    "infer_main",
]

if __name__ == "__main__":
    import sys

    train_main(sys.argv[1:])
