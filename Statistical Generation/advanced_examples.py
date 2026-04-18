"""
Advanced Examples for Universal Statistical Generator Framework
================================================================

This script demonstrates more sophisticated usage patterns.
"""

from universal_generator import Generator, InformationFilter, LevyTriplet
import numpy as np


def example_long_context():
    """
    Demonstrate advantage of long context over classical n-grams.
    
    Shows how our framework can use 50+ word context while n-grams
    are limited to 3-5 words.
    """
    print("=" * 80)
    print("LONG CONTEXT DEMONSTRATION")
    print("=" * 80)
    
    # Create story with long-range dependencies
    story = """
    once upon a time there was a brave knight named arthur
    arthur lived in a castle with his faithful horse named thunder
    one day arthur rode thunder into the dark forest
    in the forest arthur found a magic sword stuck in stone
    arthur pulled the sword from the stone with great strength
    the sword glowed with magical power in arthur hands
    with his new sword arthur defeated the evil dragon
    the kingdom celebrated and arthur became king
    king arthur ruled wisely with his magic sword for many years
    """.lower().split()
    
    vocab = sorted(set(story))
    
    # Train with different context lengths
    for context_len in [3, 10, 20]:
        gen = Generator(vocab)
        gen.train(story, context_length=context_len, min_count=1)
        
        # Generate continuation
        initial = story[:context_len]
        generated = gen.generate(seed=42, length=15, initial_context=initial)
        
        print(f"\nContext length {context_len}:")
        print("Initial:", " ".join(initial[-5:]))
        print("Generated:", " ".join(generated[-15:]))
        
        # Perplexity on test
        test = "arthur pulled the sword".split()
        perplexity = gen.perplexity(test, context_length=min(context_len, len(test)-1))
        print(f"Perplexity: {perplexity:.2f}")


def example_temperature_sampling():
    """
    Demonstrate temperature-based sampling for controlling randomness.
    """
    print("\n" + "=" * 80)
    print("TEMPERATURE SAMPLING DEMONSTRATION")
    print("=" * 80)
    
    text = """
    the quick brown fox jumps over the lazy dog
    the fast red cat runs under the sleepy bird
    the slow blue elephant walks beside the tired mouse
    """.lower().split()
    
    vocab = sorted(set(text))
    gen = Generator(vocab)
    gen.train(text, context_length=3, min_count=1)
    
    initial = ["the", "quick", "brown"]
    
    for temp in [0.1, 0.5, 1.0, 2.0]:
        generated = gen.generate(
            seed=42, 
            length=10, 
            initial_context=initial,
            temperature=temp
        )
        print(f"\nTemperature {temp}:")
        print(" ".join(generated))


def example_hierarchical_composition():
    """
    Demonstrate building complex generators from simple ones.
    
    Shows category theory in action: compose character-level and
    word-level generators.
    """
    print("\n" + "=" * 80)
    print("HIERARCHICAL COMPOSITION DEMONSTRATION")
    print("=" * 80)
    
    # Character-level generator
    text_chars = list("the cat sat on the mat")
    char_gen = Generator(sorted(set(text_chars)))
    char_gen.train(text_chars, context_length=5, min_count=1)
    
    print("Character-level generation:")
    char_output = char_gen.generate(seed=42, length=30)
    print("".join(char_output))
    
    # Word-level generator
    text_words = "the cat sat on the mat the dog ran in the park".split()
    word_gen = Generator(sorted(set(text_words)))
    word_gen.train(text_words, context_length=3, min_count=1)
    
    print("\nWord-level generation:")
    word_output = word_gen.generate(seed=42, length=10)
    print(" ".join(word_output))
    
    # Note: True hierarchical composition would require character → word → sentence
    # This would need additional abstraction layers


def example_compression_quality():
    """
    Compare storage efficiency vs classical methods.
    """
    print("\n" + "=" * 80)
    print("COMPRESSION EFFICIENCY DEMONSTRATION")
    print("=" * 80)
    
    # Generate larger dataset
    np.random.seed(42)
    
    words = ["the", "cat", "sat", "on", "mat", "dog", "ran", "in", "park", "bird"]
    data = []
    for _ in range(1000):
        sentence_len = np.random.randint(5, 10)
        sentence = np.random.choice(words, size=sentence_len)
        data.extend(sentence)
    
    print(f"Dataset: {len(data)} words, {len(set(data))} unique")
    
    # Calculate classical n-gram storage
    V = len(set(data))
    for n in [3, 4, 5]:
        states_ngram = V ** n
        storage_ngram = states_ngram * 4  # 4 bytes per probability
        
        print(f"\n{n}-gram model:")
        print(f"  States: {states_ngram:,}")
        print(f"  Storage: {storage_ngram / 1e9:.2f} GB")
    
    # Our framework
    gen = Generator(sorted(set(data)), max_states=2**20)
    gen.train(data, context_length=10, min_count=2)
    
    storage_ours = len(gen.states) * V * 4  # states × vocab × 4 bytes
    
    print(f"\nOur framework (context=10):")
    print(f"  States: {len(gen.states):,}")
    print(f"  Storage: {storage_ours / 1e6:.2f} MB")
    print(f"  Compression vs 5-gram: {(V**5 * 4 / storage_ours):.0f}x smaller")


def example_adaptive_generation():
    """
    Show how generator adapts to different domains.
    """
    print("\n" + "=" * 80)
    print("DOMAIN ADAPTATION DEMONSTRATION")
    print("=" * 80)
    
    # Two different domains
    science_text = """
    the experiment was conducted in the laboratory using advanced equipment
    the hypothesis was tested through rigorous scientific methodology
    the results were analyzed and published in peer reviewed journals
    """.lower().split()
    
    casual_text = """
    hey dude lets hang out and grab some pizza tonight
    yeah man that sounds awesome lets do it
    cool see you later bro have a great day
    """.lower().split()
    
    vocab = sorted(set(science_text + casual_text))
    
    # Train separate generators
    science_gen = Generator(vocab)
    science_gen.train(science_text, context_length=4, min_count=1)
    
    casual_gen = Generator(vocab)
    casual_gen.train(casual_text, context_length=4, min_count=1)
    
    # Test on appropriate domains
    science_test = "the experiment was conducted".split()
    casual_test = "hey dude lets hang".split()
    
    print("\nScience generator on science text:")
    print(f"  Perplexity: {science_gen.perplexity(science_test, 4):.2f}")
    
    print("\nScience generator on casual text:")
    print(f"  Perplexity: {science_gen.perplexity(casual_test, 4):.2f}")
    
    print("\nCasual generator on casual text:")
    print(f"  Perplexity: {casual_gen.perplexity(casual_test, 4):.2f}")
    
    print("\nCasual generator on science text:")
    print(f"  Perplexity: {casual_gen.perplexity(science_test, 4):.2f}")
    
    # Composed generator (hybrid)
    hybrid_gen = science_gen.compose(casual_gen)
    
    print("\nHybrid generator on science text:")
    print(f"  Perplexity: {hybrid_gen.perplexity(science_test, 4):.2f}")
    
    print("\nHybrid generator on casual text:")
    print(f"  Perplexity: {hybrid_gen.perplexity(casual_test, 4):.2f}")


def example_robust_generation():
    """
    Show robustness to noise and rare events.
    """
    print("\n" + "=" * 80)
    print("ROBUSTNESS DEMONSTRATION")
    print("=" * 80)
    
    # Create noisy dataset
    clean_pattern = "the cat sat on the mat"
    
    data = []
    for _ in range(50):
        data.extend(clean_pattern.split())
    
    # Add noise
    noise_words = ["xyzzy", "plugh", "frobozz"]
    for _ in range(10):
        data.extend(noise_words)
    
    vocab = sorted(set(data))
    
    # Train without filtration
    gen_noisy = Generator(vocab)
    gen_noisy.train(data, context_length=3, min_count=1)
    
    # Train with filtration
    gen_clean = InformationFilter.filter_generator(
        gen_noisy, data,
        context_length=3,
        mdl_percentile=60,
        use_spectral=True
    )
    
    # Test on clean data
    test = "the cat sat on the mat".split()
    
    print(f"\nNoisy generator:")
    print(f"  States: {len(gen_noisy.states)}")
    print(f"  Perplexity: {gen_noisy.perplexity(test, 3):.2f}")
    
    print(f"\nFiltered generator:")
    print(f"  States: {len(gen_clean.states)}")
    print(f"  Perplexity: {gen_clean.perplexity(test, 3):.2f}")
    
    print("\nGeneration from noisy generator:")
    print(" ".join(gen_noisy.generate(seed=42, length=15, temperature=0.8)))
    
    print("\nGeneration from filtered generator:")
    print(" ".join(gen_clean.generate(seed=42, length=15, temperature=0.8)))


if __name__ == "__main__":
    print("ADVANCED EXAMPLES FOR UNIVERSAL GENERATOR FRAMEWORK")
    print("=" * 80)
    
    example_long_context()
    example_temperature_sampling()
    example_hierarchical_composition()
    example_compression_quality()
    example_adaptive_generation()
    example_robust_generation()
    
    print("\n" + "=" * 80)
    print("ALL ADVANCED EXAMPLES COMPLETE")
    print("=" * 80)
