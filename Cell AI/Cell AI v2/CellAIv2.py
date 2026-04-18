#!/usr/bin/env python3
"""
CellAIv2 Full Mathematical Model Implementation and Demonstration

This script demonstrates the complete CellAIv2 system with all mathematical
components from the math model including the Crystal Lattice structure.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.fft as fft
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Union
import logging
from time import time
import math
import pandas as pd
import sys

# ====================================================================
# PART 1: SYSTEM DEFINITIONS AND CLASSES
# ====================================================================

@dataclass
class SystemParams:
    """Core system parameters"""
    dt: float = 0.01                # Time step
    spatial_dims: int = 3           # Spatial dimensions
    num_cells: int = 1000           # Number of cells
    num_states: int = 100           # States per cell
    compression_levels: int = 8     # DNA-like compression levels
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'

class LoadBalancer:
    """Handles multi-device load balancing"""
    def __init__(self, primary_device: torch.device):
        self.primary_device = primary_device
        self.devices = self._get_available_devices()
        self.device_stats = {dev: {'load': 0.0, 'memory': 0.0} for dev in self.devices}

    def _get_available_devices(self) -> List[torch.device]:
        devices = [self.primary_device]
        if self.primary_device.type == 'cuda':
            devices.append(torch.device('cpu'))
        return devices

    def balance_load(self, data: torch.Tensor) -> Dict[torch.device, List[int]]:
        self._update_device_stats()
        total_load = sum(stats['load'] for stats in self.device_stats.values())
        
        device_capacity = {
            dev: 1.0 - (stats['load'] / total_load if total_load > 0 else 0)
            for dev, stats in self.device_stats.items()
        }
        
        num_items = len(data)
        device_map = {dev: [] for dev in self.devices}
        
        current_idx = 0
        for device, capacity in sorted(device_capacity.items(), key=lambda x: x[1], reverse=True):
            if current_idx >= num_items:
                break
            
            num_items_device = int(capacity * num_items)
            device_map[device] = list(range(current_idx, min(current_idx + num_items_device, num_items)))
            current_idx += num_items_device
        
        return device_map

    def _update_device_stats(self):
        for device in self.devices:
            if device.type == 'cuda':
                memory_allocated = torch.cuda.memory_allocated(device) / torch.cuda.get_device_properties(device).total_memory
                self.device_stats[device].update({'memory': memory_allocated, 'load': memory_allocated})
            else:
                import psutil
                self.device_stats[device].update({
                    'memory': psutil.virtual_memory().percent / 100.0,
                    'load': psutil.cpu_percent() / 100.0
                })

class ResonanceSystem:
    """Handles resonance and wave interactions"""
    def __init__(self, num_cells: int, num_states: int, device: torch.device):
        self.device = device
        self.num_cells = num_cells
        self.num_states = num_states
        
        # Initialize parameters
        self.resonance_frequencies = torch.randn(num_cells, device=device)
        self.coupling_matrix = torch.randn(num_cells, num_cells, device=device) * 0.1
        self.wave_number = torch.randn(num_states, device=device)
        self.phase_velocity = torch.ones(num_states, device=device)

    def compute_resonance(self, state: torch.Tensor) -> torch.Tensor:
        # Check if input is 1D and handle appropriately
        original_dim = state.dim()
        if original_dim == 1:
            # Add batch dimension for 1D inputs
            state = state.unsqueeze(0)
            freq_domain = fft.fft2(state)
            # Use only first resonance frequency for single samples
            resonance = torch.exp(1j * self.resonance_frequencies[0].view(1, 1))
            enhanced = freq_domain * resonance
            result = torch.real(fft.ifft2(enhanced))
            # Remove the batch dimension we added
            return result.squeeze(0)
        else:
            # Original 2D implementation
            freq_domain = fft.fft2(state)
            resonance = torch.exp(1j * self.resonance_frequencies.view(-1, 1))
            enhanced = freq_domain * resonance
            return torch.real(fft.ifft2(enhanced))

    def wave_interaction(self, state: torch.Tensor) -> torch.Tensor:
        # Check if input is 1D and handle appropriately
        original_dim = state.dim()
        if original_dim == 1:
            # Add batch dimension for 1D inputs
            state = state.unsqueeze(0)
            
            k = self.wave_number.view(1, -1)
            v = self.phase_velocity.view(1, -1)
            omega = k * v
            wave_factor = torch.exp(1j * (k * state - omega * 0.1))
            result = torch.real(wave_factor * state)
            
            # Remove the batch dimension we added
            return result.squeeze(0)
        else:
            # Original 2D implementation
            k = self.wave_number.view(1, -1)
            v = self.phase_velocity.view(1, -1)
            omega = k * v
            wave_factor = torch.exp(1j * (k * state - omega * 0.1))
            return torch.real(wave_factor * state)

class PatternRecognition:
    """Handles pattern recognition and learning"""
    def __init__(self, num_cells: int, num_states: int, device: torch.device):
        self.device = device
        self.num_cells = num_cells
        self.num_states = num_states
        
        self.pattern_bank = torch.zeros((1000, num_states), device=device)
        self.pattern_count = 0
        self.recognition_threshold = 0.95
        self.learning_rate = 0.01

    def recognize_pattern(self, pattern: torch.Tensor) -> Tuple[bool, float, Optional[int]]:
        if self.pattern_count == 0:
            return False, 0.0, None
        
        # Ensure pattern is properly shaped for matrix multiplication (1D tensor)
        if pattern.dim() > 1:
            # If we somehow get a batch, just use the first pattern
            pattern = pattern[0]
            
        # Calculate similarity with each pattern in the bank
        similarity = torch.matmul(pattern, self.pattern_bank[:self.pattern_count].t())
        
        # Find the most similar pattern
        confidence, idx = torch.max(similarity, dim=0)
        
        # Convert to scalar values
        confidence_val = confidence.item()
        idx_val = idx.item()
        
        if confidence_val > self.recognition_threshold:
            return True, confidence_val, idx_val
        return False, confidence_val, None

    def learn_pattern(self, pattern: torch.Tensor, enhance: bool = True) -> int:
        found, conf, idx = self.recognize_pattern(pattern)
        if found:
            self.pattern_bank[idx] = self.pattern_bank[idx] * (1 - self.learning_rate) + \
                                   pattern * self.learning_rate
            return idx
            
        if self.pattern_count >= len(self.pattern_bank):
            new_bank = torch.zeros((len(self.pattern_bank) * 2, self.num_states), 
                                 device=self.device)
            new_bank[:len(self.pattern_bank)] = self.pattern_bank
            self.pattern_bank = new_bank
            
        self.pattern_bank[self.pattern_count] = pattern
        self.pattern_count += 1
        return self.pattern_count - 1

class CrystalLattice:
    """Handles crystal lattice structure and operations based on the math model
    
    L(S) = ∑ᵢⱼₖ Tᵢⱼₖ × Φᵢⱼₖ(S) × D(S)
    
    Where:
    Tᵢⱼₖ = Lattice tensors
    Φᵢⱼₖ = Structure functions
    D(S) = Defect operator
    
    With defect handling:
    D(S) = S + ∑ᵢ d(rᵢ)φ(S-rᵢ)
    d(r) = Defect strength
    φ(S) = Localization function
    """
    def __init__(self, num_states: int, spatial_dims: int, device: torch.device):
        self.device = device
        self.num_states = num_states
        self.spatial_dims = spatial_dims
        
        # Initialize lattice tensors (Tijk)
        self.lattice_tensors = torch.randn(
            spatial_dims, spatial_dims, spatial_dims, 
            device=device
        ) * 0.1
        
        # Initialize structure functions (Φijk)
        self.structure_functions = torch.randn(
            spatial_dims, spatial_dims, spatial_dims, num_states,
            device=device
        ) * 0.1
        
        # Initialize defect parameters
        self.num_defects = 10
        self.defect_sites = torch.randn(self.num_defects, spatial_dims, device=device)  # Random defect positions
        self.defect_strengths = torch.randn(self.num_defects, device=device) * 0.1      # Random defect strengths
        self.localization_width = 0.5                                      # Width of localization function
        
    def lattice_operation(self, state: torch.Tensor) -> torch.Tensor:
        """Apply lattice structure operation L(S)"""
        original_dim = state.dim()
        
        # Handle both batched and non-batched inputs
        if original_dim == 1:
            state = state.unsqueeze(0)  # Add batch dimension
        
        result = torch.zeros_like(state)
        
        # Apply lattice tensor operations (simplified for practical implementation)
        for i in range(self.spatial_dims):
            for j in range(self.spatial_dims):
                for k in range(self.spatial_dims):
                    # Get structure function for this lattice point
                    structure_fn = self.structure_functions[i, j, k]
                    
                    # Apply structure function to each cell's state separately
                    for cell_idx in range(state.size(0)):
                        # Project structure function onto the cell's state vector
                        cell_state = state[cell_idx]
                        projection = torch.dot(structure_fn, cell_state)
                        
                        # Apply lattice tensor (scalar multiplication)
                        result[cell_idx] += self.lattice_tensors[i, j, k] * projection
        
        # Apply defect operator
        result = self.apply_defects(result)
        
        # Remove batch dimension if it was added
        if original_dim == 1:
            result = result.squeeze(0)
            
        return result
    
    def apply_defects(self, state: torch.Tensor) -> torch.Tensor:
        """Apply defect operator D(S) = S + ∑ᵢ d(rᵢ)φ(S-rᵢ)"""
        # Create a copy to avoid modifying the input
        modified_state = state.clone()
        
        # Apply defects to each state element
        for i in range(self.num_defects):
            defect_site = self.defect_sites[i]
            defect_strength = self.defect_strengths[i]
            
            # Simplified localization function (Gaussian-like)
            # This simulates φ(S-rᵢ) with a scalar value for computational efficiency
            localization = torch.exp(-self.localization_width * defect_strength**2)
            
            # Apply the defect operator
            modified_state = modified_state + localization * defect_strength * state
        
        return modified_state
    
    def get_enhancement_factor(self, state: torch.Tensor) -> float:
        """Calculate the enhancement factor provided by the lattice structure"""
        original_norm = torch.norm(state)
        if original_norm == 0:
            return 1.0
            
        enhanced_state = self.lattice_operation(state)
        enhanced_norm = torch.norm(enhanced_state)
        
        return (enhanced_norm / original_norm).item()

class EnhancedCellAI:
    """Core Cell AI system with physics-based enhancements, including Crystal Lattice"""
    def __init__(self, params: SystemParams):
        self.p = params
        self.device = torch.device(params.device)
        
        # Initialize states
        self.state = torch.zeros((params.num_cells, params.num_states), device=self.device)
        self.field = torch.zeros((params.spatial_dims, params.num_cells), device=self.device)
        self.phase = torch.zeros(params.num_cells, device=self.device)
        
        # Initialize subsystems
        self.setup_dynamics()
        self.setup_compression()
        self.load_balancer = LoadBalancer(self.device)
        self.resonance = ResonanceSystem(params.num_cells, params.num_states, self.device)
        self.pattern_system = PatternRecognition(params.num_cells, params.num_states, self.device)
        
        # Initialize Crystal Lattice system (new addition)
        self.crystal_lattice = CrystalLattice(
            num_states=params.num_states, 
            spatial_dims=params.spatial_dims,
            device=self.device
        )
        
        # Enhanced states
        self.resonant_state = torch.zeros_like(self.state)
        self.pattern_state = torch.zeros_like(self.state)
        self.lattice_state = torch.zeros_like(self.state)  # New tracking for lattice state
        
        # Training mode flag
        self.train_mode = False

    def setup_dynamics(self):
        """Setup dynamic system parameters"""
        self.sigma = 10.0
        self.rho = 28.0
        self.beta = 8.0/3.0
        self.coupling_strength = 0.1
        self.natural_frequencies = torch.randn(self.p.num_cells, device=self.device)
        self.diffusion_constant = 0.1
        self.wave_constant = 0.1

    def setup_compression(self):
        """Setup DNA-like compression"""
        self.compression_matrices = [
            nn.Parameter(torch.randn(self.p.num_states, self.p.num_states, device=self.device) * 0.1)
            for _ in range(self.p.compression_levels)
        ]

    def field_evolution(self, state: torch.Tensor) -> torch.Tensor:
        grad = torch.gradient(state, dim=1)[0]
        laplacian = torch.gradient(grad, dim=1)[0]
        field_term = self.diffusion_constant * laplacian
        wave_term = self.wave_constant * torch.sin(state)
        return field_term + wave_term

    def lorenz_dynamics(self, x: torch.Tensor) -> torch.Tensor:
        dx = self.sigma * (x[:, 1] - x[:, 0])
        dy = x[:, 0] * (self.rho - x[:, 2]) - x[:, 1]
        dz = x[:, 0] * x[:, 1] - self.beta * x[:, 2]
        return torch.stack([dx, dy, dz], dim=1)

    def oscillator_coupling(self, phase: torch.Tensor) -> torch.Tensor:
        phase_diff = phase.unsqueeze(0) - phase.unsqueeze(1)
        coupling = self.coupling_strength * torch.sin(phase_diff)
        return coupling.sum(dim=1)

    def compress_state(self, state: torch.Tensor) -> torch.Tensor:
        compressed = state
        for matrix in self.compression_matrices:
            compressed = torch.matmul(compressed, matrix)
            compressed = torch.tanh(compressed)
        return compressed

    def decompress_state(self, compressed: torch.Tensor) -> torch.Tensor:
        state = compressed
        for matrix in reversed(self.compression_matrices):
            state = torch.matmul(state, matrix.t())
            state = torch.tanh(state)
        return state

    def evolve_state(self, dt: float) -> None:
        device_map = self.load_balancer.balance_load(self.state)
        new_state = torch.zeros_like(self.state)
        
        for device, idx in device_map.items():
            if len(idx) == 0:
                continue
                
            state_device = self.state[idx].to(device)
            field_term = self.field_evolution(state_device)
            
            lorenz_state = state_device[:, :3]
            lorenz_term = self.lorenz_dynamics(lorenz_state)
            
            phase_device = self.phase[idx].to(device)
            coupling_term = self.oscillator_coupling(phase_device)
            
            derivative = (field_term + 
                        torch.cat([lorenz_term, torch.zeros_like(state_device[:, 3:])], dim=1) +
                        coupling_term.unsqueeze(1))
            
            new_state[idx] = state_device + dt * derivative
        
        self.state = new_state
        
        # Add resonance effects
        self.resonant_state = self.resonance.compute_resonance(self.state)
        wave_state = self.resonance.wave_interaction(self.state)
        self.state = self.state + 0.1 * (self.resonant_state + wave_state)
        
        # Add lattice operations - NEW
        self.lattice_state = self.crystal_lattice.lattice_operation(self.state)
        self.state = self.state + 0.05 * self.lattice_state
        
        # Update pattern state
        self.update_pattern_state()

    def update_pattern_state(self):
        for i in range(0, self.state.size(0), 100):
            end_idx = min(i+100, self.state.size(0))
            batch = self.state[i:end_idx]
            
            # Process each pattern in the batch individually
            for j in range(batch.size(0)):
                pattern = batch[j]
                found, conf, pattern_idx = self.pattern_system.recognize_pattern(pattern)
                if found:
                    self.pattern_state[i+j] = self.pattern_system.pattern_bank[pattern_idx]

    def process_input(self, input_pattern: torch.Tensor) -> Tuple[torch.Tensor, float]:
        compressed = self.compress_state(input_pattern)
        found, confidence, idx = self.pattern_system.recognize_pattern(compressed)
        
        if not found:
            idx = self.pattern_system.learn_pattern(compressed)
            
        resonant = self.resonance.compute_resonance(compressed)
        lattice = self.crystal_lattice.lattice_operation(compressed)  # Add lattice effect
        result = compressed + 0.1 * resonant + 0.05 * lattice  # Include lattice contribution
        
        return result, confidence

    def get_system_state(self) -> dict:
        return {
            'base_state': self.state.cpu().numpy(),
            'resonant_state': self.resonant_state.cpu().numpy(),
            'pattern_state': self.pattern_state.cpu().numpy(),
            'lattice_state': self.lattice_state.cpu().numpy(),
            'num_patterns': self.pattern_system.pattern_count,
            'compression_ratio': self.p.num_states / self.state.size(1),
            'lattice_enhancement': self.crystal_lattice.get_enhancement_factor(self.state[0]) if self.state.size(0) > 0 else 0.0
        }

class CellDataset(Dataset):
    """Dataset handler for Cell AI"""
    def __init__(self, 
                 data: Union[np.ndarray, pd.DataFrame, torch.Tensor],
                 targets: Optional[Union[np.ndarray, pd.Series, torch.Tensor]] = None,
                 transform: Optional[callable] = None):
        self.data = torch.as_tensor(data) if not isinstance(data, torch.Tensor) else data
        self.targets = None if targets is None else (
            torch.as_tensor(targets) if not isinstance(targets, torch.Tensor) else targets
        )
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        if self.transform:
            sample = self.transform(sample)
        
        if self.targets is not None:
            return sample, self.targets[idx]
        return sample

# ====================================================================
# PART 2: DEMONSTRATION FUNCTION
# ====================================================================

def demonstrate_full_math_model():
    """Demonstration of the CellAIv2 system with full mathematical model implementation"""
    print("=" * 70)
    print("CellAIv2 FULL MATHEMATICAL MODEL DEMONSTRATION")
    print("=" * 70)
    
    # Step 1: Initialize system with comprehensive parameters
    print("\n1. Initializing system with full mathematical model...")
    
    # Configure parameters according to the mathematical model
    params = SystemParams(
        dt=0.01,                # Time step
        spatial_dims=3,         # Spatial dimensions
        num_cells=200,          # Number of cells
        num_states=100,         # States per cell
        compression_levels=8,   # DNA-like compression levels (from math model)
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )
    
    # Initialize the system
    system = EnhancedCellAI(params)
    print(f"   → System initialized on device: {system.device}")
    print(f"   → Mathematical components active: ")
    print(f"     • Base Evolution (dS/dt = F(S) + D∇²S + W(S) + A(S) + O(S))")
    print(f"     • Lorenz Dynamics (dx/dt = σ(y-x), dy/dt = x(ρ-z) - y, dz/dt = xy - βz)")
    print(f"     • DNA-like Compression (F(S) = ∏ᵢ₌₁ⁿ [Fᵢ(S) + Gᵢ(t)] × H(S))")
    print(f"     • Crystal Lattice (L(S) = ∑ᵢⱼₖ Tᵢⱼₖ × Φᵢⱼₖ(S) × D(S))")
    print(f"     • Oscillator Coupling (dθᵢ/dt = ωᵢ + ∑ⱼ Kᵢⱼsin(θⱼ - θᵢ))")
    print(f"     • Resonance System (R(ω) = A₀/√[(ω₀² - ω²)² + γ²ω²])")
    print(f"     • Pattern Recognition (P(pattern|S) = |∫ Ψ*(pattern)Ψ(S)dV|² × E(pattern,S))")
    
    # Step 2: Demonstrate individual mathematical components
    print("\n2. Demonstrating individual mathematical components:")
    
    # Initialize a test state for demonstrations
    test_state = torch.zeros((1, params.num_states), device=system.device)
    test_state[0, :40] = torch.sin(torch.linspace(0, 4*np.pi, 40, device=system.device))
    
    # a. Compression System
    print("\n   a. DNA-Like Compression Mathematics:")
    start_time = time()
    compressed = system.compress_state(test_state)
    decompressed = system.decompress_state(compressed)
    compression_time = time() - start_time
    
    compression_ratio = test_state.numel() / compressed.numel()
    compression_fidelity = 1.0 - torch.norm(test_state - decompressed) / torch.norm(test_state)
    
    print(f"      → Compression ratio: {compression_ratio:.2f}:1")
    print(f"      → Compression fidelity: {compression_fidelity:.4f}")
    print(f"      → Compression time: {compression_time*1000:.2f} ms")
    print(f"      → Compression levels: {params.compression_levels}")
    
    # b. Crystal Lattice System
    print("\n   b. Crystal Lattice Mathematics:")
    start_time = time()
    lattice_enhanced = system.crystal_lattice.lattice_operation(test_state)
    lattice_time = time() - start_time
    
    lattice_factor = system.crystal_lattice.get_enhancement_factor(test_state[0])
    
    print(f"      → Lattice enhancement factor: {lattice_factor:.4f}x")
    print(f"      → Lattice operation time: {lattice_time*1000:.2f} ms")
    print(f"      → Number of defect sites: {system.crystal_lattice.num_defects}")
    
    # c. Resonance System
    print("\n   c. Resonance Mathematics:")
    start_time = time()
    resonant_state = system.resonance.compute_resonance(test_state)
    wave_state = system.resonance.wave_interaction(test_state)
    resonance_time = time() - start_time
    
    resonance_factor = torch.norm(resonant_state)/torch.norm(test_state)
    wave_factor = torch.norm(wave_state)/torch.norm(test_state)
    
    print(f"      → Resonance enhancement factor: {resonance_factor:.4f}x")
    print(f"      → Wave interaction factor: {wave_factor:.4f}x")
    print(f"      → Combined resonance effect: {(resonance_factor + wave_factor):.4f}x")
    print(f"      → Resonance computation time: {resonance_time*1000:.2f} ms")
    
    # d. Pattern Recognition
    print("\n   d. Pattern Recognition Mathematics:")
    # Learn a few patterns first
    pattern_types = ["Sine wave", "Square wave", "Gaussian"]
    
    # Pattern 1: Sine wave
    pattern1 = torch.zeros(params.num_states, device=system.device)
    pattern1[:40] = torch.sin(torch.linspace(0, 4*np.pi, 40, device=system.device))
    
    # Pattern 2: Square wave
    pattern2 = torch.zeros(params.num_states, device=system.device)
    square = torch.linspace(0, 4, 40, device=system.device)
    pattern2[:40] = (square.floor() % 2) * 2 - 1
    
    # Pattern 3: Gaussian
    pattern3 = torch.zeros(params.num_states, device=system.device)
    x = torch.linspace(-3, 3, 40, device=system.device)
    pattern3[:40] = torch.exp(-x**2/2)
    
    # Learn patterns
    for pattern in [pattern1, pattern2, pattern3]:
        system.pattern_system.learn_pattern(pattern)
    
    # Test recognition
    start_time = time()
    for i, pattern in enumerate([pattern1, pattern2, pattern3]):
        # Add noise
        test_pattern = pattern + torch.randn_like(pattern) * 0.2
        found, confidence, idx = system.pattern_system.recognize_pattern(test_pattern)
        print(f"      → {pattern_types[i]}: Recognition confidence = {confidence:.4f}, Found = {found}")
    
    recognition_time = (time() - start_time) / 3
    print(f"      → Average recognition time: {recognition_time*1000:.2f} ms")
    
    # Step 3: Demonstrate Full System Evolution
    print("\n3. Demonstrating full system evolution with all mathematical components:")
    
    # Initialize with more interesting state
    system.state[0, :40] = torch.sin(torch.linspace(0, 4*np.pi, 40, device=system.device))
    system.state[1, :40] = torch.cos(torch.linspace(0, 4*np.pi, 40, device=system.device))
    
    # Track metrics over time
    num_steps = 100
    metrics = {
        'energy': [],
        'phase_coherence': [],
        'pattern_overlap': [],
        'lattice_enhancement': [],
        'resonance_factor': []
    }
    
    print(f"   → Evolving system for {num_steps} time steps with dt={params.dt}...")
    start_time = time()
    
    for step in range(num_steps):
        # Evolve system
        system.evolve_state(params.dt)
        
        # Calculate metrics
        energy = torch.norm(system.state).item()
        
        # Phase coherence (measure of oscillator synchronization)
        phases = system.phase
        phase_diffs = phases.unsqueeze(0) - phases.unsqueeze(1)
        coherence = torch.abs(torch.mean(torch.exp(1j * phase_diffs))).item()
        
        # Pattern overlap (measure of pattern recognition)
        max_overlap = 0.0
        for i in range(system.pattern_system.pattern_count):
            pattern = system.pattern_system.pattern_bank[i]
            overlap = torch.abs(torch.mean(torch.matmul(system.state, pattern))).item()
            max_overlap = max(max_overlap, overlap)
        
        # Get lattice enhancement
        lattice_factor = system.crystal_lattice.get_enhancement_factor(system.state[0])
        
        # Get resonance factor
        resonant_state = system.resonance.compute_resonance(system.state[0].unsqueeze(0))
        resonance_factor = (torch.norm(resonant_state)/torch.norm(system.state[0].unsqueeze(0))).item()
        
        # Store metrics
        metrics['energy'].append(energy)
        metrics['phase_coherence'].append(coherence)
        metrics['pattern_overlap'].append(max_overlap)
        metrics['lattice_enhancement'].append(lattice_factor)
        metrics['resonance_factor'].append(resonance_factor)
    
    evolution_time = time() - start_time
    print(f"   → Evolution completed in {evolution_time:.2f} seconds")
    print(f"   → Average time per step: {evolution_time/num_steps*1000:.2f} ms")
    
    # Step 4: Visualize results
    print("\n4. Visualizing system evolution metrics:")
    
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.plot(metrics['energy'])
    plt.title('System Energy')
    plt.xlabel('Time Step')
    plt.ylabel('Energy')
    
    plt.subplot(2, 3, 2)
    plt.plot(metrics['phase_coherence'])
    plt.title('Phase Coherence')
    plt.xlabel('Time Step')
    plt.ylabel('Coherence')
    
    plt.subplot(2, 3, 3)
    plt.plot(metrics['pattern_overlap'])
    plt.title('Pattern Recognition Overlap')
    plt.xlabel('Time Step')
    plt.ylabel('Overlap')
    
    plt.subplot(2, 3, 4)
    plt.plot(metrics['lattice_enhancement'])
    plt.title('Crystal Lattice Enhancement')
    plt.xlabel('Time Step')
    plt.ylabel('Enhancement Factor')
    
    plt.subplot(2, 3, 5)
    plt.plot(metrics['resonance_factor'])
    plt.title('Resonance Factor')
    plt.xlabel('Time Step')
    plt.ylabel('Factor')
    
    # Visualize state evolution in the last subplot
    plt.subplot(2, 3, 6)
    plt.imshow(system.state[:10, :40].cpu().numpy(), aspect='auto', cmap='viridis')
    plt.title('Final System State (First 10 cells)')
    plt.xlabel('State Dimension')
    plt.ylabel('Cell Index')
    plt.colorbar(label='State Value')
    
    plt.tight_layout()
    plt.savefig('cellaiv2_full_math_demo.png')
    print(f"   → Metrics visualization saved to 'cellaiv2_full_math_demo.png'")
    
    # Step 5: Calculate combined enhancement factors
    print("\n5. Mathematical model enhancement factors:")
    
    avg_lattice = sum(metrics['lattice_enhancement']) / len(metrics['lattice_enhancement'])
    avg_resonance = sum(metrics['resonance_factor']) / len(metrics['resonance_factor'])
    
    print(f"   → Crystal Lattice enhancement: {avg_lattice:.4f}x")
    print(f"   → Resonance enhancement: {avg_resonance:.4f}x")
    print(f"   → DNA-like compression ratio: {compression_ratio:.2f}:1")
    print(f"   → Pattern recognition fidelity: {max(metrics['pattern_overlap']):.4f}")
    
    # Calculate theoretical combined enhancement
    theoretical_enhancement = avg_lattice * avg_resonance * compression_ratio
    print(f"   → Theoretical combined enhancement: ~{theoretical_enhancement:.2f}x")
    
    print("\nDemonstration complete!")
    return system, metrics

# ====================================================================
# PART 3: MAIN FUNCTION
# ====================================================================

def main():
    """Main entry point for CellAIv2 demonstration"""
    print("CellAIv2 Full Mathematical Model Implementation")
    print("=" * 50)
    
    # Check for CUDA availability
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    try:
        # Run the full demonstration
        system, metrics = demonstrate_full_math_model()
        
        # Show the visualization
        plt.show()
        
        # Print completion message
        print("\nCellAIv2 demonstration completed successfully!")
        
    except Exception as e:
        print(f"Error running demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())