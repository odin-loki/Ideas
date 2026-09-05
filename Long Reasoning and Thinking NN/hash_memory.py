"""
Hash Memory System Implementation
Implements locality-sensitive hashing for memory storage and retrieval.
"""

import numpy as np
from collections import defaultdict
from typing import List, Tuple, Dict, Optional
import hashlib


class LSHHasher:
    """Locality-Sensitive Hashing using random hyperplanes."""
    
    def __init__(self, input_dim: int, hash_bits: int = 64):
        """
        Args:
            input_dim: Dimension of input vectors
            hash_bits: Number of hash bits (controls collision rate)
        """
        self.input_dim = input_dim
        self.hash_bits = hash_bits
        
        # Random hyperplanes for hashing
        # Each row is a random hyperplane normal vector
        self.hyperplanes = np.random.randn(hash_bits, input_dim)
        self.hyperplanes /= np.linalg.norm(self.hyperplanes, axis=1, keepdims=True)
    
    def hash(self, vector: np.ndarray) -> int:
        """
        Compute LSH hash of a vector.
        
        Args:
            vector: [input_dim] vector to hash
            
        Returns:
            Integer hash value (from binary representation)
        """
        # Project onto hyperplanes and take sign
        projections = self.hyperplanes @ vector  # [hash_bits]
        binary_hash = (projections > 0).astype(int)  # [hash_bits]
        
        # Convert binary to integer
        hash_value = int(''.join(map(str, binary_hash)), 2)
        return hash_value
    
    def hash_to_binary(self, hash_value: int) -> np.ndarray:
        """Convert integer hash back to binary array."""
        binary_str = format(hash_value, f'0{self.hash_bits}b')
        return np.array([int(b) for b in binary_str])
    
    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """Compute Hamming distance between two hashes."""
        binary1 = self.hash_to_binary(hash1)
        binary2 = self.hash_to_binary(hash2)
        return np.sum(binary1 != binary2)


class MemorySegment:
    """A single segment of memory with signature."""
    
    def __init__(self, 
                 tokens: np.ndarray,
                 embeddings: np.ndarray,
                 segment_id: int):
        """
        Args:
            tokens: [segment_size] token IDs
            embeddings: [segment_size, embedding_dim] token embeddings
            segment_id: Unique identifier
        """
        self.tokens = tokens
        self.embeddings = embeddings
        self.segment_id = segment_id
        
        # Compute signature
        self.centroid = embeddings.mean(axis=0)  # [embedding_dim]
        self.spread = np.mean(np.linalg.norm(embeddings - self.centroid, axis=1)**2)
        self.hash_value = None  # Set by hash table
        
    def __repr__(self):
        return f"Segment(id={self.segment_id}, size={len(self.tokens)}, spread={self.spread:.3f})"


class HashMemoryBank:
    """Memory bank using LSH for storage and retrieval."""
    
    def __init__(self,
                 embedding_dim: int,
                 compressed_dim: int = 512,
                 hash_bits: int = 64,
                 segment_size: int = 100,
                 probe_buckets: int = 8):
        """
        Args:
            embedding_dim: Full embedding dimension
            compressed_dim: Compressed centroid dimension
            hash_bits: Number of LSH bits
            segment_size: Tokens per segment
            probe_buckets: Nearest buckets to probe when the Hamming
                threshold matches none
        """
        self.embedding_dim = embedding_dim
        self.compressed_dim = compressed_dim
        self.hash_bits = hash_bits
        self.segment_size = segment_size
        self.probe_buckets = probe_buckets
        
        # LSH hasher (operates on compressed centroids)
        self.hasher = LSHHasher(compressed_dim, hash_bits)
        
        # Hash table: hash_value -> List[MemorySegment]
        self.hash_table = defaultdict(list)
        
        # Compression matrix (simple random projection)
        self.compression_matrix = np.random.randn(compressed_dim, embedding_dim)
        self.compression_matrix /= np.linalg.norm(self.compression_matrix, axis=1, keepdims=True)
        
        self.num_segments = 0
    
    def compress(self, vector: np.ndarray) -> np.ndarray:
        """Compress full embedding to lower dimension."""
        return self.compression_matrix @ vector
    
    def insert_segment(self, segment: MemorySegment):
        """Insert a memory segment into the hash table."""
        # Compress centroid
        compressed_centroid = self.compress(segment.centroid)
        
        # Compute hash
        hash_value = self.hasher.hash(compressed_centroid)
        segment.hash_value = hash_value
        
        # Store in hash table
        self.hash_table[hash_value].append(segment)
        self.num_segments += 1
    
    def build_from_sequence(self, tokens: np.ndarray, embeddings: np.ndarray):
        """
        Build memory bank from a token sequence.
        
        Args:
            tokens: [num_tokens] token IDs
            embeddings: [num_tokens, embedding_dim] embeddings
        """
        num_tokens = len(tokens)
        segment_id = 0
        
        # Create non-overlapping segments
        for i in range(0, num_tokens, self.segment_size):
            end = min(i + self.segment_size, num_tokens)
            segment_tokens = tokens[i:end]
            segment_embeddings = embeddings[i:end]
            
            if len(segment_tokens) < self.segment_size // 2:
                # Skip very short segments at end
                continue
            
            segment = MemorySegment(segment_tokens, segment_embeddings, segment_id)
            self.insert_segment(segment)
            segment_id += 1
        
        print(f"Built memory bank: {self.num_segments} segments, "
              f"{len(self.hash_table)} unique hash buckets")
    
    def retrieve_candidates(self,
                           query_embedding: np.ndarray,
                           hamming_threshold: int = 3,
                           max_candidates: int = 1000) -> List[MemorySegment]:
        """
        Retrieve candidate segments within Hamming threshold.
        
        Args:
            query_embedding: [embedding_dim] query vector
            hamming_threshold: Max Hamming distance for candidates
            max_candidates: Maximum number of candidates to return
            
        Returns:
            List of candidate segments
        """
        # Compress and hash query
        compressed_query = self.compress(query_embedding)
        query_hash = self.hasher.hash(compressed_query)
        
        # Rank every bucket by Hamming distance, then take those inside the
        # threshold.
        distances = [(self.hasher.hamming_distance(query_hash, h), h)
                     for h in self.hash_table]
        near = [h for d, h in distances if d <= hamming_threshold]

        # A threshold of 3 is unreachable for a 64-bit hash: two random
        # signatures sit ~32 bits apart, and even genuinely similar ones land
        # around 20. Taken literally this returned nothing for every query,
        # which left the inference loop with no observations at all. Fall back
        # to multi-probe - the nearest buckets, whatever their distance - so
        # the threshold stays a fast path rather than a wall.
        if not near:
            distances.sort(key=lambda t: t[0])
            near = [h for _, h in distances[:self.probe_buckets]]

        candidates = []
        for hash_value in near:
            candidates.extend(self.hash_table[hash_value])
        
        # Limit number of candidates
        if len(candidates) > max_candidates:
            candidates = candidates[:max_candidates]
        
        return candidates
    
    def compute_similarity(self,
                          query_embedding: np.ndarray,
                          segment: MemorySegment) -> float:
        """
        Compute similarity score between query and segment.
        
        Uses cosine similarity of centroids.
        """
        query_norm = np.linalg.norm(query_embedding)
        centroid_norm = np.linalg.norm(segment.centroid)
        
        if query_norm == 0 or centroid_norm == 0:
            return 0.0
        
        cosine_sim = np.dot(query_embedding, segment.centroid) / (query_norm * centroid_norm)
        return cosine_sim
    
    def retrieve_top_k(self,
                      query_embedding: np.ndarray,
                      k: int = 10,
                      hamming_threshold: int = 3) -> List[Tuple[MemorySegment, float]]:
        """
        Retrieve top-k most similar segments.
        
        Returns:
            List of (segment, similarity_score) tuples, sorted by score
        """
        # Get candidates
        candidates = self.retrieve_candidates(query_embedding, hamming_threshold)
        
        if not candidates:
            return []
        
        # Score all candidates
        scored = []
        for segment in candidates:
            score = self.compute_similarity(query_embedding, segment)
            scored.append((segment, score))
        
        # Sort by score and take top-k
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]
    
    def get_statistics(self) -> Dict:
        """Get memory bank statistics."""
        bucket_sizes = [len(segments) for segments in self.hash_table.values()]
        
        return {
            'num_segments': self.num_segments,
            'num_buckets': len(self.hash_table),
            'avg_bucket_size': np.mean(bucket_sizes) if bucket_sizes else 0,
            'max_bucket_size': max(bucket_sizes) if bucket_sizes else 0,
            'load_factor': self.num_segments / len(self.hash_table) if self.hash_table else 0,
            'expected_collisions': self.num_segments**2 / (2 * 2**self.hash_bits)
        }


class HierarchicalHashMemory:
    """Multi-level hash memory with different granularities."""
    
    def __init__(self,
                 embedding_dim: int,
                 compressed_dim: int = 512,
                 segment_sizes: List[int] = [100, 1000, 10000]):
        """
        Args:
            embedding_dim: Full embedding dimension
            compressed_dim: Compressed dimension
            segment_sizes: Segment sizes for each level (fine to coarse)
        """
        self.embedding_dim = embedding_dim
        self.compressed_dim = compressed_dim
        self.segment_sizes = segment_sizes
        self.num_levels = len(segment_sizes)
        
        # Create memory bank for each level
        self.memory_banks = [
            HashMemoryBank(embedding_dim, compressed_dim, segment_size=s)
            for s in segment_sizes
        ]
    
    def build_from_sequence(self, tokens: np.ndarray, embeddings: np.ndarray):
        """Build all hierarchical levels from sequence."""
        for level, bank in enumerate(self.memory_banks):
            print(f"\nBuilding level {level} (segment_size={self.segment_sizes[level]})...")
            bank.build_from_sequence(tokens, embeddings)
    
    def retrieve_hierarchical(self,
                            query_embedding: np.ndarray,
                            k_per_level: List[int] = [50, 20, 10]) -> List[List[Tuple[MemorySegment, float]]]:
        """
        Retrieve from all hierarchical levels.
        
        Returns:
            List of retrieved segments for each level
        """
        results = []
        for level, bank in enumerate(self.memory_banks):
            k = k_per_level[level] if level < len(k_per_level) else 10
            retrieved = bank.retrieve_top_k(query_embedding, k=k)
            results.append(retrieved)
        return results
    
    def get_all_statistics(self) -> List[Dict]:
        """Get statistics for all levels."""
        return [bank.get_statistics() for bank in self.memory_banks]


if __name__ == "__main__":
    # Test the hash memory system
    print("Testing Hash Memory System\n")
    
    # Create synthetic data
    num_tokens = 10000
    embedding_dim = 128
    
    tokens = np.arange(num_tokens)
    # Create embeddings with some structure (clusters)
    embeddings = np.random.randn(num_tokens, embedding_dim)
    
    # Add cluster structure
    for i in range(0, num_tokens, 500):
        cluster_center = np.random.randn(embedding_dim) * 3
        embeddings[i:i+500] += cluster_center
    
    # Build memory bank
    memory = HashMemoryBank(embedding_dim, compressed_dim=64, segment_size=100)
    memory.build_from_sequence(tokens, embeddings)
    
    # Show statistics
    stats = memory.get_statistics()
    print("\nMemory Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}")
    
    # Test retrieval
    query = embeddings[550]  # Should be similar to tokens 500-599
    print(f"\nQuery: embedding at position 550")
    
    results = memory.retrieve_top_k(query, k=5)
    print(f"\nTop-5 retrieved segments:")
    for segment, score in results:
        token_range = f"{segment.tokens[0]}-{segment.tokens[-1]}"
        print(f"  Segment {segment.segment_id} (tokens {token_range}): similarity={score:.3f}")
    
    # Test hierarchical memory
    print("\n" + "="*60)
    print("Testing Hierarchical Memory\n")
    
    hierarchical = HierarchicalHashMemory(embedding_dim, compressed_dim=64)
    hierarchical.build_from_sequence(tokens, embeddings)
    
    print("\nHierarchical Statistics:")
    for level, stats in enumerate(hierarchical.get_all_statistics()):
        print(f"\nLevel {level} (segment_size={hierarchical.segment_sizes[level]}):")
        for key, value in stats.items():
            print(f"  {key}: {value:.2f}")
