"""
Hierarchical Predictive Coding Implementation
Implements the error minimization dynamics for inference.
"""

import numpy as np
from typing import List, Tuple, Optional, Callable, Dict


class PredictiveCodingLayer:
    """Single layer in hierarchical predictive coding network."""
    
    def __init__(self,
                 state_dim: int,
                 learning_rate: float = 0.1,
                 precision: float = 1.0,
                 prior_precision: float = 0.01):
        """
        Args:
            state_dim: Dimension of state vector
            learning_rate: Step size for gradient descent
            precision: Π (inverse noise variance)
            prior_precision: Λ^-1 (inverse prior variance)
        """
        self.state_dim = state_dim
        self.learning_rate = learning_rate
        self.precision = precision
        self.prior_precision = prior_precision
        
        # State and prior
        self.state = np.zeros(state_dim)
        self.prior_mean = np.zeros(state_dim)
        
        # Generative model (simple linear for now, can be nonlinear)
        self.W_gen = np.random.randn(state_dim, state_dim) * 0.01
        
    def predict(self, top_down_input: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Generate prediction from current state.
        
        Args:
            top_down_input: Input from level above (if any)
            
        Returns:
            Prediction vector
        """
        # For simplicity, prediction is just a copy of state  
        # (can be made nonlinear with W_gen @ nonlinearity(state))
        prediction = self.state.copy()
        
        if top_down_input is not None:
            # Add top-down influence
            prediction += 0.3 * top_down_input  # Weighted combination
        
        return prediction
    
    def compute_error(self, observation: np.ndarray, prediction: np.ndarray) -> np.ndarray:
        """Compute prediction error."""
        return observation - prediction
    
    def update_state(self,
                    bottom_up_error: np.ndarray,
                    top_down_error: Optional[np.ndarray] = None,
                    hash_coupling: Optional[np.ndarray] = None) -> float:
        """
        Update state via gradient descent on free energy.
        
        Args:
            bottom_up_error: Error from level below
            top_down_error: Error from level above (weighted by gradient)
            hash_coupling: Additional coupling from hash memory
            
        Returns:
            Magnitude of update (for convergence checking)
        """
        # Bottom-up term: -Π * ε
        grad = -self.precision * bottom_up_error
        
        # Top-down term (if exists)
        if top_down_error is not None:
            grad += top_down_error
        
        # Prior term: -Λ^-1 * (s - μ)
        grad -= self.prior_precision * (self.state - self.prior_mean)
        
        # Hash coupling term (if exists)
        if hash_coupling is not None:
            grad -= hash_coupling
        
        # Gradient descent step
        update = self.learning_rate * grad
        self.state += update
        
        return np.linalg.norm(update)
    
    def get_free_energy(self, error: np.ndarray) -> float:
        """Compute free energy contribution from this layer."""
        error_term = 0.5 * self.precision * np.sum(error**2)
        prior_term = 0.5 * self.prior_precision * np.sum((self.state - self.prior_mean)**2)
        return error_term + prior_term


class HierarchicalPredictiveCoding:
    """Multi-layer hierarchical predictive coding network."""
    
    def __init__(self,
                 layer_dims: List[int],
                 learning_rate: float = 0.1,
                 precisions: Optional[List[float]] = None):
        """
        Args:
            layer_dims: Dimensions for each layer (bottom to top)
            learning_rate: Learning rate for all layers
            precisions: Precision for each layer (if None, all 1.0)
        """
        self.num_layers = len(layer_dims)
        self.layer_dims = layer_dims
        
        if precisions is None:
            precisions = [1.0] * self.num_layers
        
        # Create layers
        self.layers = [
            PredictiveCodingLayer(
                state_dim=dim,
                learning_rate=learning_rate,
                precision=precisions[i]
            )
            for i, dim in enumerate(layer_dims)
        ]
        
        # Store errors for each layer
        self.errors = [np.zeros(dim) for dim in layer_dims]
        self.predictions = [np.zeros(dim) for dim in layer_dims]
    
    def initialize_from_observation(self, observation: np.ndarray):
        """Initialize all layers from bottom-up observation."""
        # Set bottom layer to observation
        if len(observation) != self.layer_dims[0]:
            raise ValueError(f"Observation dim {len(observation)} doesn't match layer 0 dim {self.layer_dims[0]}")
        
        self.layers[0].state = observation.copy()
        
        # Initialize higher layers with random states (will be refined during inference)
        for i in range(1, self.num_layers):
            # Initialize with small random values
            self.layers[i].state = np.random.randn(self.layer_dims[i]) * 0.01
    
    def forward_pass(self) -> List[np.ndarray]:
        """
        Compute predictions at all layers (top-down).
        
        Returns:
            List of predictions for each layer
        """
        predictions = []
        
        # Each layer predicts its own state (no cross-layer prediction for different dims)
        for i in range(self.num_layers):
            pred = self.layers[i].predict()
            predictions.append(pred)
        
        self.predictions = predictions
        return predictions
    
    def compute_errors(self, observations: List[np.ndarray]) -> List[np.ndarray]:
        """
        Compute prediction errors at all layers.
        
        Args:
            observations: Observations for each layer (usually just bottom layer)
            
        Returns:
            List of errors for each layer
        """
        errors = []
        
        for i in range(self.num_layers):
            if i < len(observations) and observations[i] is not None:
                # Have external observation
                error = self.layers[i].compute_error(observations[i], self.predictions[i])
            else:
                # No external observation - use small error to allow state adjustment
                error = np.zeros_like(self.predictions[i])
            
            errors.append(error)
        
        self.errors = errors
        return errors
    
    def backward_pass(self, hash_couplings: Optional[List[np.ndarray]] = None) -> float:
        """
        Update states via backpropagation of errors.
        
        Args:
            hash_couplings: Optional coupling terms from hash memory for each layer
            
        Returns:
            Total magnitude of updates (for convergence check)
        """
        total_update = 0.0
        
        # Update each layer independently (simplified for different dimensions)
        for i in range(self.num_layers):
            bottom_up_error = self.errors[i]
            
            # Hash coupling (if provided)
            hash_coupling = hash_couplings[i] if hash_couplings else None
            
            # Update (no top-down error since dimensions may differ)
            update_mag = self.layers[i].update_state(
                bottom_up_error,
                top_down_error=None,
                hash_coupling=hash_coupling
            )
            total_update += update_mag
        
        return total_update
    
    def inference_step(self,
                      observations: List[np.ndarray],
                      hash_couplings: Optional[List[np.ndarray]] = None) -> Tuple[float, float]:
        """
        Single iteration of inference.
        
        Returns:
            (free_energy, update_magnitude)
        """
        # Forward pass: compute predictions
        self.forward_pass()
        
        # Compute errors
        self.compute_errors(observations)
        
        # Compute free energy
        free_energy = sum(
            layer.get_free_energy(error)
            for layer, error in zip(self.layers, self.errors)
        )
        
        # Backward pass: update states
        update_mag = self.backward_pass(hash_couplings)
        
        return free_energy, update_mag
    
    def run_inference(self,
                     observations: List[np.ndarray],
                     max_iterations: int = 100,
                     convergence_threshold: float = 1e-4,
                     hash_couplings_fn: Optional[Callable] = None,
                     verbose: bool = False) -> Dict:
        """
        Run inference to convergence.
        
        Args:
            observations: External observations (usually just bottom layer)
            max_iterations: Maximum iterations
            convergence_threshold: Convergence criterion
            hash_couplings_fn: Function that takes current states and returns coupling terms
            verbose: Print progress
            
        Returns:
            Dictionary with results
        """
        # Initialize
        if observations[0] is not None:
            self.initialize_from_observation(observations[0])
        
        # Track convergence
        free_energies = []
        update_magnitudes = []
        
        for iteration in range(max_iterations):
            # Get hash couplings if function provided
            hash_couplings = None
            if hash_couplings_fn is not None:
                current_states = [layer.state for layer in self.layers]
                hash_couplings = hash_couplings_fn(current_states)
            
            # Inference step
            fe, update_mag = self.inference_step(observations, hash_couplings)
            
            free_energies.append(fe)
            update_magnitudes.append(update_mag)
            
            if verbose and iteration % 10 == 0:
                print(f"Iteration {iteration}: F={fe:.4f}, |update|={update_mag:.4f}")
            
            # Check convergence
            if update_mag < convergence_threshold:
                if verbose:
                    print(f"Converged at iteration {iteration}")
                break
        
        return {
            'converged': update_mag < convergence_threshold,
            'iterations': iteration + 1,
            'final_free_energy': free_energies[-1],
            'free_energy_history': np.array(free_energies),
            'update_history': np.array(update_magnitudes),
            'final_states': [layer.state.copy() for layer in self.layers],
            'final_errors': [e.copy() for e in self.errors]
        }
    
    def get_state(self, level: int) -> np.ndarray:
        """Get state at specified level."""
        return self.layers[level].state.copy()


if __name__ == "__main__":
    # Test hierarchical predictive coding
    print("Testing Hierarchical Predictive Coding\n")
    
    # Create 3-level hierarchy
    layer_dims = [128, 64, 32]  # Bottom to top
    hpc = HierarchicalPredictiveCoding(
        layer_dims,
        learning_rate=0.1,
        precisions=[1.0, 0.5, 0.1]  # Higher precision at lower levels
    )
    
    # Create synthetic observation
    observation = np.random.randn(128)
    observations = [observation, None, None]  # Only observe bottom layer
    
    # Run inference
    print("Running inference without hash coupling...")
    results = hpc.run_inference(observations, max_iterations=50, verbose=True)
    
    print(f"\nResults:")
    print(f"  Converged: {results['converged']}")
    print(f"  Iterations: {results['iterations']}")
    print(f"  Final free energy: {results['final_free_energy']:.4f}")
    
    # Test with hash coupling
    print("\n" + "="*60)
    print("Testing with simulated hash coupling\n")
    
    def mock_hash_coupling(states):
        """Simulate hash memory providing coupling terms."""
        # Simulate pulling states toward some "retrieved memory"
        retrieved_memory = np.random.randn(128) * 0.5
        
        couplings = [
            0.1 * (retrieved_memory - states[0]),  # Pull level 0 toward memory
            np.zeros_like(states[1]),  # No coupling at level 1
            np.zeros_like(states[2])   # No coupling at level 2
        ]
        return couplings
    
    # Reset and run with coupling
    observation2 = np.random.randn(128)
    observations2 = [observation2, None, None]
    
    print("Running inference WITH hash coupling...")
    results2 = hpc.run_inference(
        observations2,
        max_iterations=50,
        hash_couplings_fn=mock_hash_coupling,
        verbose=True
    )
    
    print(f"\nResults with coupling:")
    print(f"  Converged: {results2['converged']}")
    print(f"  Iterations: {results2['iterations']}")
    print(f"  Final free energy: {results2['final_free_energy']:.4f}")
    
    # Compare convergence
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(results['free_energy_history'], label='Without coupling')
    plt.plot(results2['free_energy_history'], label='With coupling')
    plt.xlabel('Iteration')
    plt.ylabel('Free Energy')
    plt.legend()
    plt.title('Free Energy Convergence')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.semilogy(results['update_history'], label='Without coupling')
    plt.semilogy(results2['update_history'], label='With coupling')
    plt.xlabel('Iteration')
    plt.ylabel('Update Magnitude (log scale)')
    plt.legend()
    plt.title('Update Magnitude')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('/home/claude/predictive_coding_test.png', dpi=150)
    print("\nPlot saved to predictive_coding_test.png")
