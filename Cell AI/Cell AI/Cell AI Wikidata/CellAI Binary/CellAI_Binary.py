#!/usr/bin/env python3
"""
CellAI_Binary - Binary Stream Cellular Model with Enhanced Encoder

This implementation provides the complete mathematical CellAI model working directly on binary streams,
with an enhanced Binary Encoder for more comprehensive feature extraction:

1. Core Mathematical Framework:
   - Cellular Equation: dS/dt = f(I, S, t) - γS + D∇²S + η(t)
   - Probabilistic State Transitions: P(Si→Sj) = exp(-ΔEij/kT) / Z
   - Temporal Memory Integration: M(t) = ∫[t-τ, t] w(t-s)I(s)ds + ∫[0, t] K(t-s)S(s)ds
   - Detailed Boundary Conditions: B(Sᵢ, Sⱼ) = 0 for adjacent partitions
   - Emergent Properties Framework for collective behavior

2. Enhanced Binary Encoder:
   - Content-defined chunking for adaptive processing
   - Multi-scale analysis with wavelet transformations
   - N-gram analysis for sequential patterns
   - Dynamic Adaptive Multi-scale Reservoir (DAMR)
   - Adaptive dictionary encoding for pattern recognition
   - Spectral analysis using FFT
   - Lightweight Feature-Selective mechanism

Usage:
  - Process: python CellAI_Binary.py process --input /path/to/file --output /path/to/output
  - Train: python CellAI_Binary.py train --data /path/to/data_folder --epochs 3
  - Benchmark: python CellAI_Binary.py benchmark --model /path/to/model.pt --test /path/to/test_folder
  - Chat: python CellAI_Binary.py chat --model /path/to/model.pt
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import ray
from dataclasses import dataclass, field
import logging
import sys
from typing import Dict, List, Tuple, Optional, Any, Union, Callable, BinaryIO
import time
import json
import os
import multiprocessing
import mmap
from tqdm import tqdm
import math
import random
import argparse
from collections import deque, Counter, defaultdict
import io
import struct
import hashlib
import pywt
import xxhash
import mmh3
from scipy.fftpack import fft
from scipy.stats import entropy, skew, kurtosis, rankdata
import zlib
from sklearn.random_projection import GaussianRandomProjection
from sklearn.decomposition import TruncatedSVD
import concurrent.futures
import glob

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Disable Ray's native logging
os.environ["RAY_DISABLE_DOCKER_CPU_WARNING"] = "1"
os.environ["RAY_DEDUP_LOGS"] = "0"
os.environ["RAY_DISABLE_CRASH_REPORTS"] = "1"

@dataclass
class ModelParams:
    """Raw cellular model parameters for binary stream processing"""
    # Core cellular parameters
    dt: float             # Time step for memory dynamics
    D: float              # Diffusion coefficient for state propagation
    gamma: float          # Decay rate for memory
    eta: float            # Noise amplitude (for η(t))
    num_partitions: int   # Number of parallel partitions
    state_size: int       # Size of state vector per partition
    
    # State transition parameters
    temperature: float        # Temperature for Boltzmann distribution (kT)
    energy_scale: float       # Scale factor for energy calculations
    
    # Temporal memory parameters
    memory_tau: float        # Memory time constant
    kernel_terms: int        # Number of terms in memory kernel expansion
    kernel_decays: List[float]  # Decay rates for memory kernel terms
    
    # Boundary condition parameters
    boundary_strength: float  # Coupling strength at boundaries
    
    # Emergent properties parameters
    collective_threshold: float  # Threshold for collective behavior emergence
    
    # Binary processing parameters
    chunk_size: int          # Size of binary chunks to process
    overlap: int             # Overlap between chunks
    cell_hidden_size: int    # Hidden size for cell gates
    
    # Training parameters
    learning_rate: float     # Learning rate for training
    batch_size: int          # Batch size for training
    accumulation_steps: int  # Steps for gradient accumulation
    early_stopping_patience: int  # Patience for early stopping
    
    # Encoding parameters
    input_dim: int = 4       # Dimension for encoding binary input (bits per chunk)
    one_hot_dim: int = 16    # Dimension for one-hot encoding (2^input_dim)
    
    # Enhanced binary encoder parameters
    encoder_params: Optional['EncoderParams'] = None


@dataclass
class EncoderParams:
    """Parameters for the Enhanced Cellular Binary Encoder"""
    # Content-defined chunking parameters
    min_chunk_size: int = 512        # Minimum bytes per chunk
    max_chunk_size: int = 8192       # Maximum bytes per chunk
    window_size: int = 16            # Rolling hash window
    boundary_mask: int = 0x0FFF      # Boundary condition (when hash & mask == 0)
    
    # Multi-scale analysis parameters
    scales: List[float] = field(default_factory=lambda: [1.0, 0.5, 0.25, 0.125])
    
    # Wavelet transform parameters
    wavelet: str = 'db4'             # Daubechies-4 wavelet
    wavelet_levels: int = 4          # Decomposition levels
    
    # Cellular memory dynamics parameters
    dt: float = 0.1                  # Time step for memory dynamics
    D: float = 0.2                   # Diffusion coefficient
    gamma: float = 0.1               # Decay rate
    eta: float = 0.01                # Noise amplitude
    
    # Feature selection parameters
    selection_threshold: float = 0.3 # Keep top 30% of features
    
    # N-gram parameters
    ngram_sizes: List[int] = field(default_factory=lambda: [2, 3, 4])
    top_ngrams: int = 50             # Number of top n-grams to keep per size
    
    # DAMR (Dynamic Adaptive Multi-scale Reservoir) parameters
    reservoir_size: int = 256        # Size of each reservoir
    num_reservoirs: int = 3          # Number of reservoirs at different scales
    influence_radius: List[int] = field(default_factory=lambda: [2, 4, 8])
    influence_strength: List[float] = field(default_factory=lambda: [0.1, 0.08, 0.06])
    
    # Adaptive dictionary parameters
    dict_max_size: int = 4096        # Maximum dictionary size
    dict_min_freq: int = 2           # Minimum frequency for dictionary entries
    
    # LSH parameters for fast similarity search
    lsh_num_hashes: int = 10         # Number of hash functions
    lsh_bands: int = 5               # Number of bands for LSH
    
    # Dimensionality reduction parameters
    pca_components: int = 64         # Number of SVD components
    random_proj_components: int = 128  # Number of random projection components


class CellularBinaryEncoder:
    """
    Enhanced Cellular Binary Encoder (ECBE)
    
    A comprehensive feature extractor combining cellular memory dynamics, multi-scale analysis,
    dictionary encoding, wavelet transforms, and spectral analysis for any binary data.
    Designed to work with CellAI architecture and other AI systems.
    """
    
    def __init__(self, params: Optional[EncoderParams] = None):
        """Initialize the encoder with optimized parameters"""
        # Use provided parameters or create default ones
        self.params = params or EncoderParams()
        
        # Initialize caches and helper data structures
        self.feature_cache = {}
        self.dictionary = {}
        
    def encode(self, binary_data, max_features=2000):
        """
        Encode binary data into a feature vector
        
        Args:
            binary_data: Bytes or binary file to encode
            max_features: Maximum number of features to return
            
        Returns:
            feature_vector: Numpy array of extracted features
        """
        # Handle file objects vs byte sequences
        if hasattr(binary_data, 'read'):
            binary_data = binary_data.read()
        
        # Determine chunks using content-defined chunking
        chunks = self._content_defined_chunking(binary_data)
        
        # Extract dictionary patterns for the entire data
        self._build_adaptive_dictionary(chunks)
        
        # Extract features from each chunk in parallel
        feature_sets = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            feature_sets = list(executor.map(self._process_chunk, chunks))
        
        # Combine features from all chunks
        combined_features = self._combine_chunk_features(feature_sets)
        
        # Add global features based on the entire data
        global_features = self._extract_global_features(binary_data, chunks)
        combined_features.update(global_features)
        
        # Apply dimensionality reduction if we have a lot of features
        if len(combined_features) > max_features * 3:
            combined_features = self._reduce_dimensionality(combined_features)
        
        # Select top features based on importance
        selected_features = self._select_top_features(combined_features, max_features)
        
        # Ensure we always return a non-empty feature vector
        if len(selected_features) == 0:
            # Fallback to basic statistical features of the entire data
            selected_features = self._extract_basic_stats(binary_data)
        
        # Convert to numpy array and normalize for numerical stability
        feature_array = np.array(selected_features, dtype=np.float32)
        
        # Apply numerical stability fixes
        # 1. Replace any NaN or Inf values
        feature_array = np.nan_to_num(feature_array, nan=0.0, posinf=1.0, neginf=-1.0)
        
        # 2. Normalize the features (mean=0, std=1) for better training stability
        if len(feature_array) > 1:
            feature_mean = np.mean(feature_array)
            feature_std = np.std(feature_array)
            if feature_std > 0:  # Avoid division by zero
                feature_array = (feature_array - feature_mean) / (feature_std + 1e-8)
            
            # 3. Clip to reasonable range to prevent extreme values
            feature_array = np.clip(feature_array, -10.0, 10.0)
        
        return feature_array
    
    def _content_defined_chunking(self, data):
        """
        Divide data into chunks based on content boundaries rather than fixed sizes
        Uses rolling hash to find natural boundaries in the data
        """
        chunks = []
        data_len = len(data)
        
        # Return whole data if smaller than minimum chunk size
        if data_len <= self.params.min_chunk_size:
            return [data]
        
        i = 0
        while i < data_len:
            # Ensure minimum chunk size
            if i + self.params.min_chunk_size >= data_len:
                chunks.append(data[i:])
                break
            
            # Find content-defined boundary
            boundary = self._find_boundary(data, i + self.params.min_chunk_size, 
                                         min(i + self.params.max_chunk_size, data_len))
            
            # If no boundary found, use maximum chunk size
            if boundary == -1:
                boundary = min(i + self.params.max_chunk_size, data_len)
            
            chunks.append(data[i:boundary])
            i = boundary
        
        return chunks
    
    def _find_boundary(self, data, start, end):
        """
        Find content-defined boundary using rolling hash
        Returns position of the boundary or -1 if no boundary found
        """
        if end <= start:
            return end
        
        for i in range(start, end - self.params.window_size + 1):
            # Create a fresh hash for each window to avoid reset issues
            h = xxhash.xxh64()
            window = data[i:i+self.params.window_size]
            h.update(window)
            if (h.intdigest() & self.params.boundary_mask) == 0:
                return i + self.params.window_size
        
        return -1
    
    def _build_adaptive_dictionary(self, chunks):
        """
        Build an adaptive dictionary of common patterns from all chunks
        Inspired by LZ77/LZ78 compression techniques
        """
        self.dictionary = {}
        pattern_counts = Counter()
        
        # First pass: count all patterns
        for chunk in chunks:
            # Convert to array for faster processing
            data = np.frombuffer(chunk, dtype=np.uint8)
            
            # Count patterns of different lengths
            for pattern_len in range(3, 17):  # Patterns from 3 to 16 bytes
                if len(data) < pattern_len:
                    continue
                
                for i in range(len(data) - pattern_len + 1):
                    pattern = bytes(data[i:i+pattern_len])
                    pattern_counts[pattern] += 1
        
        # Second pass: keep only frequent patterns
        for pattern, count in pattern_counts.items():
            if count >= self.params.dict_min_freq:
                # Only keep patterns that appear multiple times
                pattern_hash = xxhash.xxh64(pattern).intdigest()
                self.dictionary[pattern_hash] = (pattern, count)
                
                # Limit dictionary size
                if len(self.dictionary) >= self.params.dict_max_size:
                    break
    
    def _process_chunk(self, chunk):
        """
        Process a single chunk to extract features using multiple techniques
        """
        features = {}
        
        # Convert to numpy array of bytes for faster processing
        data = np.frombuffer(chunk, dtype=np.uint8)
        
        # 1. Multi-scale analysis
        for scale_idx, scale in enumerate(self.params.scales):
            # Scale the data (take a proportion of it)
            scale_size = max(1, int(len(data) * scale))
            scaled_data = data[:scale_size]
            
            # 2. Wavelet decomposition at this scale
            wavelet_features = self._extract_wavelet_features(scaled_data)
            
            # Add scale prefix to feature names
            scale_prefix = f"scale_{scale_idx}_"
            features.update({scale_prefix + k: v for k, v in wavelet_features.items()})
            
            # 3. Statistical features at this scale
            stat_features = self._extract_statistical_features(scaled_data)
            features.update({scale_prefix + k: v for k, v in stat_features.items()})
            
            # 4. N-gram features at this scale
            if len(scaled_data) >= max(self.params.ngram_sizes):
                ngram_features = self._extract_ngram_features(scaled_data)
                features.update({scale_prefix + k: v for k, v in ngram_features.items()})
        
        # 5. Cellular dynamics-based features
        cell_features = self._extract_cellular_features(data)
        features.update(cell_features)
        
        # 6. DAMR (Dynamic Adaptive Multi-scale Reservoir) features
        reservoir_features = self._extract_reservoir_features(data)
        features.update(reservoir_features)
        
        # 7. Spectral features
        spectral_features = self._extract_spectral_features(data)
        features.update(spectral_features)
        
        # 8. Dictionary-based pattern features
        dict_features = self._extract_dictionary_features(chunk)
        features.update(dict_features)
        
        # 9. Lightweight feature-selective mechanisms using statistical attention
        lsf_features = self._extract_lsf_features(data)
        features.update(lsf_features)
        
        return features
    
    def _extract_wavelet_features(self, data):
        """
        Extract features using wavelet decomposition for multi-resolution analysis
        """
        features = {}
        
        # Skip if data is too small for wavelet transform
        if len(data) < 2**self.params.wavelet_levels:
            return features
        
        try:
            # Perform wavelet decomposition
            coeffs = pywt.wavedec(data, self.params.wavelet, level=min(self.params.wavelet_levels, 
                                                              pywt.dwt_max_level(len(data), self.params.wavelet)))
            
            # Extract statistical features from each coefficient set
            for i, coeff in enumerate(coeffs):
                prefix = "approx_" if i == 0 else f"detail_{i}_"
                
                features[prefix + "mean"] = float(np.mean(coeff))
                features[prefix + "std"] = float(np.std(coeff))
                features[prefix + "energy"] = float(np.sum(coeff**2))
                features[prefix + "entropy"] = float(entropy(np.abs(coeff) + 1e-10))
                
                # Add higher order statistics for better noise pattern capture
                if len(coeff) > 5:  # Need sufficient points for valid higher-order stats
                    features[prefix + "skew"] = float(skew(coeff))
                    features[prefix + "kurtosis"] = float(kurtosis(coeff))
                    
                    # Add zero-crossing rate for wavelet coefficients
                    zero_crossings = np.sum(np.diff(coeff > 0).astype(bool))
                    features[prefix + "zero_crossing"] = float(zero_crossings) / max(1, len(coeff) - 1)
        except Exception:
            # Fallback if wavelet transform fails
            features["wavelet_fallback"] = 1.0
            
        return features
    
    def _extract_statistical_features(self, data):
        """
        Extract comprehensive statistical features from the data
        """
        features = {}
        
        # Basic statistics
        features["mean"] = float(np.mean(data))
        features["median"] = float(np.median(data))
        features["std"] = float(np.std(data))
        features["min"] = float(np.min(data))
        features["max"] = float(np.max(data))
        features["range"] = float(np.max(data) - np.min(data))
        
        # Distribution shape
        features["entropy"] = float(entropy(np.bincount(data) + 1e-10))
        features["unique_bytes"] = len(np.unique(data)) / 256.0
        
        # Percentiles for better distribution characterization
        for p in [10, 25, 75, 90]:
            features[f"percentile_{p}"] = float(np.percentile(data, p))
        
        # Calculate inter-quartile range
        features["iqr"] = float(np.percentile(data, 75) - np.percentile(data, 25))
        
        # Calculate zero-crossing rate (how often the value crosses the mean)
        mean = np.mean(data)
        zero_crossings = np.sum(np.diff(data > mean).astype(bool))
        features["zero_crossing_rate"] = float(zero_crossings) / max(1, len(data) - 1)
        
        # Peak ratio (ratio of values higher than 1 std above mean)
        std = np.std(data)
        peaks = np.sum(data > (mean + std))
        features["peak_ratio"] = float(peaks) / max(1, len(data))
        
        # Calculate permutation entropy if enough data points
        if len(data) >= 5:
            features["perm_entropy"] = self._permutation_entropy(data, order=3)
        
        # Calculate run-length encoding related statistics
        rle_stats = self._calculate_rle_stats(data)
        features.update(rle_stats)
        
        # Calculate rank-order statistics
        if len(data) > 10:
            # Apply rank transformation
            ranks = rankdata(data)
            rank_mean = np.mean(ranks)
            rank_std = np.std(ranks)
            
            # Calculate spearman correlation between position and value
            positions = np.arange(len(data))
            features["rank_trend"] = float(np.corrcoef(positions, ranks)[0, 1])
            
            # Calculate rank concentration
            features["rank_concentration"] = float(np.sum((ranks - rank_mean)**2)) / (len(data) * (rank_std + 1e-10)**2)
        
        return features
    
    def _calculate_rle_stats(self, data):
        """
        Calculate run-length encoding statistics to capture repetition patterns
        """
        features = {}
        
        # Skip if data is too small
        if len(data) < 3:
            return features
        
        # Find runs of identical bytes
        runs = []
        run_length = 1
        
        for i in range(1, len(data)):
            if data[i] == data[i-1]:
                run_length += 1
            else:
                runs.append((data[i-1], run_length))
                run_length = 1
        
        # Add the last run
        if run_length > 0:
            runs.append((data[-1], run_length))
        
        if not runs:
            return features
        
        # Calculate statistics on run lengths
        run_lengths = [length for _, length in runs]
        
        features["avg_run_length"] = float(np.mean(run_lengths))
        features["max_run_length"] = float(np.max(run_lengths))
        features["std_run_length"] = float(np.std(run_lengths))
        
        # Calculate entropy of run lengths
        run_length_counts = Counter(run_lengths)
        run_length_probs = np.array(list(run_length_counts.values())) / len(run_lengths)
        features["run_length_entropy"] = float(entropy(run_length_probs))
        
        # Calculate compression ratio using zlib (estimate of data redundancy)
        try:
            compressed_size = len(zlib.compress(data.tobytes()))
            features["compression_ratio"] = float(len(data) / max(1, compressed_size))
        except:
            features["compression_ratio"] = 1.0
        
        return features
    
    def _permutation_entropy(self, data, order=3, delay=1):
        """
        Calculate permutation entropy to quantify complexity in the sequence
        without assuming any particular distribution
        """
        n = len(data)
        if n < order + 1:
            return 0.0
            
        # Create patterns
        patterns = np.zeros(n - delay * (order - 1))
        for i in range(order):
            patterns = patterns * order + rankdata(data[i * delay:i * delay + len(patterns)], method='ordinal') - 1
            
        # Count patterns
        counter = Counter(patterns)
        probs = np.array(list(counter.values())) / len(patterns)
        
        # Calculate entropy
        return float(entropy(probs))
    
    def _extract_ngram_features(self, data):
        """
        Extract n-gram frequency features to capture sequential patterns
        """
        features = {}
        
        for n in self.params.ngram_sizes:
            # Skip if data is too small for this n-gram size
            if len(data) < n:
                continue
            
            # Extract n-grams
            ngrams = [bytes(data[i:i+n]) for i in range(len(data) - n + 1)]
            
            # Count n-gram frequencies
            ngram_counts = Counter(ngrams)
            
            # Get top n-grams
            top_ngrams = ngram_counts.most_common(self.params.top_ngrams)
            
            # Convert to features
            for i, (ngram, count) in enumerate(top_ngrams):
                if i >= self.params.top_ngrams:
                    break
                    
                # Create a deterministic feature name from the n-gram bytes
                ngram_hash = xxhash.xxh32(ngram).hexdigest()
                feature_name = f"ngram_{n}_{ngram_hash}"
                
                # Normalize count by total possible n-grams
                features[feature_name] = float(count) / max(1, len(data) - n + 1)
            
            # Add overall statistics for this n-gram size
            ngram_freqs = np.array(list(ngram_counts.values()))
            features[f"ngram_{n}_entropy"] = float(entropy(ngram_freqs / np.sum(ngram_freqs)))
            features[f"ngram_{n}_unique_ratio"] = float(len(ngram_counts)) / max(1, len(data) - n + 1)
        
        return features
    
    def _extract_cellular_features(self, data):
        """
        Extract features using cellular memory dynamics from the Cell AI model
        This emulates key aspects of cellular memory equations
        """
        features = {}
        
        # Skip if data is too small
        if len(data) < 10:
            return features
        
        # Initialize state vector
        state_size = min(256, len(data))
        state = np.zeros(state_size)
        memory = np.zeros_like(state)
        
        # Process data through cellular dynamics equations
        for t, byte_val in enumerate(data):
            # Fix: Ensure byte is in bounds for uint8 by applying modulo 256
            byte = int(byte_val) % 256
            
            # Update state based on cellular equation
            # Simplified version of: dS/dt = f(I, S, t) - γS + D∇²S + η(t)
            
            # Input influence - ensure index is in bounds with another modulo
            input_term = np.zeros_like(state)
            input_idx = byte % state_size
            input_term[input_idx] = 1.0
            
            # Diffusion term (simplified ∇²S as difference with neighbors)
            diffusion = np.zeros_like(state)
            for i in range(len(state)):
                neighbors = [(i-1) % state_size, (i+1) % state_size]
                neighbor_avg = np.mean([state[j] for j in neighbors])
                diffusion[i] = self.params.D * (neighbor_avg - state[i])
            
            # Decay term
            decay = -self.params.gamma * state
            
            # Noise term
            noise = self.params.eta * np.random.randn(len(state))
            
            # Update state with all terms
            dstate = input_term + diffusion + decay + noise
            state = state + self.params.dt * dstate
            
            # Memory integration (simplified memory kernel)
            memory = 0.9 * memory + 0.1 * state
        
        # Extract features from final state and memory
        features["cellular_state_mean"] = float(np.mean(state))
        features["cellular_state_std"] = float(np.std(state))
        features["cellular_state_entropy"] = float(entropy(np.abs(state) + 1e-10))
        features["cellular_state_energy"] = float(np.sum(state**2))
        
        features["cellular_memory_mean"] = float(np.mean(memory))
        features["cellular_memory_std"] = float(np.std(memory))
        features["cellular_memory_entropy"] = float(entropy(np.abs(memory) + 1e-10))
        features["cellular_memory_energy"] = float(np.sum(memory**2))
        
        # Extract top activated state indices
        top_indices = np.argsort(state)[-5:]
        for i, idx in enumerate(top_indices):
            features[f"cellular_top_{i}"] = float(idx) / (state_size - 1)  # Normalize by state size
            features[f"cellular_top_{i}_value"] = float(state[idx])
        
        return features
    
    def _extract_reservoir_features(self, data):
        """
        Extract features using dynamic reservoir computing approach (DAMR)
        """
        features = {}
        
        # Initialize reservoirs (one per scale)
        reservoirs = [np.zeros(self.params.reservoir_size) for _ in range(self.params.num_reservoirs)]
        
        # Pre-calculate neighbor indices
        neighbor_indices = {}
        for b in range(256):
            neighbors = {}
            # Fixed: Using the actual radius values from the list instead of max() on the list
            for r_idx, radius in enumerate(self.params.influence_radius):
                if radius < 1:
                    continue
                neighbors[radius] = [(b - radius) % 256, (b + radius) % 256]
            neighbor_indices[b] = neighbors
        
        # Sliding window for context-aware updates
        window_size = min(8, len(data))
        window = deque(maxlen=window_size)
        
        # Process each byte through the reservoirs
        for byte_val in data:
            # Fix: Ensure value is in uint8 range (0-255) by applying modulo
            byte = int(byte_val) % 256
            
            # Update window
            window.append(byte)
            
            # Calculate contextual boost factor
            context_boost = 1.0
            if len(window) >= 3:
                # Count repeats in window
                repeat_count = window.count(byte)
                if repeat_count > 1:
                    # Fast sigmoid approximation: x / (1 + |x|)
                    x = repeat_count - 1.5
                    context_boost = x / (1.0 + abs(x))
            
            # Update each reservoir
            for r_idx, reservoir in enumerate(reservoirs):
                # Base increment for current byte
                reservoir[byte] += 1
                
                # Apply neighbor influence with decay
                radius = self.params.influence_radius[r_idx]
                strength = self.params.influence_strength[r_idx] * context_boost
                
                # Fixed: Check neighbors directly for this radius
                if radius in neighbor_indices[byte]:
                    neighbors = neighbor_indices[byte][radius]
                    decay_factor = strength
                    
                    for neighbor in neighbors:
                        reservoir[neighbor] += decay_factor
        
        # Extract features from each reservoir state
        for r_idx, reservoir in enumerate(reservoirs):
            # Normalize reservoir by dividing by data length
            normalized = reservoir / max(1, len(data))
            
            # Calculate reservoir statistics
            features[f"reservoir_{r_idx}_mean"] = float(np.mean(normalized))
            features[f"reservoir_{r_idx}_std"] = float(np.std(normalized))
            features[f"reservoir_{r_idx}_entropy"] = float(entropy(normalized + 1e-10))
            features[f"reservoir_{r_idx}_max"] = float(np.max(normalized))
            features[f"reservoir_{r_idx}_sparsity"] = float(np.sum(normalized > 0.01) / len(normalized))
            
            # Find indices of top activated nodes
            top_indices = np.argsort(normalized)[-10:]
            for i, idx in enumerate(top_indices):
                features[f"reservoir_{r_idx}_top_{i}"] = float(idx) / 255.0
                features[f"reservoir_{r_idx}_top_{i}_value"] = float(normalized[idx])
            
            # Calculate spectral properties of the reservoir state
            fft_vals = np.abs(fft(normalized))
            fft_vals = fft_vals[:len(normalized)//2]
            if len(fft_vals) > 0:
                features[f"reservoir_{r_idx}_spectral_mean"] = float(np.mean(fft_vals))
                features[f"reservoir_{r_idx}_spectral_energy"] = float(np.sum(fft_vals**2))
        
        return features
    
    def _extract_spectral_features(self, data):
        """
        Extract spectral features using FFT to capture frequency domain characteristics
        """
        features = {}
        
        # Skip if data is too small
        if len(data) < 32:
            return features
        
        # Perform FFT
        try:
            # Zero-pad to next power of 2 for efficiency
            next_pow2 = int(2 ** np.ceil(np.log2(len(data))))
            padded = np.zeros(next_pow2)
            padded[:len(data)] = data
            
            # Compute FFT
            spectrum = np.abs(fft(padded))
            spectrum = spectrum[:next_pow2 // 2]  # Only need first half
            
            # Normalize
            spectrum = spectrum / max(np.max(spectrum), 1e-10)
            
            # Extract features from spectrum
            features["spectral_mean"] = float(np.mean(spectrum))
            features["spectral_std"] = float(np.std(spectrum))
            features["spectral_entropy"] = float(entropy(spectrum + 1e-10))
            features["spectral_energy"] = float(np.sum(spectrum**2))
            
            # Spectral centroid (weighted average of frequencies)
            freqs = np.arange(len(spectrum))
            features["spectral_centroid"] = float(np.sum(freqs * spectrum) / np.sum(spectrum))
            
            # Spectral spread (variance around centroid)
            centroid = features["spectral_centroid"]
            features["spectral_spread"] = float(np.sqrt(np.sum((freqs - centroid)**2 * spectrum) / np.sum(spectrum)))
            
            # Energy in different frequency bands
            band_size = len(spectrum) // 4
            for i in range(4):
                start = i * band_size
                end = (i + 1) * band_size if i < 3 else len(spectrum)
                band_energy = np.sum(spectrum[start:end] ** 2)
                features[f"spectral_band_{i}_energy"] = float(band_energy)
            
            # Find dominant frequencies
            top_freq_indices = np.argsort(spectrum)[-5:]
            for i, idx in enumerate(top_freq_indices):
                features[f"dominant_freq_{i}"] = float(idx) / len(spectrum)
                features[f"dominant_freq_{i}_magnitude"] = float(spectrum[idx])
                
        except Exception:
            features["spectral_fallback"] = 1.0
            
        return features
    
    def _extract_dictionary_features(self, chunk):
        """
        Extract features based on dictionary pattern matching
        Similar to compression algorithms like LZ77/LZ78
        """
        features = {}
        
        if not self.dictionary:
            return features
        
        # Count pattern occurrences
        pattern_counts = {}
        total_matched_bytes = 0
        
        for pattern_hash, (pattern, _) in self.dictionary.items():
            # Count occurrences of this pattern in the chunk
            count = 0
            pos = 0
            
            while True:
                pos = chunk.find(pattern, pos)
                if pos == -1:
                    break
                count += 1
                pos += 1
                
            if count > 0:
                pattern_counts[pattern_hash] = count
                total_matched_bytes += len(pattern) * count
        
        # Calculate dictionary match statistics
        features["dict_match_ratio"] = float(total_matched_bytes) / max(1, len(chunk))
        features["dict_match_count"] = float(len(pattern_counts))
        features["dict_pattern_diversity"] = float(len(pattern_counts)) / max(1, len(self.dictionary))
        
        # Add top patterns as features
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        for i, (pattern_hash, count) in enumerate(sorted_patterns[:10]):
            # Limit to top 10 patterns
            features[f"dict_pattern_{i}_freq"] = float(count) / max(1, len(chunk))
        
        return features
    
    def _extract_lsf_features(self, data):
        """
        Extract features using Lightweight Feature-Selective (LFS) mechanism
        using statistical measures of feature importance
        """
        features = {}
        
        # Skip if data is too small
        if len(data) < 16:
            return features
        
        # Calculate statistical importance scores
        importance_scores = {}
        
        # Split data into overlapping windows
        window_size = min(64, len(data))
        stride = max(1, window_size // 4)
        
        windows = []
        for i in range(0, len(data) - window_size + 1, stride):
            windows.append(data[i:i+window_size])
        
        if not windows:
            return features
        
        # Calculate basic statistics for each window
        window_stats = []
        for window in windows:
            stats = {}
            stats["mean"] = float(np.mean(window))
            stats["std"] = float(np.std(window))
            stats["entropy"] = float(entropy(np.bincount(window) + 1e-10))
            window_stats.append(stats)
        
        # Calculate importance scores (variation across windows)
        for stat in ["mean", "std", "entropy"]:
            values = [stats[stat] for stats in window_stats]
            importance_scores[stat] = float(np.std(values))
        
        # Apply adaptive threshold to identify significant windows
        mean_importance = np.mean(list(importance_scores.values()))
        std_importance = np.std(list(importance_scores.values()))
        threshold = mean_importance + 0.1 * std_importance
        
        # Select significant windows
        significant_indices = []
        for i, window_stat in enumerate(window_stats):
            # A window is significant if any of its stats has high importance
            if any(window_stat[stat] > threshold for stat in ["mean", "std", "entropy"]):
                significant_indices.append(i)
        
        # Extract features from significant windows
        if significant_indices:
            # Create sparse vector representation
            for i, idx in enumerate(significant_indices[:5]):  # Limit to top 5 significant windows
                window = windows[idx]
                features[f"lsf_window_{i}_mean"] = float(np.mean(window))
                features[f"lsf_window_{i}_std"] = float(np.std(window))
                features[f"lsf_window_{i}_entropy"] = float(entropy(np.bincount(window) + 1e-10))
                features[f"lsf_window_{i}_position"] = float(idx) / max(1, len(windows))
        
        # Calculate LSH signatures for quick similarity comparison
        lsh_sigs = self._calculate_lsh_signatures(data)
        for i, sig in enumerate(lsh_sigs[:10]):  # Limit to first 10 signatures
            features[f"lsh_sig_{i}"] = float(sig) / (2**32 - 1)  # Normalize to [0,1]
        
        return features
    
    def _calculate_lsh_signatures(self, data):
        """
        Calculate Locality-Sensitive Hashing signatures for fast similarity search
        """
        signatures = []
        
        # Use Murmurhash3 for fast hashing
        for seed in range(self.params.lsh_num_hashes):
            hash_val = mmh3.hash(data.tobytes(), seed=seed, signed=False)
            signatures.append(hash_val)
        
        return signatures
    
    def _extract_global_features(self, data, chunks):
        """
        Extract global features from the entire data that can't be captured
        at the chunk level
        """
        features = {}
        
        # Calculate chunk size statistics
        chunk_sizes = [len(chunk) for chunk in chunks]
        if chunk_sizes:
            features["chunk_count"] = float(len(chunks))
            features["avg_chunk_size"] = float(np.mean(chunk_sizes))
            features["std_chunk_size"] = float(np.std(chunk_sizes))
            features["chunk_size_entropy"] = float(entropy(chunk_sizes))
        
        # Calculate compression ratio of the entire data
        try:
            compressed = zlib.compress(data)
            features["global_compression_ratio"] = float(len(data)) / max(1, len(compressed))
        except:
            features["global_compression_ratio"] = 1.0
        
        # Calculate Shannon entropy of the entire data
        byte_counts = Counter(data)
        byte_probs = np.array(list(byte_counts.values())) / len(data)
        features["global_entropy"] = float(entropy(byte_probs))
        
        # Number of unique bytes
        features["unique_byte_ratio"] = float(len(byte_counts)) / 256.0
        
        # Byte distribution statistics
        byte_values = np.array(list(byte_counts.keys()))
        byte_freqs = np.array(list(byte_counts.values())) / len(data)
        
        if len(byte_values) > 0:
            # Calculate weighted average of byte values
            features["byte_value_mean"] = float(np.sum(byte_values * byte_freqs))
            
            # Calculate weighted standard deviation of byte values
            features["byte_value_std"] = float(np.sqrt(np.sum(byte_freqs * (byte_values - features["byte_value_mean"])**2)))
        
        return features
    
    def _combine_chunk_features(self, feature_sets):
        """
        Combine features from multiple chunks into a single feature set
        Implementation added - was missing in original code
        """
        # Gather all unique feature names
        all_features = set()
        for features in feature_sets:
            all_features.update(features.keys())
        
        # Combine features across chunks
        combined = {}
        
        for feature in all_features:
            # Get all values for this feature across chunks
            values = [features.get(feature, 0.0) for features in feature_sets]
            values = [v for v in values if np.isfinite(v)]
            
            if not values:
                continue
                
            # Calculate aggregate statistics
            combined[feature + "_mean"] = float(np.mean(values))
            combined[feature + "_max"] = float(np.max(values))
            
            # Only calculate standard deviation if we have enough chunks
            if len(values) > 1:
                combined[feature + "_std"] = float(np.std(values))
        
        return combined
    
    def _reduce_dimensionality(self, features):
        """
        Reduce dimensionality of feature space using SVD and random projections
        """
        # Convert features to vector form
        feature_keys = sorted(features.keys())
        feature_vector = np.array([features[k] for k in feature_keys])
        
        # Replace non-finite values
        feature_vector = np.nan_to_num(feature_vector, nan=0.0, posinf=1e6, neginf=-1e6)
        
        reduced_features = {}
        
        try:
            # Apply truncated SVD for high-variance components
            svd = TruncatedSVD(n_components=min(self.params.pca_components, len(feature_vector)-1))
            svd_transformed = svd.fit_transform(feature_vector.reshape(1, -1))[0]
            
            for i, val in enumerate(svd_transformed):
                reduced_features[f"svd_{i}"] = float(val)
                
            # Apply random projection for better distance preservation
            rp = GaussianRandomProjection(n_components=min(self.params.random_proj_components, len(feature_vector)))
            rp_transformed = rp.fit_transform(feature_vector.reshape(1, -1))[0]
            
            for i, val in enumerate(rp_transformed):
                reduced_features[f"rp_{i}"] = float(val)
                
        except Exception:
            # Fallback if dimensionality reduction fails
            # Just return a subset of original features
            for i, k in enumerate(feature_keys[:200]):  # Limit to first 200 features
                reduced_features[k] = features[k]
        
        return reduced_features
    
    def _select_top_features(self, features, max_features):
        """
        Select the most important features based on importance scores
        Implementation added - was missing in original code
        """
        if not features:
            return []
            
        # Calculate importance score for each feature
        # Importance is a combination of entropy and standard deviation (if available)
        importance_scores = {}
        
        for feature, value in features.items():
            # Skip if value is not finite
            if not np.isfinite(value):
                continue
                
            # Calculate base importance from the feature value itself
            base_importance = abs(value)
            
            # If we have std of this feature across chunks, factor it in
            std_feature = feature.replace("_mean", "_std")
            if std_feature in features:
                std_value = features[std_feature]
                if np.isfinite(std_value):
                    base_importance *= (1 + std_value)
            
            importance_scores[feature] = base_importance
        
        # Select top features based on importance score
        sorted_features = sorted(importance_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Keep only top 30% or max_features, whichever is smaller
        num_to_keep = min(max_features, int(len(sorted_features) * self.params.selection_threshold))
        selected = [value for feature, value in sorted_features[:num_to_keep]]
        
        return selected
    
    def _extract_basic_stats(self, data):
        """
        Extract very basic statistical features as fallback
        Used when other methods fail to produce features
        """
        # Convert to numpy array
        data_array = np.frombuffer(data, dtype=np.uint8)
        
        # Basic statistics that are almost guaranteed to work
        features = [
            float(np.mean(data_array)),
            float(np.std(data_array)),
            float(np.min(data_array)),
            float(np.max(data_array)),
            len(data_array)
        ]
        
        # Add byte frequency features
        hist, _ = np.histogram(data_array, bins=16, range=(0, 256))
        features.extend([float(h) / max(1, len(data_array)) for h in hist])
        
        return features
        
    def encode_file(self, file_path, max_features=2000):
        """Encode a file using the cellular binary encoder"""
        with open(file_path, 'rb') as f:
            features = self.encode(f, max_features=max_features)
        
        return features
    
    def encode_bytes(self, binary_data, max_features=2000):
        """Encode bytes using the cellular binary encoder"""
        features = self.encode(binary_data, max_features=max_features)
        return features


class CellularMemory(nn.Module):
    """
    Implementation of the complete cellular memory dynamics for binary streams
    Includes the full set of equations from the CellAI mathematical framework
    
    Mathematical foundation:
    Core equation: dS/dt = f(I, S, t) - γS + D∇²S + η(t)
    Energy-based transitions: P(Si→Sj) = exp(-ΔEij/kT) / Z
    Boundary conditions: B(Sᵢ, Sⱼ) = 0 for adjacent partitions
    """
    def __init__(self, state_size: int, params: ModelParams):
        super().__init__()
        self.state_size = state_size
        self.params = params
        
        # Weight matrices for energy calculation
        self.W = nn.Parameter(torch.randn(state_size, state_size) * 0.01)
        
        # Cellular gates - used to process input and current state
        self.input_gate = nn.Linear(state_size * 2, state_size)
        self.forget_gate = nn.Linear(state_size * 2, state_size)
        self.output_gate = nn.Linear(state_size * 2, state_size)
        self.cell_gate = nn.Linear(state_size * 2, state_size)
        
        # Energy function parameters
        self.energy_scale = params.energy_scale
        self.temperature = params.temperature
        
        # Boundary condition coupling strength
        self.boundary_coupling = nn.Parameter(torch.tensor(params.boundary_strength))
        
        # Memory kernel for temporal integration
        self.memory_kernel = TemporalMemoryKernel(
            state_size,
            params.kernel_terms,
            params.kernel_decays
        )
        
        # Emergent properties detector
        self.emergence_detector = nn.Linear(state_size, 1)
        self.collective_threshold = params.collective_threshold
        
    def compute_energy(self, state: torch.Tensor) -> torch.Tensor:
        """Compute energy of state for probabilistic transitions"""
        # Use quadratic energy function: E(s) = s^T W s
        energy = torch.sum(state * torch.matmul(state, self.W), dim=-1)
        return energy * self.energy_scale
    
    def compute_transition_prob(self, state: torch.Tensor, next_state: torch.Tensor) -> torch.Tensor:
        """Compute transition probability using Boltzmann distribution"""
        # Calculate energy of current and next states
        energy_current = self.compute_energy(state)
        energy_next = self.compute_energy(next_state)
        
        # Energy difference
        energy_diff = energy_next - energy_current
        
        # Boltzmann probability: P(s→s') = exp(-ΔE/kT)/Z
        # We omit the partition function Z since we only need relative probabilities
        transition_prob = torch.exp(-energy_diff / self.temperature)
        
        return transition_prob
    
    def apply_boundary_conditions(self, state: torch.Tensor, 
                                neighbor_states: torch.Tensor) -> torch.Tensor:
        """Apply detailed boundary conditions between partitions"""
        if neighbor_states.size(0) == 0:
            return state
            
        # Calculate average neighbor state
        avg_neighbor = torch.mean(neighbor_states, dim=0)
        
        # Apply boundary condition B(Sᵢ, Sⱼ) = 0
        # Implementation: pull states at boundaries toward average of neighbors
        boundary_force = self.boundary_coupling * (avg_neighbor - state)
        
        # Apply force at boundaries only (first and last 10% of state)
        boundary_size = max(1, int(self.state_size * 0.1))
        boundary_mask = torch.zeros_like(state)
        boundary_mask[:boundary_size] = 1.0
        boundary_mask[-boundary_size:] = 1.0
        
        # Apply boundary conditions
        state = state + boundary_force * boundary_mask
        
        return state
    
    def detect_emergence(self, states: torch.Tensor) -> torch.Tensor:
        """Detect emergent collective properties in states"""
        # Compute emergence score
        scores = self.emergence_detector(states).squeeze(-1)
        
        # Apply threshold
        emergence = (scores > self.collective_threshold).float()
        
        return emergence
    
    def forward(self, state: torch.Tensor, 
               input_signal: torch.Tensor, 
               neighbor_states: torch.Tensor,
               time_point: float) -> Dict[str, torch.Tensor]:
        """
        Complete cellular update with all mathematical components
        
        Args:
            state: Current state [batch_size, state_size]
            input_signal: Input signal [batch_size, state_size]
            neighbor_states: Neighbor states [num_neighbors, batch_size, state_size]
            time_point: Current time point
            
        Returns:
            Dict with updated state and metadata
        """
        # Ensure inputs are correctly shaped
        if state.dim() == 1:
            state = state.unsqueeze(0)
        if input_signal.dim() == 1:
            input_signal = input_signal.unsqueeze(0)
            
        # Combine state and input for gating (like in LSTM cells)
        combined = torch.cat([state, input_signal], dim=-1)
        
        # Compute gates
        i = torch.sigmoid(self.input_gate(combined))
        f = torch.sigmoid(self.forget_gate(combined))
        o = torch.sigmoid(self.output_gate(combined))
        g = torch.tanh(self.cell_gate(combined))
        
        # Update cell state with gates
        cell_state = f * state + i * g
        output_state = o * torch.tanh(cell_state)
        
        # Compute diffusion term D∇²S (influence from neighbors)
        diffusion = torch.zeros_like(state)
        
        # Fixed: Properly handle neighbor_states dimensions for diffusion
        if neighbor_states.numel() > 0:
            # Ensure neighbor_states has correct shape: [batch_size, num_neighbors, state_size]
            if neighbor_states.dim() == 2:  
                # If [num_neighbors, state_size] -> [1, num_neighbors, state_size]
                neighbor_states = neighbor_states.unsqueeze(0)
            elif neighbor_states.dim() == 3 and neighbor_states.size(1) != state.size(0):
                # If [num_neighbors, batch_size, state_size] -> [batch_size, num_neighbors, state_size]
                neighbor_states = neighbor_states.permute(1, 0, 2)
                
            # Calculate mean across neighbors dimension
            neighbor_means = torch.mean(neighbor_states, dim=1)
            diffusion = self.params.D * (neighbor_means - state)
        
        # Compute decay term -γS
        decay = -self.params.gamma * cell_state
        
        # Add noise term η(t)
        noise = self.params.eta * torch.randn_like(cell_state)
        
        # Compute full state update
        d_state = output_state + diffusion + decay + noise
        
        # Euler integration step
        new_state = state + self.params.dt * d_state
        
        # Apply boundary conditions
        new_state = self.apply_boundary_conditions(new_state, neighbor_states)
        
        # Calculate transition probability
        transition_prob = self.compute_transition_prob(state, new_state)
        
        # Apply temporal memory integration
        memory_state = self.memory_kernel(new_state, time_point)
        
        # Fixed: Detect emergent properties (properly handle dimensions)
        emergence = torch.zeros(new_state.size(0), device=new_state.device)
        if neighbor_states.numel() > 0:
            # Ensure both tensors have compatible dimensions for concatenation
            all_states = torch.cat([new_state.unsqueeze(1), 
                                   neighbor_states], dim=1)
            
            # Reshape for emergence detector: [batch_size * (num_neighbors+1), state_size]
            all_states_flat = all_states.reshape(-1, self.state_size)
            emergence_flat = self.detect_emergence(all_states_flat)
            
            # Reshape back to get per-batch emergence
            emergence = emergence_flat.reshape(new_state.size(0), -1).mean(dim=1)
            
        return {
            'new_state': new_state,
            'transition_prob': transition_prob,
            'memory_state': memory_state,
            'emergence': emergence
        }


class TemporalMemoryKernel(nn.Module):
    """
    Implements temporal integration for memory using memory kernels
    Based on the Multi-Scale Memory equations from the CellAI math framework
    
    Mathematical foundation:
    M(t) = ∫[t-τ, t] w(t-s)I(s)ds + ∫[0, t] K(t-s)S(s)ds
    K(t) = ∑ₖ αₖexp(-t/τₖ)  (Memory kernel)
    """
    def __init__(self, state_size: int, kernel_terms: int, kernel_decays: List[float], 
                max_history_length: int = 50):
        super().__init__()
        self.state_size = state_size
        self.kernel_terms = kernel_terms
        self.max_history_length = max_history_length
        
        # Register kernel decay rates (τₖ in the equations)
        self.register_buffer('kernel_decays', torch.tensor(kernel_decays))
        
        # Learnable kernel coefficients (αₖ in the equations)
        self.kernel_coefs = nn.Parameter(torch.ones(kernel_terms) / kernel_terms)
        
        # State history buffer - will store past states and times
        # Fixed: Initialize with correct dimensions
        self.register_buffer('state_history', torch.zeros(0, 0, state_size))
        self.register_buffer('time_points', torch.zeros(0))
        
    def forward(self, current_state: torch.Tensor, current_time: float, 
               reset_history: bool = False) -> torch.Tensor:
        """
        Apply temporal memory integration
        
        Args:
            current_state: Current state tensor [batch_size, state_size]
            current_time: Current time point
            reset_history: Whether to reset the history buffer
            
        Returns:
            memory_state: Memory-integrated state [batch_size, state_size]
        """
        batch_size = current_state.size(0)
        device = current_state.device
        
        # Reset history if requested or if batch size changes
        if reset_history or (self.state_history.size(0) > 0 and 
                            self.state_history.size(1) != batch_size):
            # Fixed: Initialize with correct shape
            self.state_history = torch.zeros(0, batch_size, self.state_size, device=device)
            self.time_points = torch.zeros(0, device=device)
        
        # Ensure current state is correctly shaped for history buffer
        if current_state.dim() == 2:
            current_state_reshaped = current_state.unsqueeze(0)  # [1, batch_size, state_size]
        else:
            current_state_reshaped = current_state
            
        # If this is the first call or history is empty, initialize
        if self.state_history.size(0) == 0:
            self.state_history = current_state_reshaped
            self.time_points = torch.tensor([current_time], device=device)
            return current_state
        
        # Add current state to history
        self.state_history = torch.cat([self.state_history, current_state_reshaped], dim=0)
        self.time_points = torch.cat([self.time_points, torch.tensor([current_time], device=device)])
        
        # Trim history if too long
        if self.state_history.size(0) > self.max_history_length:
            self.state_history = self.state_history[-self.max_history_length:]
            self.time_points = self.time_points[-self.max_history_length:]
        
        # Calculate time differences
        time_diffs = current_time - self.time_points  # [history_len]
        
        # Apply memory kernel to history
        # K(t) = ∑ₖ αₖexp(-t/τₖ)
        memory_state = torch.zeros(batch_size, self.state_size, device=device)
        kernel_sum = 0.0
        
        # Calculate memory integration for each history point
        for i, time_diff in enumerate(time_diffs):
            # Calculate kernel value for this time difference
            kernel_value = 0.0
            for k in range(self.kernel_terms):
                # Get coefficient and decay rate
                alpha_k = torch.sigmoid(self.kernel_coefs[k])  # Keep coefficient positive
                tau_k = self.kernel_decays[k]
                
                # Calculate kernel contribution
                kernel_value += alpha_k * torch.exp(-time_diff / tau_k)
            
            # Add weighted contribution to memory state
            memory_state += kernel_value * self.state_history[i]
            kernel_sum += kernel_value
        
        # Normalize by sum of weights to maintain scale
        if kernel_sum > 0:
            memory_state = memory_state / kernel_sum
            
        return memory_state


class CellAIBinaryModel(nn.Module):
    """Complete CellAI Binary model with encoder and cellular memory components"""
    def __init__(self, params: Optional[ModelParams] = None):
        super().__init__()
        self.params = params or create_default_model_params()
        
        # Binary encoder (feature extractor)
        self.encoder = CellularBinaryEncoder(self.params.encoder_params)
        
        # Partitions (cellular memory layers)
        self.partitions = nn.ModuleList([
            CellularMemory(self.params.state_size, self.params)
            for _ in range(self.params.num_partitions)
        ])
        
        # Decoder (output projection)
        self.decoder = nn.Sequential(
            nn.Linear(self.params.state_size * self.params.num_partitions, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 256)
        )
        
    def forward(self, binary_data, time_step=0.0):
        """Process binary data through the model"""
        try:
            # Extract features using the binary encoder
            features = self.encoder.encode(binary_data)
            features_tensor = torch.tensor(features, dtype=torch.float32)
            
            # Additional safety check for NaN/Inf values
            if torch.isnan(features_tensor).any() or torch.isinf(features_tensor).any():
                # Replace NaN/Inf with zeros
                features_tensor = torch.nan_to_num(features_tensor, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Split features among partitions
            features_per_partition = max(1, len(features) // self.params.num_partitions)
            
            # Initialize states for each partition
            states = []
            memory_states = []
            
            # Process features through each partition
            for i, partition in enumerate(self.partitions):
                # Get features for this partition
                start_idx = i * features_per_partition
                end_idx = min(len(features), (i + 1) * features_per_partition)
                partition_features = features_tensor[start_idx:end_idx]
                
                # Pad or truncate to expected size
                if len(partition_features) < self.params.state_size:
                    padding = torch.zeros(self.params.state_size - len(partition_features))
                    partition_features = torch.cat([partition_features, padding])
                elif len(partition_features) > self.params.state_size:
                    partition_features = partition_features[:self.params.state_size]
                    
                # Normalize partition features for numerical stability
                partition_mean = partition_features.mean()
                partition_std = partition_features.std()
                if partition_std > 0:
                    partition_features = (partition_features - partition_mean) / (partition_std + 1e-8)
                
                # Clip to reasonable range
                partition_features = torch.clamp(partition_features, -10.0, 10.0)
                    
                # Create initial state and input signal
                initial_state = torch.zeros(1, self.params.state_size)
                input_signal = partition_features.unsqueeze(0)
                
                try:
                    # Get neighbor partition states for boundary conditions
                    if len(states) > 0:
                        # Ensure all tensors have consistent dimensions before stacking
                        processed_states = []
                        for state in states:
                            # Make sure all states have shape [1, state_size]
                            if state.dim() == 3:
                                processed_states.append(state.squeeze(1))  # Remove extra dimension
                            else:
                                processed_states.append(state)
                        
                        if len(processed_states) > 0:
                            try:
                                # Try to create neighbor states with proper dimensions
                                neighbor_states = torch.cat(processed_states, dim=0).unsqueeze(1)
                            except RuntimeError:
                                # If that fails, use empty tensor as fallback
                                neighbor_states = torch.zeros(0, 1, self.params.state_size)
                        else:
                            neighbor_states = torch.zeros(0, 1, self.params.state_size)
                    else:
                        neighbor_states = torch.zeros(0, 1, self.params.state_size)
                        
                    # Apply cellular dynamics
                    result = partition(initial_state, input_signal, neighbor_states, time_step)
                    
                    # Safety check on result
                    for key, value in result.items():
                        if torch.isnan(value).any() or torch.isinf(value).any():
                            # Use fallback value if NaN/Inf detected
                            result[key] = torch.zeros_like(value)
                    
                    # Store results
                    states.append(result['new_state'])
                    memory_states.append(result['memory_state'])
                except RuntimeError as e:
                    # Use zero state as fallback if dimensions don't match
                    fallback_state = torch.zeros_like(initial_state)
                    states.append(fallback_state)
                    memory_states.append(fallback_state)
            
            # Handle case where no states were successfully processed
            if not states:
                return torch.zeros(256)  # Return empty tensor as fallback
            
            try:
                # Properly reshape all states to 1D before concatenation
                reshaped_states = []
                for s in states:
                    if s.dim() > 1:
                        reshaped_states.append(s.reshape(-1))
                    else:
                        reshaped_states.append(s)
                        
                # Make sure all states have the same size
                min_size = min(s.size(0) for s in reshaped_states)
                trimmed_states = [s[:min_size] for s in reshaped_states]
                
                combined_state = torch.cat(trimmed_states)
                
                # Ensure combined state has correct shape for decoder
                if combined_state.dim() == 1:
                    # Add batch dimension if missing
                    combined_state = combined_state.unsqueeze(0)
                
                # Final safety check before decoding
                combined_state = torch.nan_to_num(combined_state, nan=0.0, posinf=1.0, neginf=-1.0)
                combined_state = torch.clamp(combined_state, -10.0, 10.0)
                
                # Decode state to output
                output = self.decoder(combined_state)
                
                # Safety check on output
                if torch.isnan(output).any() or torch.isinf(output).any():
                    output = torch.zeros_like(output)
                
                # Make sure output is 1D to match target in training
                if output.dim() > 1:
                    output = output.squeeze(0)
                    
                return output
                
            except RuntimeError as e:
                # Last resort fallback - return zero tensor
                logging.warning(f"Using fallback zero tensor due to: {e}")
                return torch.zeros(256)
        except Exception as e:
            # Catch-all for other errors
            logging.error(f"Error in forward pass: {e}")
            return torch.zeros(256)
    
    def process_file(self, file_path):
        """Process a binary file and return encoded representation"""
        features = self.encoder.encode_file(file_path)
        return self(features)


def create_default_model_params():
    """Create default model parameters for the CellAI model"""
    return ModelParams(
        dt=0.1,
        D=0.2,
        gamma=0.1,
        eta=0.01,
        num_partitions=4,
        state_size=256,
        temperature=1.0,
        energy_scale=0.5,
        memory_tau=5.0,
        kernel_terms=3,
        kernel_decays=[1.0, 5.0, 10.0],
        boundary_strength=0.2,
        collective_threshold=0.7,
        chunk_size=2048,
        overlap=512,
        cell_hidden_size=512,
        learning_rate=1e-5,  # Reduced from 0.001 to 1e-5 for stability
        batch_size=4,  # Reduced from 8 to 4 for better stability
        accumulation_steps=4,
        early_stopping_patience=5,
        encoder_params=EncoderParams()
    )


class DatasetIterator:
    """Iterator for dataset files, supporting multiple formats"""
    def __init__(self, data_path, chunk_size=2048, overlap=512, max_chunks_per_file=1000):
        self.data_path = data_path
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.max_chunks_per_file = max_chunks_per_file
        
        # Determine files to process
        if os.path.isfile(data_path):
            self.files = [data_path]
        elif os.path.isdir(data_path):
            self.files = []
            for ext in ['.jsonl', '.json', '.txt', '.bin', '.csv']:
                self.files.extend(glob.glob(os.path.join(data_path, f'*{ext}')))
        else:
            raise ValueError(f"Invalid data path: {data_path}")
        
        if not self.files:
            raise ValueError(f"No valid data files found in {data_path}")
            
        # Calculate total items (used for progress bar)
        self.total_items = self._estimate_total_items()
            
        logging.info(f"Found {len(self.files)} files for processing")
        
    def _estimate_total_items(self):
        """Estimate the total number of chunks in all files"""
        total = 0
        
        for file_path in self.files:
            try:
                # Get file size
                file_size = os.path.getsize(file_path)
                
                if file_path.endswith(('.jsonl', '.json')):
                    # For JSON/JSONL, count lines as a rough estimate
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if file_path.endswith('.jsonl'):
                            # Sample the first few lines to get average line length
                            sample_lines = [len(f.readline()) for _ in range(min(100, file_size // 100))]
                            if sample_lines:
                                avg_line_length = sum(sample_lines) / len(sample_lines)
                                estimated_lines = min(file_size / max(1, avg_line_length), self.max_chunks_per_file)
                                total += estimated_lines
                            else:
                                # Fallback if no lines
                                total += min(file_size // self.chunk_size, self.max_chunks_per_file)
                        else:
                            # For single JSON, estimate based on file size
                            total += min(file_size // (self.chunk_size - self.overlap), self.max_chunks_per_file)
                else:
                    # For binary files, estimate based on size
                    total += min(file_size // (self.chunk_size - self.overlap), self.max_chunks_per_file)
            except Exception:
                # If estimation fails, use a reasonable default
                total += 100
                
        return max(1, int(total))
            
    def __iter__(self):
        """Iterate through all data chunks in all files"""
        for file_path in self.files:
            try:
                # Process file based on extension
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext in ['.jsonl', '.json']:
                    yield from self._process_json_file(file_path)
                else:
                    # Process as binary file
                    yield from self._process_binary_file(file_path)
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
                
    def __len__(self):
        """Return estimated number of items for progress bar"""
        return self.total_items
    
    def _process_json_file(self, file_path):
        """Process JSON/JSONL file and yield text chunks"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Check if it's a JSONL file
                if file_path.endswith('.jsonl'):
                    # Process line by line
                    line_count = 0
                    for line in f:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                texts = extract_texts_from_json(data)
                                for text in texts:
                                    for chunk in self._chunk_text(text):
                                        # Safely encode to UTF-8 and convert to bytes
                                        try:
                                            # Sanitize bytes to ensure they're valid for numpy uint8
                                            byte_data = bytearray(chunk.encode('utf-8'))
                                            # This is a safety measure but we'll handle uint8 bounds in processing
                                            yield bytes(byte_data)
                                        except UnicodeEncodeError as ue:
                                            logging.warning(f"Unicode encoding error: {ue}. Using ASCII fallback")
                                            # Fallback to ASCII with replacement
                                            yield chunk.encode('ascii', errors='replace')
                                
                                line_count += 1
                                if line_count >= self.max_chunks_per_file:
                                    logging.info(f"Reached max chunk limit for {file_path}")
                                    break
                            except json.JSONDecodeError:
                                logging.warning(f"Invalid JSON in line: {line[:50]}...")
                                continue
                else:
                    # Process as single JSON
                    data = json.load(f)
                    texts = extract_texts_from_json(data)
                    chunk_count = 0
                    for text in texts:
                        for chunk in self._chunk_text(text):
                            # Safely encode to UTF-8 with sanitization
                            try:
                                byte_data = bytearray(chunk.encode('utf-8'))
                                yield bytes(byte_data)
                            except UnicodeEncodeError as ue:
                                logging.warning(f"Unicode encoding error: {ue}. Using ASCII fallback")
                                yield chunk.encode('ascii', errors='replace')
                                
                            chunk_count += 1
                            if chunk_count >= self.max_chunks_per_file:
                                logging.info(f"Reached max chunk limit for {file_path}")
                                return
        except Exception as e:
            logging.error(f"Error processing JSON file {file_path}: {e}")
    
    def _process_binary_file(self, file_path):
        """Process binary file and yield binary chunks"""
        try:
            # Process file in chunks
            file_size = os.path.getsize(file_path)
            with open(file_path, 'rb') as f:
                # Use memory mapping for large files
                if file_size > 100 * 1024 * 1024:  # 100MB
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        for i in range(0, min(len(mm), self.max_chunks_per_file * self.chunk_size), 
                                     self.chunk_size - self.overlap):
                            chunk = mm[i:i+self.chunk_size]
                            if chunk:  # Skip empty chunks
                                yield chunk
                else:
                    # For smaller files, read directly
                    for i in range(0, min(file_size, self.max_chunks_per_file * self.chunk_size), 
                                 self.chunk_size - self.overlap):
                        f.seek(i)
                        chunk = f.read(self.chunk_size)
                        if chunk:  # Skip empty chunks
                            yield chunk
        except Exception as e:
            logging.error(f"Error processing binary file {file_path}: {e}")
    
    def _chunk_text(self, text):
        """Split text into overlapping chunks"""
        if not text or len(text) < 10:
            return []
            
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunk = text[i:i + self.chunk_size]
            if len(chunk) > 10:  # Skip very small chunks
                chunks.append(chunk)
                
        return chunks


def extract_texts_from_json(json_obj, max_depth=5, current_depth=0):
    """Extract text values from JSON objects recursively"""
    texts = []
    
    # Avoid excessive recursion
    if current_depth > max_depth:
        return texts
        
    if isinstance(json_obj, dict):
        # Process dictionary
        for key, value in json_obj.items():
            if isinstance(value, str) and len(value) > 5:
                # Add both the key and value if they're strings
                texts.append(value)
                if len(key) > 5:
                    texts.append(key)
            elif isinstance(value, (dict, list)):
                texts.extend(extract_texts_from_json(value, max_depth, current_depth + 1))
    elif isinstance(json_obj, list):
        # Process list
        for item in json_obj:
            if isinstance(item, str) and len(item) > 5:
                texts.append(item)
            elif isinstance(item, (dict, list)):
                texts.extend(extract_texts_from_json(item, max_depth, current_depth + 1))
    
    return texts


class TrainingManager:
    """Manages the training process for CellAI binary model"""
    def __init__(self, model, data_path, output_path, num_epochs, device=None, val_split=0.1):
        self.model = model
        self.data_path = data_path
        self.output_path = output_path
        self.num_epochs = num_epochs
        self.val_split = val_split
        
        # Initialize device
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Using device: {self.device}")
        
        # Move model to device
        self.model = self.model.to(self.device)
        
        # Setup optimizer and loss function - use smaller learning rate
        self.optimizer = optim.Adam(model.parameters(), lr=1e-5)
        
        # Use HuberLoss instead of MSE for better robustness to outliers
        self.criterion = nn.HuberLoss(delta=1.0)
        
        # Enable gradient scaler for numerical stability
        self.scaler = torch.cuda.amp.GradScaler() if torch.cuda.is_available() else None
        
        # Training stats
        self.stats = {
            'epoch_losses': [],
            'val_losses': [],
            'best_val_loss': float('inf'),
            'patience_counter': 0
        }
        
        # Set up learning rate scheduler
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, 'min', factor=0.5, patience=2, verbose=True
        )
    
    def train(self):
        """Run the full training process"""
        logging.info(f"Starting training for {self.num_epochs} epochs")
        
        # Safety check - make sure model's weights are finite before starting
        for name, param in self.model.named_parameters():
            if torch.isnan(param.data).any() or torch.isinf(param.data).any():
                logging.warning(f"Parameter {name} contains NaN or Inf values - reinitializing")
                # Reinitialize problematic parameters
                if "weight" in name:
                    nn.init.xavier_normal_(param.data)
                else:
                    nn.init.zeros_(param.data)
        
        for epoch in range(self.num_epochs):
            # Training phase
            try:
                train_loss = self._train_epoch(epoch)
                self.stats['epoch_losses'].append(train_loss)
                
                # Save checkpoint
                self._save_checkpoint(epoch, is_best=False)
                
                # Check early stopping
                if self._check_early_stopping(train_loss):
                    logging.info(f"Early stopping triggered after {epoch+1} epochs")
                    break
            except Exception as e:
                logging.error(f"Error during epoch {epoch+1}: {e}")
                # Try to continue with next epoch
                continue
                
        # Save final model
        self._save_final_model()
        
        return self.stats
    
    def _train_epoch(self, epoch):
        """Train for one epoch"""
        self.model.train()
        running_loss = 0.0
        batch_count = 0
        processed_chunks = 0
        successful_chunks = 0
        
        # Create data iterator
        dataset = DatasetIterator(
            self.data_path, 
            chunk_size=self.model.params.chunk_size,
            overlap=self.model.params.overlap
        )
        
        # Track batches and accumulation
        accumulated_loss = 0.0
        samples_in_batch = 0
        
        # Process batches with proper progress bar
        pbar = tqdm(total=dataset.total_items, desc=f"Epoch {epoch+1}/{self.num_epochs}")
        
        for i, chunk_bytes in enumerate(dataset):
            processed_chunks += 1
            pbar.update(1)  # Update progress bar for each chunk
            
            # Skip empty chunks
            if not chunk_bytes or len(chunk_bytes) < 10:
                continue
                
            try:
                # Sanity check on bytes - ensure all values are valid for uint8
                try:
                    # Create a numpy array to test if all bytes are valid
                    np_array = np.frombuffer(chunk_bytes, dtype=np.uint8)
                except ValueError as ve:
                    logging.warning(f"Invalid byte data in chunk {i}: {ve}, skipping")
                    continue
                
                # Extract features with numerical stability fixes 
                with torch.no_grad():
                    encoded_features = self.model.encoder.encode(chunk_bytes)
                    if len(encoded_features) == 0:
                        logging.warning(f"Encoder returned empty features for chunk {i}, skipping")
                        continue
                        
                    # Convert to tensor with fp32 precision
                    encoded_tensor = torch.tensor(encoded_features, dtype=torch.float32).to(self.device)
                    
                    # Additional safety check for NaN/Inf values
                    if torch.isnan(encoded_tensor).any() or torch.isinf(encoded_tensor).any():
                        logging.warning(f"NaN or Inf values in encoded features for chunk {i}, skipping")
                        continue
                
                # Create self-supervised target (reconstruction)
                # Make sure target is 2D: [1, feature_dim]
                if encoded_tensor.dim() == 1:
                    target = encoded_tensor.unsqueeze(0)  # Add batch dimension
                else:
                    target = encoded_tensor
                
                # Forward pass - use try/except to catch any dimension errors
                try:
                    # Use mixed precision if available
                    if self.scaler:
                        with torch.cuda.amp.autocast():
                            output = self.model(chunk_bytes)
                            output = output.to(self.device)
                    else:
                        output = self.model(chunk_bytes)
                        output = output.to(self.device)
                    
                    # Safety check - detect NaN/Inf values
                    if torch.isnan(output).any() or torch.isinf(output).any():
                        logging.warning(f"NaN or Inf values in model output for chunk {i}, skipping")
                        continue
                    
                    # Fix dimensions - ensure both tensors have same dimensions
                    if output.dim() == 1 and target.dim() == 2:
                        output = output.unsqueeze(0)  # Make output [1, feature_dim]
                    elif output.dim() == 2 and target.dim() == 1:
                        target = target.unsqueeze(0)  # Make target [1, feature_dim]
                    
                    # Trim or pad target to match output size
                    if output.size(-1) != target.size(-1):
                        if output.size(-1) < target.size(-1):
                            target = target[..., :output.size(-1)]
                        else:
                            # Pad target
                            padding_size = output.size(-1) - target.size(-1)
                            padding = torch.zeros(target.size(0), padding_size, device=self.device)
                            target = torch.cat([target, padding], dim=-1)
                    
                    # Normalize both tensors for stable loss calculation
                    def normalize_tensor(x):
                        x_mean = x.mean()
                        x_std = x.std()
                        if x_std > 0:
                            x = (x - x_mean) / (x_std + 1e-8)
                        return torch.clamp(x, -10, 10)  # Clip values
                        
                    output = normalize_tensor(output)
                    target = normalize_tensor(target)
                    
                    # Calculate loss with additional safety checks
                    try:
                        loss = self.criterion(output, target)
                        
                        # Check for extreme loss values
                        if torch.isnan(loss) or torch.isinf(loss) or loss > 1e6:
                            logging.warning(f"Extreme loss value {loss.item()} in chunk {i}, skipping")
                            continue
                            
                        # Scale loss for gradient accumulation
                        batch_size = self.model.params.batch_size
                        batch_loss = loss / batch_size
                        
                        # Use grad scaler if available
                        if self.scaler:
                            self.scaler.scale(batch_loss).backward()
                        else:
                            batch_loss.backward()
                        
                        # Track loss
                        accumulated_loss += loss.item()
                        samples_in_batch += 1
                        successful_chunks += 1
                        
                    except RuntimeError as e:
                        logging.warning(f"Loss calculation error for chunk {i}: {e}, skipping")
                        continue
                    
                    # Update parameters after accumulation steps
                    if samples_in_batch >= batch_size:
                        # Very aggressive gradient clipping for stability
                        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=0.1)
                        
                        # Step optimizer with grad scaler if available
                        if self.scaler:
                            self.scaler.step(self.optimizer)
                            self.scaler.update()
                        else:
                            self.optimizer.step()
                            
                        self.optimizer.zero_grad()
                        
                        # Update metrics
                        running_loss += accumulated_loss / samples_in_batch
                        batch_count += 1
                        
                        # Reset accumulation
                        accumulated_loss = 0.0
                        samples_in_batch = 0
                        
                        # Update progress bar statistics
                        pbar.set_postfix({
                            'loss': f"{running_loss/max(1, batch_count):.4f}", 
                            'success': f"{successful_chunks}/{processed_chunks}"
                        })
                    
                    # Log periodically
                    if batch_count > 0 and batch_count % 10 == 0:
                        avg_loss = running_loss / batch_count
                        logging.info(f"Epoch {epoch+1}, Batch {batch_count}, Loss: {avg_loss:.6f}")
                
                except RuntimeError as e:
                    if "stack expects" in str(e) or "size mismatch" in str(e) or "dimension" in str(e):
                        logging.warning(f"Tensor dimension mismatch in chunk {i}: {str(e)}, skipping")
                        continue
                    else:
                        raise e
                
            except Exception as e:
                logging.error(f"Error processing chunk {i}: {e}")
                continue
        
        # Make sure to update with any remaining samples
        if samples_in_batch > 0:
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=0.1)
            
            # Step optimizer with grad scaler if available
            if self.scaler:
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                self.optimizer.step()
                
            self.optimizer.zero_grad()
            
            # Update metrics
            running_loss += accumulated_loss / samples_in_batch
            batch_count += 1
        
        pbar.close()
        
        # Calculate epoch average loss
        avg_epoch_loss = running_loss / max(1, batch_count)
        logging.info(f"Epoch {epoch+1} completed. Average loss: {avg_epoch_loss:.6f}")
        logging.info(f"Processed {processed_chunks} chunks, {successful_chunks} were successful")
        
        # Update learning rate scheduler
        self.scheduler.step(avg_epoch_loss)
        
        return avg_epoch_loss
    
    def _check_early_stopping(self, epoch_loss):
        """Check if early stopping criteria is met"""
        if epoch_loss < self.stats['best_val_loss']:
            # New best model
            self.stats['best_val_loss'] = epoch_loss
            self.stats['patience_counter'] = 0
            self._save_checkpoint(is_best=True)
            return False
        else:
            # No improvement
            self.stats['patience_counter'] += 1
            if self.stats['patience_counter'] >= self.model.params.early_stopping_patience:
                return True
            return False
    
    def _save_checkpoint(self, epoch=None, is_best=False):
        """Save model checkpoint"""
        try:
            # Ensure output path has .pt extension
            output_path = self.output_path
            if not output_path.endswith('.pt'):
                output_path += '.pt'
                
            # Create checkpoint directory if it doesn't exist
            checkpoint_dir = os.path.dirname(output_path)
            if checkpoint_dir and not os.path.exists(checkpoint_dir):
                try:
                    os.makedirs(checkpoint_dir)
                    logging.info(f"Created directory: {checkpoint_dir}")
                except Exception as e:
                    logging.error(f"Failed to create directory {checkpoint_dir}: {e}")
                    # Continue anyway to attempt direct save
            
            # Determine checkpoint path
            if is_best:
                checkpoint_path = output_path.replace('.pt', '_best.pt')
                logging.info(f"Saving best model to {checkpoint_path}")
            elif epoch is not None:
                checkpoint_path = output_path.replace('.pt', f'_epoch_{epoch+1}.pt')
                logging.info(f"Saving checkpoint for epoch {epoch+1} to {checkpoint_path}")
            else:
                checkpoint_path = output_path
            
            # Try absolute path if relative path fails
            try:
                # Save model
                torch.save({
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'epoch': epoch,
                    'loss': self.stats['epoch_losses'][-1] if self.stats['epoch_losses'] else None,
                    'best_val_loss': self.stats['best_val_loss'],
                }, checkpoint_path)
                logging.info(f"Successfully saved checkpoint to {checkpoint_path}")
            except Exception as e:
                # Try with absolute path in case of WSL path issues
                abs_path = os.path.abspath(checkpoint_path)
                logging.warning(f"Failed to save to {checkpoint_path}, trying absolute path: {abs_path}")
                torch.save({
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'epoch': epoch,
                    'loss': self.stats['epoch_losses'][-1] if self.stats['epoch_losses'] else None,
                    'best_val_loss': self.stats['best_val_loss'],
                }, abs_path)
                
        except Exception as e:
            logging.error(f"Failed to save checkpoint: {e}")
            
    def _save_final_model(self):
        """Save the final model after training"""
        try:
            # Ensure output path has .pt extension
            if not self.output_path.endswith('.pt'):
                output_path = self.output_path + '.pt'
            else:
                output_path = self.output_path
                
            # Save complete model
            final_path = output_path.replace('.pt', '_final.pt')
            
            # Try to save with error handling
            try:
                torch.save(self.model.state_dict(), final_path)
                logging.info(f"Final model saved to: {final_path}")
                
                # Save optimizer state and training stats
                meta_path = output_path.replace('.pt', '_meta.json')
                with open(meta_path, 'w') as f:
                    json.dump({
                        'epoch_losses': self.stats['epoch_losses'],
                        'val_losses': self.stats['val_losses'],
                        'best_val_loss': self.stats['best_val_loss'],
                        'num_epochs_trained': len(self.stats['epoch_losses']),
                        'early_stopped': self.stats['patience_counter'] >= self.model.params.early_stopping_patience,
                    }, f, indent=2)
                    
                logging.info(f"Training metadata saved to: {meta_path}")
                
            except Exception as e:
                # Try with absolute path as a fallback
                abs_final_path = os.path.abspath(final_path)
                logging.warning(f"Failed direct save, trying absolute path: {abs_final_path}")
                torch.save(self.model.state_dict(), abs_final_path)
                logging.info(f"Final model saved to absolute path: {abs_final_path}")
                
        except Exception as e:
            logging.error(f"Failed to save final model: {e}")
            
            # Try alternate location as fallback
            try:
                # Use current working directory with more explicit name
                fallback_path = os.path.join(os.getcwd(), "cellai_model_final.pt")
                torch.save(self.model.state_dict(), fallback_path)
                logging.info(f"Final model saved to alternate location: {fallback_path}")
            except Exception as e2:
                logging.error(f"Failed to save to alternate location: {e2}")


class BenchmarkManager:
    """
    Manager for benchmarking the CellAI model on test data
    """
    def __init__(self, model, test_data_path, device=None):
        self.model = model
        self.test_data_path = test_data_path
        
        # Initialize device
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Using device: {self.device}")
        
        # Move model to device
        self.model = self.model.to(self.device)
    
    def run_benchmark(self):
        """Run the benchmark and return metrics"""
        self.model.eval()
        metrics = {
            'total_samples': 0,
            'processing_times': [],
            'encoding_times': [],
            'inference_times': [],
            'sample_sizes': [],
            'error_count': 0
        }
        
        # Create data iterator
        dataset = DatasetIterator(
            self.test_data_path, 
            chunk_size=self.model.params.chunk_size,
            overlap=self.model.params.overlap
        )
        
        # Process each sample
        for i, chunk_bytes in enumerate(tqdm(dataset, desc="Benchmarking")):
            try:
                # Skip empty chunks
                if not chunk_bytes or len(chunk_bytes) < 10:
                    continue
                    
                # Record sample size
                metrics['sample_sizes'].append(len(chunk_bytes))
                
                # Benchmark encoding time
                start_time = time.time()
                with torch.no_grad():
                    encoded_features = self.model.encoder.encode(chunk_bytes)
                encoding_time = time.time() - start_time
                metrics['encoding_times'].append(encoding_time)
                
                # Benchmark inference time
                start_time = time.time()
                with torch.no_grad():
                    output = self.model(chunk_bytes)
                inference_time = time.time() - start_time
                metrics['inference_times'].append(inference_time)
                
                # Total processing time
                metrics['processing_times'].append(encoding_time + inference_time)
                metrics['total_samples'] += 1
                
            except Exception as e:
                logging.error(f"Error benchmarking sample {i}: {e}")
                metrics['error_count'] += 1
        
        # Calculate summary statistics
        metrics['avg_processing_time'] = np.mean(metrics['processing_times']) if metrics['processing_times'] else 0
        metrics['avg_encoding_time'] = np.mean(metrics['encoding_times']) if metrics['encoding_times'] else 0
        metrics['avg_inference_time'] = np.mean(metrics['inference_times']) if metrics['inference_times'] else 0
        metrics['max_processing_time'] = np.max(metrics['processing_times']) if metrics['processing_times'] else 0
        metrics['min_processing_time'] = np.min(metrics['processing_times']) if metrics['processing_times'] else 0
        metrics['avg_sample_size'] = np.mean(metrics['sample_sizes']) if metrics['sample_sizes'] else 0
        metrics['throughput'] = (metrics['total_samples'] / 
                               sum(metrics['processing_times'])) if metrics['processing_times'] else 0
        
        return metrics


def chat_mode(model):
    """
    Interactive chat mode for the CellAI Binary model
    """
    logging.info("Starting chat mode. Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            # Process input as bytes
            input_bytes = user_input.encode('utf-8')
            
            # Get model response
            start_time = time.time()
            with torch.no_grad():
                # Extract features
                encoded_features = model.encoder.encode(input_bytes)
                features_tensor = torch.tensor(encoded_features, dtype=torch.float32)
                
                # Process through model
                output = model(input_bytes)
                
                # Get top activations
                top_indices = torch.topk(output, 5).indices.cpu().numpy()
                
            # Compute processing time
            proc_time = time.time() - start_time
            
            # Prepare response
            response = f"Model response: {output[:10].tolist()}\n"
            response += f"Top activations: {top_indices.tolist()}\n"
            response += f"Features extracted: {len(encoded_features)}\n"
            response += f"Processing time: {proc_time:.4f} seconds"
            
            print(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            print(f"Error processing input: {e}")
    
    logging.info("Chat mode terminated")


def load_model_with_buffer_handling(model, checkpoint_path):
    """
    Load model state dict with special handling for buffer size mismatches.
    
    Args:
        model: The model to load parameters into
        checkpoint_path: Path to the checkpoint file
        
    Returns:
        The loaded model
    """
    try:
        # Load checkpoint
        checkpoint = torch.load(checkpoint_path, map_location='cpu')
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        else:
            state_dict = checkpoint
            
        # Create new state dict without problematic buffer tensors
        filtered_state_dict = {}
        for name, param in state_dict.items():
            # Skip buffers with dynamic sizes that cause loading issues
            if ('memory_kernel.state_history' in name or 
                'memory_kernel.time_points' in name):
                logging.info(f"Skipping dynamic buffer: {name}")
                continue
                
            filtered_state_dict[name] = param
            
        # Load the filtered state dict
        model.load_state_dict(filtered_state_dict, strict=False)
        
        # Reinitialize any buffers that were skipped
        for name, buffer in model.named_buffers():
            if ('memory_kernel.state_history' in name or 
                'memory_kernel.time_points' in name):
                # These will be reinitialized during the first forward pass
                pass
                
        logging.info("Model loaded successfully with buffer handling")
        return model
        
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise


def main():
    """Command-line interface for CellAI Binary Enhanced"""
    parser = argparse.ArgumentParser(description='CellAI Binary Enhanced - Binary Stream Cellular Model')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process a binary file')
    process_parser.add_argument('--input', required=True, help='Input file path')
    process_parser.add_argument('--output', required=True, help='Output file path')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train the model')
    train_parser.add_argument('--data', required=True, help='Data folder path')
    train_parser.add_argument('--epochs', type=int, default=3, help='Number of epochs')
    train_parser.add_argument('--output', default='model.pt', help='Output model path')
    train_parser.add_argument('--batch-size', type=int, default=4, help='Batch size for training')
    train_parser.add_argument('--learning-rate', type=float, default=1e-6, help='Learning rate')
    train_parser.add_argument('--debug', action='store_true', help='Enable debug mode with extra checks')
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Benchmark the model')
    benchmark_parser.add_argument('--model', required=True, help='Model file path')
    benchmark_parser.add_argument('--test', required=True, help='Test folder path')
    benchmark_parser.add_argument('--output-json', help='Path to save benchmark results as JSON')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Interactive chat mode')
    chat_parser.add_argument('--model', required=True, help='Model file path')
    
    args = parser.parse_args()
    
    # Initialize model
    model_params = create_default_model_params()
    
    # Update parameters if specified
    if hasattr(args, 'batch_size') and args.batch_size:
        model_params.batch_size = args.batch_size
    
    if hasattr(args, 'learning_rate') and args.learning_rate:
        model_params.learning_rate = args.learning_rate
    
    # Create model with updated parameters
    model = CellAIBinaryModel(model_params)
    
    # Enable debug mode if requested
    if hasattr(args, 'debug') and args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        torch.autograd.set_detect_anomaly(True)
        logging.info("Debug mode enabled with autograd anomaly detection")
    
    if args.command == 'process':
        logging.info(f"Processing file: {args.input}")
        features = model.encoder.encode_file(args.input)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save features to output file
        np.save(args.output, features)
        logging.info(f"Features saved to: {args.output}")
        
    elif args.command == 'train':
        logging.info(f"Training model on data from: {args.data}")
        
        # Add pre-training check
        logging.info("Performing pre-training weight check...")
        for name, param in model.named_parameters():
            if torch.isnan(param.data).any() or torch.isinf(param.data).any():
                logging.warning(f"Parameter {name} contains NaN or Inf values before training starts - reinitializing")
                if "weight" in name:
                    nn.init.xavier_normal_(param.data)
                else:
                    nn.init.zeros_(param.data)
                
        # Setup training manager
        trainer = TrainingManager(
            model=model,
            data_path=args.data,
            output_path=args.output,
            num_epochs=args.epochs
        )
        
        # Run training
        trainer.train()
        
    elif args.command == 'benchmark':
        logging.info(f"Loading model from: {args.model}")
        
        # Load model weights with buffer handling
        try:
            load_model_with_buffer_handling(model, args.model)
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return
        
        logging.info(f"Benchmarking on data from: {args.test}")
        
        # Run benchmark
        benchmark = BenchmarkManager(model, args.test)
        metrics = benchmark.run_benchmark()
        
        # Print results
        logging.info("Benchmark Results:")
        logging.info(f"Total samples processed: {metrics['total_samples']}")
        logging.info(f"Average processing time: {metrics['avg_processing_time']:.6f} seconds")
        logging.info(f"  - Encoding time: {metrics['avg_encoding_time']:.6f} seconds")
        logging.info(f"  - Inference time: {metrics['avg_inference_time']:.6f} seconds")
        logging.info(f"Average sample size: {metrics['avg_sample_size']:.1f} bytes")
        logging.info(f"Throughput: {metrics['throughput']:.2f} samples/second")
        logging.info(f"Error count: {metrics['error_count']}")
        
        # Save to JSON if requested
        if args.output_json:
            try:
                with open(args.output_json, 'w') as f:
                    json.dump(metrics, f, indent=4)
                logging.info(f"Benchmark results saved to {args.output_json}")
            except Exception as e:
                logging.error(f"Error saving benchmark results: {e}")
        
    elif args.command == 'chat':
        logging.info(f"Loading model from: {args.model}")
        
        # Load model weights with buffer handling
        try:
            load_model_with_buffer_handling(model, args.model)
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return
        
        # Start chat mode
        chat_mode(model)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()