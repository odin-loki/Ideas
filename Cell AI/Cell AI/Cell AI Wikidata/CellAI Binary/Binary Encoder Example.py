import numpy as np
import pywt
from collections import deque, Counter, defaultdict
import xxhash
from scipy.fftpack import fft
from scipy.stats import entropy, skew, kurtosis, rankdata
import struct
import array
import concurrent.futures
from sklearn.random_projection import GaussianRandomProjection
from sklearn.decomposition import TruncatedSVD
import mmh3
import zlib

class CellularBinaryEncoder:
    """
    Unified Cellular Binary Encoder (UCBE)
    
    A comprehensive feature extractor combining cellular memory dynamics, multi-scale analysis,
    dictionary encoding, wavelet transforms, and spectral analysis for any binary data.
    Designed to work with any AI system, with special optimization for Cell AI architectures.
    """
    
    def __init__(self):
        """Initialize the encoder with optimized parameters"""
        # Content-defined chunking parameters
        self.min_chunk_size = 512        # Minimum bytes per chunk
        self.max_chunk_size = 8192       # Maximum bytes per chunk
        self.window_size = 16            # Rolling hash window
        self.boundary_mask = 0x0FFF      # Boundary condition (when hash & mask == 0)
        
        # Multi-scale analysis parameters
        self.scales = [1.0, 0.5, 0.25, 0.125]  # Analysis at 100%, 50%, 25%, 12.5%
        
        # Wavelet transform parameters
        self.wavelet = 'db4'             # Daubechies-4 wavelet
        self.wavelet_levels = 4          # Decomposition levels
        
        # Cellular memory dynamics parameters
        self.dt = 0.1                    # Time step for memory dynamics
        self.D = 0.2                     # Diffusion coefficient
        self.gamma = 0.1                 # Decay rate
        self.eta = 0.01                  # Noise amplitude
        
        # Feature selection parameters
        self.selection_threshold = 0.3   # Keep top 30% of features
        
        # N-gram parameters
        self.ngram_sizes = [2, 3, 4]     # Extract 2-grams, 3-grams, and 4-grams
        self.top_ngrams = 50             # Number of top n-grams to keep per size
        
        # DAMR (Dynamic Adaptive Multi-scale Reservoir) parameters
        self.reservoir_size = 256        # Size of each reservoir
        self.num_reservoirs = 3          # Number of reservoirs at different scales
        self.influence_radius = [2, 4, 8]  # Neighbor influence radius per reservoir
        self.influence_strength = [0.1, 0.08, 0.06]  # Strength of neighbor influence
        
        # Adaptive dictionary parameters
        self.dict_max_size = 4096        # Maximum dictionary size
        self.dict_min_freq = 2           # Minimum frequency for dictionary entries
        
        # LSH parameters for fast similarity search
        self.lsh_num_hashes = 10         # Number of hash functions
        self.lsh_bands = 5               # Number of bands for LSH
        
        # Dimensionality reduction parameters
        self.pca_components = 64         # Number of SVD components
        self.random_proj_components = 128  # Number of random projection components
        
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
        
        return np.array(selected_features, dtype=np.float32)
    
    def _content_defined_chunking(self, data):
        """
        Divide data into chunks based on content boundaries rather than fixed sizes
        Uses rolling hash to find natural boundaries in the data
        """
        chunks = []
        data_len = len(data)
        
        # Return whole data if smaller than minimum chunk size
        if data_len <= self.min_chunk_size:
            return [data]
        
        i = 0
        while i < data_len:
            # Ensure minimum chunk size
            if i + self.min_chunk_size >= data_len:
                chunks.append(data[i:])
                break
            
            # Find content-defined boundary
            boundary = self._find_boundary(data, i + self.min_chunk_size, 
                                         min(i + self.max_chunk_size, data_len))
            
            # If no boundary found, use maximum chunk size
            if boundary == -1:
                boundary = min(i + self.max_chunk_size, data_len)
            
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
        
        # Use fast rolling hash
        h = xxhash.xxh64()
        
        for i in range(start, end - self.window_size + 1):
            window = data[i:i+self.window_size]
            h.update(window)
            if (h.intdigest() & self.boundary_mask) == 0:
                return i + self.window_size
            h.reset()
        
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
            if count >= self.dict_min_freq:
                # Only keep patterns that appear multiple times
                pattern_hash = xxhash.xxh64(pattern).intdigest()
                self.dictionary[pattern_hash] = (pattern, count)
                
                # Limit dictionary size
                if len(self.dictionary) >= self.dict_max_size:
                    break
    
    def _process_chunk(self, chunk):
        """
        Process a single chunk to extract features using multiple techniques
        """
        features = {}
        
        # Convert to numpy array of bytes for faster processing
        data = np.frombuffer(chunk, dtype=np.uint8)
        
        # 1. Multi-scale analysis
        for scale_idx, scale in enumerate(self.scales):
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
            if len(scaled_data) >= max(self.ngram_sizes):
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
        if len(data) < 2**self.wavelet_levels:
            return features
        
        try:
            # Perform wavelet decomposition
            coeffs = pywt.wavedec(data, self.wavelet, level=min(self.wavelet_levels, 
                                                              pywt.dwt_max_level(len(data), self.wavelet)))
            
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
        
        for n in self.ngram_sizes:
            # Skip if data is too small for this n-gram size
            if len(data) < n:
                continue
            
            # Extract n-grams
            ngrams = [bytes(data[i:i+n]) for i in range(len(data) - n + 1)]
            
            # Count n-gram frequencies
            ngram_counts = Counter(ngrams)
            
            # Get top n-grams
            top_ngrams = ngram_counts.most_common(self.top_ngrams)
            
            # Convert to features
            for i, (ngram, count) in enumerate(top_ngrams):
                if i >= self.top_ngrams:
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
        state = np.zeros(min(256, len(data)))
        memory = np.zeros_like(state)
        
        # Process data through cellular dynamics equations
        for t, byte in enumerate(data):
            # Update state based on cellular equation
            # Simplified version of: dS/dt = f(I, S, t) - γS + D∇²S + η(t)
            
            # Input influence
            input_term = np.zeros_like(state)
            input_term[byte % len(state)] = 1.0
            
            # Diffusion term (simplified ∇²S as difference with neighbors)
            diffusion = np.zeros_like(state)
            for i in range(len(state)):
                neighbors = [(i-1) % len(state), (i+1) % len(state)]
                neighbor_avg = np.mean([state[j] for j in neighbors])
                diffusion[i] = self.D * (neighbor_avg - state[i])
            
            # Decay term
            decay = -self.gamma * state
            
            # Noise term
            noise = self.eta * np.random.randn(len(state))
            
            # Update state with all terms
            dstate = input_term + diffusion + decay + noise
            state = state + self.dt * dstate
            
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
            features[f"cellular_top_{i}"] = float(idx) / 255.0
            features[f"cellular_top_{i}_value"] = float(state[idx])
        
        return features
    
    def _extract_reservoir_features(self, data):
        """
        Extract features using dynamic reservoir computing approach (DAMR)
        """
        features = {}
        
        # Initialize reservoirs (one per scale)
        reservoirs = [np.zeros(self.reservoir_size) for _ in range(self.num_reservoirs)]
        
        # Pre-calculate neighbor indices
        neighbor_indices = {}
        for b in range(256):
            neighbors = {}
            for r in range(max(self.influence_radius)):
                if r < 1:
                    continue
                neighbors[r] = [(b - r) % 256, (b + r) % 256]
            neighbor_indices[b] = neighbors
        
        # Sliding window for context-aware updates
        window_size = min(8, len(data))
        window = deque(maxlen=window_size)
        
        # Process each byte through the reservoirs
        for byte in data:
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
                radius = self.influence_radius[r_idx]
                strength = self.influence_strength[r_idx] * context_boost
                
                for j in range(1, radius + 1):
                    if j not in neighbor_indices[byte]:
                        continue
                        
                    neighbors = neighbor_indices[byte][j]
                    decay_factor = strength / j
                    
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
                features[f"lfs_window_{i}_mean"] = float(np.mean(window))
                features[f"lfs_window_{i}_std"] = float(np.std(window))
                features[f"lfs_window_{i}_entropy"] = float(entropy(np.bincount(window) + 1e-10))
                features[f"lfs_window_{i}_position"] = float(idx) / max(1, len(windows))
        
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
        for seed in range(self.lsh_num_hashes):
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
            svd = TruncatedSVD(n_components=min(self.pca_components, len(feature_vector)-1))
            svd_transformed = svd.fit_transform(feature_vector.reshape(1, -1))[0]
            
            for i, val in enumerate(svd_transformed):
                reduced_features[f"svd_{i}"] = float(val)
                
            # Apply random projection for better distance preservation
            rp = GaussianRandomProjection(n_components=min(self.random_proj_components, len(feature_vector)))
            rp_transformed = rp.fit_transform(feature_vector.reshape(1, -1))[0]
            
            for i, val in enumerate(rp_transformed):
                reduced_features[f"rp_{i}"] = float(val)
                
        except Exception:
            # Fallback if dimensionality reduction fails
            # Just return a subset of original features
            for i, k in enumerate(feature_keys[:200]):  # Limit to first 200 features
                reduced_features[k] = features[k]
        
        return reduced_features
    
    def _combine_chunk_features(self, feature_sets):
        """
        Combine features from multiple chunks into a single feature set
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
    
    def _select_top_features(self, features, max_features):
        """
        Select the most important features based on importance scores
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
        num_to_keep = min(max_features, int(len(sorted_features) * self.selection_threshold))
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

# Example usage:
def encode_file(file_path, max_features=2000):
    """Encode a file using the cellular binary encoder"""
    encoder = CellularBinaryEncoder()
    
    with open(file_path, 'rb') as f:
        features = encoder.encode(f, max_features=max_features)
    
    return features

# Example usage with a binary stream:
def encode_bytes(binary_data, max_features=2000):
    """Encode bytes using the cellular binary encoder"""
    encoder = CellularBinaryEncoder()
    features = encoder.encode(binary_data, max_features=max_features)
    return features