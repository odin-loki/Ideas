import math
from typing import List, Callable
from collections import deque

class SimpleTests:
    """Fast, simple statistical tests for verification."""
    
    @staticmethod
    def quick_entropy(data: int, bits: int = 64) -> float:
        """Quick entropy estimation of bits."""
        ones = bin(data).count('1')
        p = ones / bits
        if p == 0 or p == 1:
            return 0.0
        return -p * math.log2(p) - (1-p) * math.log2(1-p)
    
    @staticmethod
    def runs_test(data: List[int], samples: int = 1000) -> bool:
        """Quick runs test on bit sequence."""
        bits = ''.join(bin(x)[2:].zfill(64) for x in data[:samples])
        runs = 1
        for i in range(1, len(bits)):
            if bits[i] != bits[i-1]:
                runs += 1
        expected = len(bits)/2
        return 0.9 < (runs/expected) < 1.1
    
    @staticmethod
    def quick_correlation(x: int, y: int) -> float:
        """Fast correlation check between consecutive numbers."""
        return bin(x ^ y).count('1') / 64.0

class TranscendentalGenerator:
    """Pure mathematical transcendental sequence generation."""
    
    def __init__(self, terms: int = 10):
        self.terms = terms
        
    def pi_series(self, x: float) -> float:
        """π series using Leibniz formula."""
        return sum((-1)**n / (2*n + 1) * x**(2*n + 1) 
                  for n in range(self.terms))
    
    def e_series(self, x: float) -> float:
        """e series using Taylor expansion."""
        return sum(x**n / math.factorial(n) 
                  for n in range(self.terms))
    
    def sqrt2_series(self, x: float) -> float:
        """√2 series using binomial expansion."""
        return sum((-1)**n * math.comb(2*n, n) / (1 - 2*n) * (x-1)**n 
                  for n in range(self.terms))
    
    def phi_series(self, x: float) -> float:
        """φ (golden ratio) series."""
        return sum(((1 + math.sqrt(5))/2)**n * x/n if n > 0 else x 
                  for n in range(self.terms))
    
    def zeta3_series(self, x: float) -> float:
        """ζ(3) (Apéry's constant) series."""
        return sum(1/(n**3) * x**n 
                  for n in range(1, self.terms))
    
    def gamma_series(self, x: float) -> float:
        """γ (Euler-Mascheroni) series approximation."""
        return sum(1/n - math.log(1 + 1/n) * x**n 
                  for n in range(1, self.terms))
    
    def catalan_series(self, x: float) -> float:
        """Catalan constant series."""
        return sum((-1)**n/(2*n + 1)**2 * x**n 
                  for n in range(self.terms))
    
    def glaisher_series(self, x: float) -> float:
        """Glaisher-Kinkelin constant series approximation."""
        return sum(math.log(n)/n * x**n 
                  for n in range(1, self.terms))

class MetaNode:
    """Core node implementing meta-operations."""
    
    def __init__(self, seed: int = 0):
        self.state = seed
        self.meta_state = seed ^ 0xC6BC279692B5C323
        self.counter = 0
        self.trans = TranscendentalGenerator()
    
    def _get_transcendental(self, index: int) -> float:
        """Get transcendental sequence value."""
        x = self.counter / 1000.0  # Scale for better convergence
        sequences = [
            self.trans.pi_series,
            self.trans.e_series,
            self.trans.sqrt2_series,
            self.trans.phi_series,
            self.trans.zeta3_series,
            self.trans.gamma_series,
            self.trans.catalan_series,
            self.trans.glaisher_series
        ]
        return sequences[index % len(sequences)](x)
    
    def _select_operation(self) -> Callable[[int], int]:
        """Meta-operation selection based on state."""
        op_index = self.meta_state & 0x7
        shift = (self.state & 0x3F)
        mask = 0xFFFFFFFFFFFFFFFF
        
        operations = [
            lambda x: (x << shift) & mask,
            lambda x: x * ((self.state | 0xFF) & mask),
            lambda x: x ^ (x >> (self.state & 0x7)),
            lambda x: (x + ((self.state << 3) | 1)) & mask,
            lambda x: (x >> 13) ^ (x << 17) & mask,
            lambda x: (x * 0xC6BC279692B5C323) & mask,
            lambda x: x ^ ((x << 7) | (x >> 5)) & mask,
            lambda x: (x + (x >> ((self.state & 0x3) + 1))) & mask
        ]
        return operations[op_index]
    
    def update(self, prev_states: List[int]) -> int:
        """Core state update using transcendental mixing."""
        x = 0
        # Mix all transcendental sequences
        for i in range(8):  # Use all 8 sequences
            val = int(self._get_transcendental(i) * 2**64) & 0xFFFFFFFFFFFFFFFF
            op = self._select_operation()
            x ^= op(val)
        
        # Counter evolution
        self.counter = (self.counter + 1) & 0xFFFFFFFFFFFFFFFF
        x ^= self.counter
        
        # Meta-state evolution
        self.meta_state = x ^ (self.meta_state >> 11)
        
        # Mix with previous states
        for prev in prev_states:
            op = self._select_operation()
            x = op(x ^ prev)
        
        self.state = x
        return x

class MetaDAG:
    """Directed Acyclic Graph of meta-nodes with simple testing."""
    
    def __init__(self, num_nodes: int = 8, seed: int = 0):
        self.nodes = [MetaNode(seed + i) for i in range(num_nodes)]
        self.paths = self._generate_paths(num_nodes)
        self.tests = SimpleTests()
        self.last_output = 0
        self.outputs = deque(maxlen=1000)  # Keep last 1000 outputs for tests
    
    def _generate_paths(self, num_nodes: int) -> List[List[int]]:
        """Generate DAG paths."""
        return [[(i + j) % num_nodes for j in range(1, 4)]
                for i in range(num_nodes)]
    
    def _evolve_paths(self) -> None:
        """Path evolution based on node states."""
        for i, node in enumerate(self.nodes):
            self.paths[i] = [(x + (node.state & 0x7)) % len(self.nodes) 
                            for x in self.paths[i]]
    
    def get_next(self) -> int:
        """Generate next random number with simple health checks."""
        new_states = []
        
        # Update nodes
        for i, node in enumerate(self.nodes):
            prev_states = [self.nodes[p].state for p in self.paths[i]]
            new_state = node.update(prev_states)
            new_states.append(new_state)
        
        # Evolve paths
        self._evolve_paths()
        
        # Mix final output
        result = new_states[0]
        for state in new_states[1:]:
            result = (result ^ state) & 0xFFFFFFFFFFFFFFFF
            
        # Quick health checks
        entropy = self.tests.quick_entropy(result)
        correlation = self.tests.quick_correlation(result, self.last_output)
        
        # Only warn on severe issues
        if entropy < 0.5:
            print(f"Warning: Low entropy detected: {entropy:.3f}")
        if correlation < 0.2:
            print(f"Warning: High correlation detected: {correlation:.3f}")
        
        self.last_output = result
        self.outputs.append(result)
        return result
    
    def get_stats(self) -> dict:
        """Get simple statistical overview."""
        if len(self.outputs) < 10:
            return {"status": "Need more samples"}
            
        return {
            "samples": len(self.outputs),
            "avg_entropy": sum(self.tests.quick_entropy(n) for n in self.outputs)/len(self.outputs),
            "runs_test_pass": self.tests.runs_test(list(self.outputs)),
            "unique_ratio": len(set(self.outputs))/len(self.outputs)
        }

def test_rng(samples: int = 1000):
    """Test RNG with statistics."""
    # Initialize RNG
    rng = MetaDAG(num_nodes=8, seed=12345)
    
    # Generate numbers
    print("Generating random numbers...")
    for _ in range(samples):
        rng.get_next()
    
    # Get stats
    stats = rng.get_stats()
    print("\nStatistical Overview:")
    print(f"Samples: {stats['samples']}")
    print(f"Average Entropy: {stats['avg_entropy']:.3f}")
    print(f"Runs Test Pass: {stats['runs_test_pass']}")
    print(f"Unique Ratio: {stats['unique_ratio']:.3f}")
    
    # Sample outputs
    print("\nSample Outputs:")
    sample = list(rng.outputs)[-5:]
    for i, num in enumerate(sample):
        print(f"Random {i}: 0x{num:016x}")

if __name__ == "__main__":
    test_rng()