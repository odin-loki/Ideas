"""
Unified Hash-Predictive Memory System
Combines LSH memory with hierarchical predictive coding through single free energy.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from hash_memory import HierarchicalHashMemory, MemorySegment
from predictive_coding import HierarchicalPredictiveCoding


class UnifiedHashPredictiveMemory:
    """
    Unified system combining hash memory and predictive coding.
    
    Key innovation: Single free energy functional creates bidirectional feedback:
    - Inference states → predict which memories to retrieve (hash weighting)
    - Retrieved memories → constrain inference states (hash coupling)
    """
    
    def __init__(self,
                 embedding_dim: int,
                 compressed_dim: int = 512,
                 segment_sizes: List[int] = [100, 1000, 10000],
                 learning_rate: float = 0.1,
                 lambda_sparse: float = 0.1):
        """
        Args:
            embedding_dim: Full embedding dimension
            compressed_dim: Compressed dimension for hash
            segment_sizes: Segment sizes for hierarchical levels
            learning_rate: Learning rate for state updates
            lambda_sparse: Sparsity regularization for bucket weights
        """
        self.embedding_dim = embedding_dim
        self.compressed_dim = compressed_dim
        self.segment_sizes = segment_sizes
        self.num_levels = len(segment_sizes)
        self.lambda_sparse = lambda_sparse
        
        # Hash memory system
        self.hash_memory = HierarchicalHashMemory(
            embedding_dim,
            compressed_dim,
            segment_sizes
        )
        
        # Predictive coding system
        # Layers: one per hierarchical level
        self.predictive_coding = HierarchicalPredictiveCoding(
            layer_dims=[embedding_dim] * self.num_levels,
            learning_rate=learning_rate,
            precisions=[1.0, 0.5, 0.2]  # Decreasing precision up hierarchy
        )
        
        # Bucket weights for each level (managed during inference)
        self.bucket_weights = [None] * self.num_levels
        self.retrieved_segments = [None] * self.num_levels
    
    def build_memory(self, tokens: np.ndarray, embeddings: np.ndarray):
        """Build hash memory from token sequence."""
        print("Building hierarchical hash memory...")
        self.hash_memory.build_from_sequence(tokens, embeddings)
        
        stats = self.hash_memory.get_all_statistics()
        print("\nMemory Statistics:")
        for level, stat in enumerate(stats):
            print(f"  Level {level}: {stat['num_segments']} segments, "
                  f"{stat['num_buckets']} buckets, "
                  f"load_factor={stat['load_factor']:.2f}")
    
    def compute_bucket_weights(self,
                               level: int,
                               candidates: List[Tuple[MemorySegment, float]],
                               prediction: np.ndarray) -> np.ndarray:
        """
        Compute weights for candidate buckets based on prediction error.
        
        This implements: w_i ∝ exp(-||retrieved_i - prediction||² / λ)
        
        Args:
            level: Hierarchical level
            candidates: List of (segment, initial_score) tuples
            prediction: Current prediction from state
            
        Returns:
            Normalized weights for each candidate
        """
        if not candidates:
            return np.array([])
        
        # Compute error for each candidate
        errors = []
        for segment, _ in candidates:
            error = np.linalg.norm(segment.centroid - prediction)**2
            errors.append(error)
        
        errors = np.array(errors)
        
        # Softmax with temperature = lambda_sparse
        weights = np.exp(-errors / self.lambda_sparse)
        weights /= weights.sum()
        
        return weights
    
    def retrieve_weighted_memory(self,
                                level: int,
                                candidates: List[Tuple[MemorySegment, float]],
                                weights: np.ndarray) -> np.ndarray:
        """
        Compute weighted average of retrieved memories.
        
        Returns:
            Weighted memory vector
        """
        if not candidates or len(weights) == 0:
            return np.zeros(self.embedding_dim)
        
        # Weighted sum of centroids
        weighted_memory = np.zeros(self.embedding_dim)
        for (segment, _), weight in zip(candidates, weights):
            weighted_memory += weight * segment.centroid
        
        return weighted_memory
    
    def compute_hash_coupling_terms(self,
                                   current_states: List[np.ndarray]) -> List[np.ndarray]:
        """
        Compute hash coupling terms for free energy.
        
        This implements the F_coupling part:
        coupling = Σ_i w_i · ∇_s ||retrieved_i - g(s)||²
        
        Returns:
            Coupling gradient for each level
        """
        couplings = []
        
        for level in range(self.num_levels):
            if self.bucket_weights[level] is None or self.retrieved_segments[level] is None:
                couplings.append(np.zeros(self.embedding_dim))
                continue
            
            # Get prediction from current state
            prediction = current_states[level]
            
            # Compute weighted gradient
            coupling = np.zeros(self.embedding_dim)
            for (segment, _), weight in zip(self.retrieved_segments[level], 
                                           self.bucket_weights[level]):
                error = segment.centroid - prediction
                coupling += weight * error
            
            couplings.append(coupling)
        
        return couplings
    
    def inference_iteration(self,
                          query_embedding: np.ndarray,
                          k_per_level: List[int] = [50, 20, 10]) -> Tuple[float, float]:
        """
        Single iteration of unified inference.
        
        This implements the core algorithm:
        1. Use current states to retrieve from hash memory (Inference → Hash)
        2. Compute bucket weights based on prediction error
        3. Use weighted memories to update states (Hash → Inference)
        
        Returns:
            (total_free_energy, update_magnitude)
        """
        # Get current states from predictive coding
        current_states = [self.predictive_coding.get_state(level) 
                         for level in range(self.num_levels)]
        
        # Step 1: Retrieve from hash memory based on current states
        all_candidates = []
        for level in range(self.num_levels):
            query = current_states[level]
            candidates = self.hash_memory.memory_banks[level].retrieve_top_k(
                query,
                k=k_per_level[level] if level < len(k_per_level) else 10
            )
            all_candidates.append(candidates)
        
        # Step 2: Compute predictions from predictive coding
        predictions = self.predictive_coding.forward_pass()
        
        # Step 3: Compute bucket weights (implements w_i ∝ exp(-error))
        for level in range(self.num_levels):
            if all_candidates[level]:
                weights = self.compute_bucket_weights(
                    level,
                    all_candidates[level],
                    predictions[level]
                )
                self.bucket_weights[level] = weights
                self.retrieved_segments[level] = all_candidates[level]
            else:
                self.bucket_weights[level] = np.array([])
                self.retrieved_segments[level] = []
        
        # Step 4: Compute weighted retrieved memories
        retrieved_memories = []
        for level in range(self.num_levels):
            memory = self.retrieve_weighted_memory(
                level,
                all_candidates[level],
                self.bucket_weights[level]
            )
            retrieved_memories.append(memory)
        
        # Step 5: Compute hash coupling terms
        hash_couplings = self.compute_hash_coupling_terms(current_states)
        
        # Step 6: Run predictive coding inference step
        # Observations = retrieved memories (they constrain the states)
        observations = retrieved_memories
        
        free_energy, update_mag = self.predictive_coding.inference_step(
            observations,
            hash_couplings
        )
        
        # Add coupling term to free energy
        coupling_energy = 0.0
        for level in range(self.num_levels):
            if self.bucket_weights[level] is not None and len(self.bucket_weights[level]) > 0:
                for (segment, _), weight in zip(self.retrieved_segments[level],
                                               self.bucket_weights[level]):
                    error = np.linalg.norm(segment.centroid - predictions[level])**2
                    coupling_energy += weight * error
        
        # Add sparsity term (entropy regularization)
        sparsity_energy = 0.0
        for weights in self.bucket_weights:
            if weights is not None and len(weights) > 0:
                # Negative entropy: -λ Σ w log(w)
                weights_safe = np.maximum(weights, 1e-10)  # Avoid log(0)
                sparsity_energy -= self.lambda_sparse * np.sum(
                    weights * np.log(weights_safe)
                )
        
        total_free_energy = free_energy + coupling_energy + sparsity_energy
        
        return total_free_energy, update_mag
    
    def query(self,
             query_embedding: np.ndarray,
             max_iterations: int = 20,
             convergence_threshold: float = 1e-3,
             k_per_level: List[int] = [50, 20, 10],
             verbose: bool = True) -> Dict:
        """
        Query the unified memory system.
        
        Args:
            query_embedding: [embedding_dim] query vector
            max_iterations: Maximum inference iterations
            convergence_threshold: Convergence criterion
            k_per_level: Number of candidates per level
            verbose: Print progress
            
        Returns:
            Dictionary with results including final states, retrieved memories, etc.
        """
        # Initialize predictive coding from query
        self.predictive_coding.initialize_from_observation(query_embedding)
        
        # Track convergence
        free_energies = []
        update_magnitudes = []
        num_retrieved_per_level = []
        
        if verbose:
            print(f"\nRunning unified inference for {max_iterations} iterations...")
        
        for iteration in range(max_iterations):
            # Single inference iteration
            fe, update_mag = self.inference_iteration(query_embedding, k_per_level)
            
            free_energies.append(fe)
            update_magnitudes.append(update_mag)
            
            # Track how many segments retrieved per level
            num_retrieved = [
                len(segs) if segs else 0 
                for segs in self.retrieved_segments
            ]
            num_retrieved_per_level.append(num_retrieved)
            
            if verbose and (iteration % 5 == 0 or iteration < 3):
                print(f"  Iter {iteration}: F={fe:.3f}, |update|={update_mag:.4f}, "
                      f"retrieved={num_retrieved}")
            
            # Check convergence
            if update_mag < convergence_threshold:
                if verbose:
                    print(f"  Converged at iteration {iteration}!")
                break
        
        # Get final states
        final_states = [self.predictive_coding.get_state(level) 
                       for level in range(self.num_levels)]
        
        # Get final retrieved memories with weights
        final_retrieved = []
        for level in range(self.num_levels):
            if self.retrieved_segments[level]:
                retrieved_info = [
                    {
                        'segment_id': seg.segment_id,
                        'tokens': seg.tokens,
                        'weight': weight,
                        'centroid': seg.centroid
                    }
                    for (seg, _), weight in zip(self.retrieved_segments[level],
                                               self.bucket_weights[level])
                ]
                final_retrieved.append(retrieved_info)
            else:
                final_retrieved.append([])
        
        return {
            'converged': update_mag < convergence_threshold,
            'iterations': iteration + 1,
            'final_free_energy': free_energies[-1] if free_energies else 0,
            'free_energy_history': np.array(free_energies),
            'update_history': np.array(update_magnitudes),
            'final_states': final_states,
            'retrieved_memories': final_retrieved,
            'num_retrieved_history': num_retrieved_per_level
        }
    
    def get_memory_statistics(self) -> Dict:
        """Get comprehensive statistics about the system."""
        hash_stats = self.hash_memory.get_all_statistics()
        
        total_segments = sum(s['num_segments'] for s in hash_stats)
        total_buckets = sum(s['num_buckets'] for s in hash_stats)
        
        # Estimate memory usage
        signature_size = (64/8 + self.compressed_dim*4 + 4)  # hash + centroid + spread
        memory_bytes = total_segments * signature_size
        
        return {
            'total_segments': total_segments,
            'total_buckets': total_buckets,
            'memory_mb': memory_bytes / (1024**2),
            'levels': hash_stats,
            'compression_ratio': None  # Will compute if we know original size
        }


if __name__ == "__main__":
    print("="*70)
    print("UNIFIED HASH-PREDICTIVE MEMORY SYSTEM")
    print("="*70)
    
    # Create synthetic corpus
    print("\n1. Creating synthetic corpus...")
    num_tokens = 50000
    embedding_dim = 128
    
    # Generate tokens
    tokens = np.arange(num_tokens)
    
    # Generate embeddings with semantic structure
    # Create 10 "topics" with distinct clusters
    num_topics = 10
    embeddings = np.zeros((num_tokens, embedding_dim))
    
    topic_centers = [np.random.randn(embedding_dim) * 3 for _ in range(num_topics)]
    
    for i in range(num_tokens):
        topic = i % num_topics
        noise = np.random.randn(embedding_dim) * 0.5
        embeddings[i] = topic_centers[topic] + noise
    
    print(f"  Created {num_tokens} tokens with {num_topics} semantic topics")
    
    # Create unified system
    print("\n2. Building unified system...")
    system = UnifiedHashPredictiveMemory(
        embedding_dim=embedding_dim,
        compressed_dim=64,
        segment_sizes=[100, 1000, 10000],
        learning_rate=0.1,
        lambda_sparse=0.1
    )
    
    # Build memory
    system.build_memory(tokens, embeddings)
    
    # Show statistics
    stats = system.get_memory_statistics()
    print(f"\n3. System Statistics:")
    print(f"  Total segments: {stats['total_segments']}")
    print(f"  Total buckets: {stats['total_buckets']}")
    print(f"  Memory usage: {stats['memory_mb']:.2f} MB")
    
    # Test queries
    print("\n4. Testing queries...")
    
    # Query 1: From topic 3
    print("\n--- Query 1: Token from topic 3 ---")
    query_idx = 3003  # Topic 3
    query1 = embeddings[query_idx]
    
    results1 = system.query(
        query1,
        max_iterations=15,
        k_per_level=[30, 15, 5],
        verbose=True
    )
    
    print(f"\nQuery 1 Results:")
    print(f"  Converged: {results1['converged']}")
    print(f"  Iterations: {results1['iterations']}")
    print(f"  Final free energy: {results1['final_free_energy']:.3f}")
    
    print(f"\n  Top retrieved segments (Level 0):")
    for i, mem in enumerate(results1['retrieved_memories'][0][:5]):
        token_range = f"{mem['tokens'][0]}-{mem['tokens'][-1]}"
        print(f"    {i+1}. Segment {mem['segment_id']} (tokens {token_range}): "
              f"weight={mem['weight']:.3f}")
    
    # Query 2: From topic 7
    print("\n--- Query 2: Token from topic 7 ---")
    query_idx2 = 7007  # Topic 7
    query2 = embeddings[query_idx2]
    
    results2 = system.query(
        query2,
        max_iterations=15,
        k_per_level=[30, 15, 5],
        verbose=True
    )
    
    print(f"\nQuery 2 Results:")
    print(f"  Top retrieved segments (Level 0):")
    for i, mem in enumerate(results2['retrieved_memories'][0][:5]):
        token_range = f"{mem['tokens'][0]}-{mem['tokens'][-1]}"
        print(f"    {i+1}. Segment {mem['segment_id']} (tokens {token_range}): "
              f"weight={mem['weight']:.3f}")
    
    # Visualize convergence
    print("\n5. Generating convergence plots...")
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Free energy convergence
    axes[0, 0].plot(results1['free_energy_history'], 'b-', label='Query 1')
    axes[0, 0].plot(results2['free_energy_history'], 'r-', label='Query 2')
    axes[0, 0].set_xlabel('Iteration')
    axes[0, 0].set_ylabel('Free Energy')
    axes[0, 0].set_title('Free Energy Convergence')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Update magnitude
    axes[0, 1].semilogy(results1['update_history'], 'b-', label='Query 1')
    axes[0, 1].semilogy(results2['update_history'], 'r-', label='Query 2')
    axes[0, 1].axhline(y=1e-3, color='k', linestyle='--', alpha=0.3, label='Threshold')
    axes[0, 1].set_xlabel('Iteration')
    axes[0, 1].set_ylabel('Update Magnitude (log)')
    axes[0, 1].set_title('Convergence Rate')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Number of retrieved segments over time
    retrieved_history = np.array(results1['num_retrieved_history'])
    for level in range(3):
        axes[1, 0].plot(retrieved_history[:, level], label=f'Level {level}')
    axes[1, 0].set_xlabel('Iteration')
    axes[1, 0].set_ylabel('Segments Retrieved')
    axes[1, 0].set_title('Retrieved Segments per Level (Query 1)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Bucket weight distribution (final)
    final_weights = [mem['weight'] for mem in results1['retrieved_memories'][0]]
    if final_weights:
        axes[1, 1].bar(range(len(final_weights)), sorted(final_weights, reverse=True))
        axes[1, 1].set_xlabel('Segment Rank')
        axes[1, 1].set_ylabel('Weight')
        axes[1, 1].set_title('Final Bucket Weights (Level 0, Query 1)')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/home/claude/unified_system_results.png', dpi=150, bbox_inches='tight')
    print("  Saved to unified_system_results.png")
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
