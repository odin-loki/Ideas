"""
Comprehensive Benchmark and Demonstration
Compares unified hash-predictive system against baselines.
"""

import numpy as np
import time
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from unified_system import UnifiedHashPredictiveMemory

from pathlib import Path

# Figures land beside this script. They used to be written to an absolute
# path under /home/claude, which is why none of them ever reached the repo.
HERE = Path(__file__).resolve().parent


class StandardAttention:
    """Baseline: Standard O(N²) attention for comparison."""
    
    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim
        self.memory_embeddings = None
        self.memory_tokens = None
    
    def build_memory(self, tokens: np.ndarray, embeddings: np.ndarray):
        """Store all embeddings in memory."""
        self.memory_tokens = tokens
        self.memory_embeddings = embeddings
    
    def query(self, query_embedding: np.ndarray, k: int = 10) -> Dict:
        """Query using full attention over all tokens."""
        start_time = time.time()
        
        # Compute attention scores for ALL tokens (O(N))
        scores = self.memory_embeddings @ query_embedding
        scores /= np.sqrt(self.embedding_dim)
        
        # Softmax
        attention_weights = np.exp(scores - np.max(scores))
        attention_weights /= attention_weights.sum()
        
        # Get top-k
        top_k_indices = np.argsort(attention_weights)[-k:][::-1]
        
        query_time = time.time() - start_time
        
        # Memory usage
        memory_bytes = self.memory_embeddings.nbytes
        
        return {
            'query_time': query_time,
            'memory_bytes': memory_bytes,
            'top_k_indices': top_k_indices,
            'top_k_weights': attention_weights[top_k_indices]
        }


class SimpleKNN:
    """Baseline: Simple k-NN retrieval (no hash)."""
    
    def __init__(self, embedding_dim: int, segment_size: int = 100):
        self.embedding_dim = embedding_dim
        self.segment_size = segment_size
        self.segment_centroids = None
        self.segments = None
    
    def build_memory(self, tokens: np.ndarray, embeddings: np.ndarray):
        """Build segments and store centroids."""
        num_tokens = len(tokens)
        segments = []
        centroids = []
        
        for i in range(0, num_tokens, self.segment_size):
            end = min(i + self.segment_size, num_tokens)
            if end - i < self.segment_size // 2:
                continue
            
            segment_embeddings = embeddings[i:end]
            centroid = segment_embeddings.mean(axis=0)
            
            segments.append({
                'tokens': tokens[i:end],
                'embeddings': segment_embeddings,
                'start': i,
                'end': end
            })
            centroids.append(centroid)
        
        self.segments = segments
        self.segment_centroids = np.array(centroids)
    
    def query(self, query_embedding: np.ndarray, k: int = 10) -> Dict:
        """Query using brute-force k-NN over centroids."""
        start_time = time.time()
        
        # Compute distances to all centroids (O(N/s))
        distances = np.linalg.norm(
            self.segment_centroids - query_embedding,
            axis=1
        )
        
        # Get top-k nearest
        top_k_indices = np.argsort(distances)[:k]
        
        query_time = time.time() - start_time
        
        # Memory usage (centroids only)
        memory_bytes = self.segment_centroids.nbytes
        
        return {
            'query_time': query_time,
            'memory_bytes': memory_bytes,
            'top_k_indices': top_k_indices,
            'top_k_segments': [self.segments[i] for i in top_k_indices]
        }


def run_comprehensive_benchmark(num_tokens_list: List[int],
                                embedding_dim: int = 128):
    """
    Run comprehensive benchmark across different context sizes.
    
    Args:
        num_tokens_list: List of context sizes to test
        embedding_dim: Embedding dimension
    """
    results = {
        'standard_attention': [],
        'simple_knn': [],
        'unified_system': []
    }
    
    print("="*70)
    print("COMPREHENSIVE BENCHMARK")
    print("="*70)
    
    for num_tokens in num_tokens_list:
        print(f"\n{'='*70}")
        print(f"Context Size: {num_tokens:,} tokens")
        print(f"{'='*70}")
        
        # Generate synthetic data
        print("Generating data...")
        tokens = np.arange(num_tokens)
        
        # Create semantic structure
        num_topics = 10
        embeddings = np.zeros((num_tokens, embedding_dim))
        topic_centers = [np.random.randn(embedding_dim) * 3 for _ in range(num_topics)]
        
        for i in range(num_tokens):
            topic = i % num_topics
            noise = np.random.randn(embedding_dim) * 0.5
            embeddings[i] = topic_centers[topic] + noise
        
        # Create query from a specific topic
        query_idx = num_tokens // 3
        query = embeddings[query_idx]
        
        # Test Standard Attention (if feasible)
        if num_tokens <= 100000:  # Only test for smaller contexts
            print("\n1. Standard Attention:")
            standard = StandardAttention(embedding_dim)
            
            build_start = time.time()
            standard.build_memory(tokens, embeddings)
            build_time = time.time() - build_start
            
            result = standard.query(query, k=10)
            
            print(f"   Build time: {build_time:.3f}s")
            print(f"   Query time: {result['query_time']*1000:.2f}ms")
            print(f"   Memory: {result['memory_bytes']/(1024**2):.2f} MB")
            
            results['standard_attention'].append({
                'num_tokens': num_tokens,
                'build_time': build_time,
                'query_time': result['query_time'],
                'memory_mb': result['memory_bytes']/(1024**2)
            })
        else:
            print("\n1. Standard Attention: SKIPPED (too large)")
            results['standard_attention'].append(None)
        
        # Test Simple k-NN
        print("\n2. Simple k-NN:")
        knn = SimpleKNN(embedding_dim, segment_size=100)
        
        build_start = time.time()
        knn.build_memory(tokens, embeddings)
        build_time = time.time() - build_start
        
        result = knn.query(query, k=10)
        
        print(f"   Build time: {build_time:.3f}s")
        print(f"   Query time: {result['query_time']*1000:.2f}ms")
        print(f"   Memory: {result['memory_bytes']/(1024**2):.2f} MB")
        
        results['simple_knn'].append({
            'num_tokens': num_tokens,
            'build_time': build_time,
            'query_time': result['query_time'],
            'memory_mb': result['memory_bytes']/(1024**2)
        })
        
        # Test Unified System
        print("\n3. Unified Hash-Predictive System:")
        system = UnifiedHashPredictiveMemory(
            embedding_dim=embedding_dim,
            compressed_dim=64,
            segment_sizes=[100, 1000, 10000],
            learning_rate=0.1
        )
        
        build_start = time.time()
        system.build_memory(tokens, embeddings)
        build_time = time.time() - build_start
        
        query_start = time.time()
        result = system.query(query, max_iterations=10, verbose=False)
        query_time = time.time() - query_start
        
        stats = system.get_memory_statistics()
        
        print(f"   Build time: {build_time:.3f}s")
        print(f"   Query time: {query_time*1000:.2f}ms")
        print(f"   Memory: {stats['memory_mb']:.2f} MB")
        print(f"   Iterations: {result['iterations']}")
        print(f"   Converged: {result['converged']}")
        
        results['unified_system'].append({
            'num_tokens': num_tokens,
            'build_time': build_time,
            'query_time': query_time,
            'memory_mb': stats['memory_mb'],
            'iterations': result['iterations'],
            'converged': result['converged']
        })
    
    return results


def visualize_benchmark_results(results: Dict, output_path: str = HERE / "benchmark_results.png"):
    """Create visualization of benchmark results."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Extract data
    context_sizes = [r['num_tokens'] for r in results['unified_system']]
    
    # Query time comparison
    ax = axes[0, 0]
    
    # Standard attention (where available)
    std_data = [r for r in results['standard_attention'] if r is not None]
    if std_data:
        std_sizes = [r['num_tokens'] for r in std_data]
        std_times = [r['query_time']*1000 for r in std_data]
        ax.plot(std_sizes, std_times, 'r-o', label='Standard Attention', linewidth=2)
    
    # Simple k-NN
    knn_sizes = [r['num_tokens'] for r in results['simple_knn']]
    knn_times = [r['query_time']*1000 for r in results['simple_knn']]
    ax.plot(knn_sizes, knn_times, 'b-s', label='Simple k-NN', linewidth=2)
    
    # Unified system
    unified_times = [r['query_time']*1000 for r in results['unified_system']]
    ax.plot(context_sizes, unified_times, 'g-^', label='Unified System', linewidth=2)
    
    ax.set_xlabel('Context Size (tokens)', fontsize=12)
    ax.set_ylabel('Query Time (ms)', fontsize=12)
    ax.set_title('Query Time Comparison', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Memory usage comparison
    ax = axes[0, 1]
    
    if std_data:
        std_memory = [r['memory_mb'] for r in std_data]
        ax.plot(std_sizes, std_memory, 'r-o', label='Standard Attention', linewidth=2)
    
    knn_memory = [r['memory_mb'] for r in results['simple_knn']]
    ax.plot(knn_sizes, knn_memory, 'b-s', label='Simple k-NN', linewidth=2)
    
    unified_memory = [r['memory_mb'] for r in results['unified_system']]
    ax.plot(context_sizes, unified_memory, 'g-^', label='Unified System', linewidth=2)
    
    ax.set_xlabel('Context Size (tokens)', fontsize=12)
    ax.set_ylabel('Memory Usage (MB)', fontsize=12)
    ax.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Speedup factors
    ax = axes[1, 0]
    
    if std_data and len(std_data) == len(unified_times):
        speedups_std = [std_data[i]['query_time'] / results['unified_system'][i]['query_time']
                       for i in range(len(std_data))]
        ax.plot(std_sizes, speedups_std, 'r-o', label='vs Standard', linewidth=2)
    
    speedups_knn = [results['simple_knn'][i]['query_time'] / results['unified_system'][i]['query_time']
                    for i in range(len(context_sizes))]
    ax.plot(context_sizes, speedups_knn, 'b-s', label='vs k-NN', linewidth=2)
    
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel('Context Size (tokens)', fontsize=12)
    ax.set_ylabel('Speedup Factor', fontsize=12)
    ax.set_title('Speed Improvement', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Memory compression factors
    ax = axes[1, 1]
    
    if std_data and len(std_data) == len(unified_memory):
        compression_std = [std_data[i]['memory_mb'] / results['unified_system'][i]['memory_mb']
                          for i in range(len(std_data))]
        ax.plot(std_sizes, compression_std, 'r-o', label='vs Standard', linewidth=2)
    
    compression_knn = [results['simple_knn'][i]['memory_mb'] / results['unified_system'][i]['memory_mb']
                      for i in range(len(context_sizes))]
    ax.plot(context_sizes, compression_knn, 'b-s', label='vs k-NN', linewidth=2)
    
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel('Context Size (tokens)', fontsize=12)
    ax.set_ylabel('Compression Factor', fontsize=12)
    ax.set_title('Memory Compression', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nBenchmark visualization saved to: {output_path}")


def print_summary_table(results: Dict):
    """Print a summary table of results."""
    print("\n" + "="*70)
    print("BENCHMARK SUMMARY")
    print("="*70)
    
    print("\n{:<15} {:<15} {:<15} {:<15}".format(
        "Context Size", "System", "Query Time", "Memory"
    ))
    print("-" * 70)
    
    for i, unified in enumerate(results['unified_system']):
        num_tokens = unified['num_tokens']
        
        # Unified system
        print("{:<15} {:<15} {:<15} {:<15}".format(
            f"{num_tokens:,}",
            "Unified",
            f"{unified['query_time']*1000:.2f}ms",
            f"{unified['memory_mb']:.2f}MB"
        ))
        
        # k-NN
        knn = results['simple_knn'][i]
        print("{:<15} {:<15} {:<15} {:<15}".format(
            "",
            "k-NN",
            f"{knn['query_time']*1000:.2f}ms",
            f"{knn['memory_mb']:.2f}MB"
        ))
        
        # Standard (if available)
        if i < len(results['standard_attention']) and results['standard_attention'][i]:
            std = results['standard_attention'][i]
            print("{:<15} {:<15} {:<15} {:<15}".format(
                "",
                "Standard",
                f"{std['query_time']*1000:.2f}ms",
                f"{std['memory_mb']:.2f}MB"
            ))
        
        print("-" * 70)


if __name__ == "__main__":
    # Run benchmark with increasing context sizes
    context_sizes = [1000, 5000, 10000, 50000, 100000]
    
    print("\nRunning benchmark with context sizes:", context_sizes)
    print("This may take a few minutes...\n")
    
    results = run_comprehensive_benchmark(
        context_sizes,
        embedding_dim=128
    )
    
    # Print summary
    print_summary_table(results)
    
    # Visualize
    visualize_benchmark_results(results)
    
    # Print key findings
    print("\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)
    
    # Calculate average improvements for largest context
    largest_idx = -1
    unified = results['unified_system'][largest_idx]
    knn = results['simple_knn'][largest_idx]
    
    speed_improvement = knn['query_time'] / unified['query_time']
    memory_improvement = knn['memory_mb'] / unified['memory_mb']
    
    print(f"\nFor {unified['num_tokens']:,} token context:")
    print(f"  Speed improvement vs k-NN: {speed_improvement:.1f}×")
    print(f"  Memory compression vs k-NN: {memory_improvement:.1f}×")
    print(f"  Converged in {unified['iterations']} iterations")
    
    if results['standard_attention'][0]:  # If we have standard results
        std = results['standard_attention'][0]
        speed_vs_std = std['query_time'] / results['unified_system'][0]['query_time']
        memory_vs_std = std['memory_mb'] / results['unified_system'][0]['memory_mb']
        
        print(f"\nFor {results['unified_system'][0]['num_tokens']:,} token context:")
        print(f"  Speed improvement vs standard: {speed_vs_std:.1f}×")
        print(f"  Memory compression vs standard: {memory_vs_std:.1f}×")
    
    print("\n" + "="*70)
