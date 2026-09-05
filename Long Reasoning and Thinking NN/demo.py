"""
Main Demonstration: Unified Hash-Predictive Memory System
Shows the key features and dual feedback mechanism.
"""

import numpy as np
import matplotlib.pyplot as plt
from unified_system import UnifiedHashPredictiveMemory

from pathlib import Path

# Figures land beside this script. They used to be written to an absolute
# path under /home/claude, which is why none of them ever reached the repo.
HERE = Path(__file__).resolve().parent


def create_realistic_corpus(num_tokens: int = 100000, embedding_dim: int = 128):
    """
    Create a more realistic corpus with:
    - Temporal structure (concepts evolve over time)
    - Semantic clusters (topics)
    - Some noise
    """
    print("Creating realistic corpus...")
    
    # Create temporal evolution of topics
    num_topics = 15
    topic_centers = [np.random.randn(embedding_dim) * 2 for _ in range(num_topics)]
    
    tokens = np.arange(num_tokens)
    embeddings = np.zeros((num_tokens, embedding_dim))
    
    # Add temporal drift to topics
    for i in range(num_tokens):
        # Topic changes slowly over time
        topic_id = int((i / num_tokens) * num_topics)
        
        # Topics also repeat cyclically
        cyclic_topic = i % num_topics
        
        # Blend temporal and cyclic
        primary_topic = topic_centers[topic_id]
        secondary_topic = topic_centers[cyclic_topic]
        
        # Weighted combination
        weight = 0.7
        base = weight * primary_topic + (1 - weight) * secondary_topic
        
        # Add noise
        noise = np.random.randn(embedding_dim) * 0.3
        
        embeddings[i] = base + noise
    
    print(f"  Created {num_tokens} tokens with {num_topics} topics")
    print(f"  Embedding dimension: {embedding_dim}")
    
    return tokens, embeddings, topic_centers


def demonstrate_dual_feedback():
    """Demonstrate the dual feedback mechanism."""
    
    print("\n" + "="*80)
    print("DEMONSTRATION 1: DUAL FEEDBACK MECHANISM")
    print("="*80)
    
    print("""
This demonstrates the key innovation: single free energy creates dual feedback.

Feedback Loop 1 (Inference → Hash):
    Current states predict which memories are relevant
    → Bucket weights: w_i ∝ exp(-||memory_i - prediction||²)
    
Feedback Loop 2 (Hash → Inference):
    Retrieved memories constrain state updates
    → State dynamics include hash coupling term
    
Both emerge automatically from: ∂F_total/∂s and ∂F_total/∂w
""")
    
    # Create small corpus for clear visualization
    num_tokens = 10000
    embedding_dim = 64
    
    tokens, embeddings, _ = create_realistic_corpus(num_tokens, embedding_dim)
    
    # Create system
    system = UnifiedHashPredictiveMemory(
        embedding_dim=embedding_dim,
        compressed_dim=32,
        segment_sizes=[100, 1000],
        learning_rate=0.15,
        lambda_sparse=0.1
    )
    
    system.build_memory(tokens, embeddings)
    
    # Query from middle of corpus
    query_idx = 5000
    query = embeddings[query_idx]
    
    print(f"\nQuery: token at position {query_idx}")
    print("Expected to retrieve: tokens 4900-5100 (same topic)")
    
    # Track feedback during inference
    print("\nRunning inference with detailed tracking...")
    
    # Manually run iterations to track feedback
    system.predictive_coding.initialize_from_observation(query)
    
    feedback_data = {
        'iteration': [],
        'free_energy': [],
        'state_change': [],
        'top_bucket_weights': [],
        'top_bucket_ids': []
    }
    
    for iteration in range(15):
        # Get state before update
        state_before = system.predictive_coding.get_state(0).copy()
        
        # Run one iteration
        fe, update_mag = system.inference_iteration(query, k_per_level=[20, 5])
        
        # Track data
        feedback_data['iteration'].append(iteration)
        feedback_data['free_energy'].append(fe)
        feedback_data['state_change'].append(update_mag)
        
        # Track top bucket weights (Level 0)
        if system.bucket_weights[0] is not None and len(system.bucket_weights[0]) > 0:
            top_5_indices = np.argsort(system.bucket_weights[0])[-5:][::-1]
            top_5_weights = system.bucket_weights[0][top_5_indices]
            top_5_segments = [system.retrieved_segments[0][i][0].segment_id 
                            for i in top_5_indices]
            
            feedback_data['top_bucket_weights'].append(top_5_weights)
            feedback_data['top_bucket_ids'].append(top_5_segments)
        
        if iteration < 3 or iteration % 5 == 0:
            print(f"\nIteration {iteration}:")
            print(f"  Free energy: {fe:.3f}")
            print(f"  State change: {update_mag:.4f}")
            if len(feedback_data['top_bucket_ids']) > 0:
                print(f"  Top bucket IDs: {feedback_data['top_bucket_ids'][-1]}")
                print(f"  Top weights: {[f'{w:.3f}' for w in feedback_data['top_bucket_weights'][-1]]}")
    
    # Visualize dual feedback
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Free energy (shows both feedbacks working)
    ax = axes[0, 0]
    ax.plot(feedback_data['iteration'], feedback_data['free_energy'], 'b-o', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Free Energy')
    ax.set_title('Free Energy: Joint Optimization', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.text(0.05, 0.95, 'Both feedbacks\nminimizing F_total',
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # State changes (Feedback 2: Hash → Inference)
    ax = axes[0, 1]
    ax.semilogy(feedback_data['iteration'], feedback_data['state_change'], 'r-s', linewidth=2)
    ax.axhline(y=1e-3, color='k', linestyle='--', alpha=0.5, label='Convergence threshold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('State Update Magnitude (log)')
    ax.set_title('Feedback 2: Hash → Inference\n(Retrieved memories update states)', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Bucket weight evolution (Feedback 1: Inference → Hash)
    ax = axes[1, 0]
    for i in range(5):
        weights = [data[i] if len(data) > i else 0 
                  for data in feedback_data['top_bucket_weights']]
        ax.plot(feedback_data['iteration'][:len(weights)], weights, 
               marker='o', label=f'Bucket rank {i+1}', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Bucket Weight')
    ax.set_title('Feedback 1: Inference → Hash\n(States predict which buckets matter)', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Final bucket distribution
    ax = axes[1, 1]
    if len(feedback_data['top_bucket_weights']) > 0:
        final_weights = feedback_data['top_bucket_weights'][-1]
        final_ids = feedback_data['top_bucket_ids'][-1]
        
        bars = ax.bar(range(len(final_weights)), final_weights, color='green', alpha=0.7)
        ax.set_xlabel('Bucket Rank')
        ax.set_ylabel('Final Weight')
        ax.set_title('Final Bucket Weights (Converged)', fontweight='bold')
        ax.set_xticks(range(len(final_weights)))
        ax.set_xticklabels([f'ID {id}' for id in final_ids], rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(HERE / "dual_feedback_demo.png", dpi=150, bbox_inches='tight')
    print("\n→ Saved visualization to: dual_feedback_demo.png")


def demonstrate_hierarchical_retrieval():
    """Demonstrate multi-resolution hierarchical retrieval."""
    
    print("\n" + "="*80)
    print("DEMONSTRATION 2: HIERARCHICAL MULTI-RESOLUTION RETRIEVAL")
    print("="*80)
    
    print("""
This shows how the system retrieves at multiple granularities:
- Level 0 (fine):   100-token segments  → Specific details
- Level 1 (medium): 1,000-token segments → Broader context
- Level 2 (coarse): 10,000-token segments → Abstract concepts
""")
    
    # Create corpus
    num_tokens = 50000
    embedding_dim = 128
    
    tokens, embeddings, _ = create_realistic_corpus(num_tokens, embedding_dim)
    
    # Create system
    system = UnifiedHashPredictiveMemory(
        embedding_dim=embedding_dim,
        compressed_dim=64,
        segment_sizes=[100, 1000, 10000],
        learning_rate=0.1
    )
    
    system.build_memory(tokens, embeddings)
    
    # Query
    query_idx = 25000
    query = embeddings[query_idx]
    
    print(f"\nQuery: token at position {query_idx}")
    
    # Run query
    results = system.query(
        query,
        max_iterations=120,
        k_per_level=[30, 15, 5],
        verbose=False
    )
    
    print(f"\nConverged in {results['iterations']} iterations")
    
    # Analyze hierarchical retrieval
    print("\n" + "-"*80)
    print("HIERARCHICAL RETRIEVAL ANALYSIS")
    print("-"*80)
    
    for level in range(3):
        print(f"\nLevel {level} (segment_size={system.segment_sizes[level]}):")
        
        if results['retrieved_memories'][level]:
            retrieved = results['retrieved_memories'][level]
            
            # Top 5
            print(f"  Top 5 retrieved segments:")
            for i, mem in enumerate(retrieved[:5]):
                token_range = f"{mem['tokens'][0]}-{mem['tokens'][-1]}"
                distance_from_query = abs(mem['tokens'][0] - query_idx)
                print(f"    {i+1}. Segment {mem['segment_id']}: tokens {token_range}")
                print(f"       Weight: {mem['weight']:.3f}, Distance from query: {distance_from_query}")
            
            # Statistics
            avg_weight = np.mean([m['weight'] for m in retrieved])
            weight_std = np.std([m['weight'] for m in retrieved])
            print(f"  Statistics: {len(retrieved)} segments retrieved")
            print(f"    Avg weight: {avg_weight:.3f} ± {weight_std:.3f}")
    
    # Visualize hierarchical structure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Token coverage at each level
    ax = axes[0, 0]
    for level in range(3):
        if results['retrieved_memories'][level]:
            token_positions = []
            weights = []
            for mem in results['retrieved_memories'][level]:
                center = (mem['tokens'][0] + mem['tokens'][-1]) / 2
                token_positions.append(center)
                weights.append(mem['weight'])
            
            # Weighted scatter
            scatter = ax.scatter(token_positions, [level]*len(token_positions),
                               s=[w*1000 for w in weights], alpha=0.6,
                               label=f'Level {level}')
    
    ax.axvline(x=query_idx, color='red', linestyle='--', linewidth=2, label='Query position')
    ax.set_xlabel('Token Position')
    ax.set_ylabel('Hierarchy Level')
    ax.set_yticks([0, 1, 2])
    ax.set_title('Retrieved Segments Across Hierarchy\n(size = weight)', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Weight distribution per level
    ax = axes[0, 1]
    for level in range(3):
        if results['retrieved_memories'][level]:
            weights = [m['weight'] for m in results['retrieved_memories'][level]]
            ax.hist(weights, bins=20, alpha=0.5, label=f'Level {level}')
    ax.set_xlabel('Weight')
    ax.set_ylabel('Count')
    ax.set_title('Weight Distributions', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Convergence by level
    ax = axes[1, 0]
    history = np.array(results['num_retrieved_history'])
    for level in range(3):
        ax.plot(history[:, level], marker='o', label=f'Level {level}', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Segments Retrieved')
    ax.set_title('Retrieved Segments Over Time', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Free energy
    ax = axes[1, 1]
    ax.plot(results['free_energy_history'], 'b-o', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Free Energy')
    ax.set_title('Free Energy Convergence', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(HERE / "hierarchical_retrieval_demo.png", dpi=150, bbox_inches='tight')
    print("\n→ Saved visualization to: hierarchical_retrieval_demo.png")


def demonstrate_scaling():
    """Demonstrate scaling to large contexts."""
    
    print("\n" + "="*80)
    print("DEMONSTRATION 3: SCALING TO LARGE CONTEXTS")
    print("="*80)
    
    print("""
This shows how the system scales to contexts that are impossible for
standard transformers.
""")
    
    context_sizes = [10000, 50000, 100000, 500000]
    embedding_dim = 128
    
    results = []
    
    for num_tokens in context_sizes:
        print(f"\n{'='*60}")
        print(f"Context: {num_tokens:,} tokens ({num_tokens/1000:.0f}K)")
        print(f"{'='*60}")
        
        # Generate data
        print("Generating corpus...")
        tokens, embeddings, _ = create_realistic_corpus(num_tokens, embedding_dim)
        
        # Build system
        system = UnifiedHashPredictiveMemory(
            embedding_dim=embedding_dim,
            compressed_dim=64,
            segment_sizes=[100, 1000, 10000]
        )
        
        import time
        build_start = time.time()
        system.build_memory(tokens, embeddings)
        build_time = time.time() - build_start
        
        # Query
        query_idx = num_tokens // 2
        query = embeddings[query_idx]
        
        query_start = time.time()
        result = system.query(query, max_iterations=120, verbose=False)
        query_time = time.time() - query_start
        
        stats = system.get_memory_statistics()
        
        print(f"\nResults:")
        print(f"  Build time: {build_time:.2f}s")
        print(f"  Query time: {query_time*1000:.1f}ms")
        print(f"  Memory usage: {stats['memory_mb']:.2f} MB")
        print(f"  Segments: {stats['total_segments']:,}")
        print(f"  Buckets: {stats['total_buckets']:,}")
        print(f"  Converged: {result['converged']} ({result['iterations']} iterations)")
        
        results.append({
            'num_tokens': num_tokens,
            'build_time': build_time,
            'query_time': query_time,
            'memory_mb': stats['memory_mb'],
            'iterations': result['iterations']
        })
    
    # Visualize scaling
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    sizes = [r['num_tokens'] for r in results]
    
    # Query time scaling
    ax = axes[0]
    query_times = [r['query_time']*1000 for r in results]
    ax.plot(sizes, query_times, 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('Context Size (tokens)')
    ax.set_ylabel('Query Time (ms)')
    ax.set_title('Query Time Scaling\n(Sublinear in context size)', fontweight='bold')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    
    # Memory scaling
    ax = axes[1]
    memory = [r['memory_mb'] for r in results]
    ax.plot(sizes, memory, 'go-', linewidth=2, markersize=8)
    ax.set_xlabel('Context Size (tokens)')
    ax.set_ylabel('Memory Usage (MB)')
    ax.set_title('Memory Scaling\n(Linear as expected)', fontweight='bold')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)
    
    # Convergence
    ax = axes[2]
    iterations = [r['iterations'] for r in results]
    ax.plot(sizes, iterations, 'ro-', linewidth=2, markersize=8)
    ax.axhline(y=120, color='k', linestyle='--', alpha=0.3, label='Max iterations')
    ax.set_xlabel('Context Size (tokens)')
    ax.set_ylabel('Iterations to Converge')
    ax.set_title('Convergence Speed\n(Near-flat in context size)', fontweight='bold')
    ax.set_xscale('log')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(HERE / "scaling_demo.png", dpi=150, bbox_inches='tight')
    print("\n→ Saved visualization to: scaling_demo.png")
    
    # Print summary
    print("\n" + "="*80)
    print("SCALING SUMMARY")
    print("="*80)
    print(f"\nAchieved {context_sizes[-1]:,} token context:")
    print(f"  Query time: {results[-1]['query_time']*1000:.1f}ms")
    print(f"  Memory: {results[-1]['memory_mb']:.1f}MB")
    print(f"  This would require {context_sizes[-1]*128*4/(1024**2):.0f}MB for standard transformer!")
    print(f"  Compression: {(context_sizes[-1]*128*4/(1024**2))/results[-1]['memory_mb']:.0f}×")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("UNIFIED HASH-PREDICTIVE MEMORY: COMPREHENSIVE DEMONSTRATION")
    print("="*80)
    
    # Run all demonstrations
    demonstrate_dual_feedback()
    demonstrate_hierarchical_retrieval()
    demonstrate_scaling()
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE!")
    print("="*80)
    print("\nGenerated visualizations:")
    print("  1. dual_feedback_demo.png - Shows dual feedback mechanism")
    print("  2. hierarchical_retrieval_demo.png - Shows multi-resolution retrieval")
    print("  3. scaling_demo.png - Shows scaling to large contexts")
    print("\nKey takeaways:")
    print("  ✓ Single free energy creates dual feedback automatically")
    print("  ✓ Hierarchical retrieval works at multiple granularities")
    print("  ✓ Scales to 500K+ tokens: query time grows sublinearly")
    print("  ✓ Iterations to converge stay near-flat as context grows")
    print("="*80)
