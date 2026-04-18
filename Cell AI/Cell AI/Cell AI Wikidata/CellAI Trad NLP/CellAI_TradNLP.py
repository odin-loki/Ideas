"""
OptimizedTextCellAI - Full Mathematical Model with Highly Optimized Traditional NLP

This implementation combines:
1. The complete CellAI mathematical framework:
   - Cellular Equation: dS/dt = f(I, S, t) - γS + D∇²S + η(t)
   - Probabilistic State Transitions: P(Si→Sj) = exp(-ΔEij/kT) / Z
   - Temporal Memory Integration: M(t) = ∫[t-τ, t] w(t-s)I(s)ds + ∫[0, t] K(t-s)S(s)ds
   - Detailed Boundary Conditions: B(Sᵢ, Sⱼ) = 0 for adjacent partitions
   - Emergent Properties Framework for collective behavior

2. Highly optimized traditional NLP techniques from the original implementation:
   - Memory-optimized sparse embeddings with separate sparse gradient optimization
   - Optimized LSTM-based encoding/decoding with bidirectional processing
   - Efficient checkpointing for reduced memory usage during backpropagation
   - Memory-mapped dataset handling for large-scale data processing
   - Parallel data loading and preprocessing
   - Batch processing with gradient accumulation
   - Optimized Ray configuration for multicore processing

This implementation maintains the optimization approaches of the original TextCellAI
while adding the full mathematical power of the complete CellAI model.

Usage:
  - Training: python optimized_textcellai.py train --data /path/to/data.jsonl --epochs 3
  - Chat: python optimized_textcellai.py chat --model /path/to/model.pt
  - Benchmark: python optimized_textcellai.py benchmark --model /path/to/model.pt --test /path/to/test.jsonl
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import ray
from dataclasses import dataclass
import logging
import sys
from typing import Dict, List, Tuple, Optional, Any, Union
import time
import json
from transformers import AutoTokenizer
import os
import multiprocessing
import mmap
import argparse
from tqdm import tqdm
from torch.utils.checkpoint import checkpoint
import atexit
import math

# Configure basic logging but filter out Ray's messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a filter to exclude Ray logs
class RayLogsFilter(logging.Filter):
    def filter(self, record):
        # Filter out messages from Ray loggers or containing SIGTERM
        if record.name.startswith('ray') or 'SIGTERM' in record.getMessage():
            return False
        return True

# Apply the filter to the root logger
root_logger = logging.getLogger()
root_logger.addFilter(RayLogsFilter())

# Completely disable Ray's native logging
os.environ["RAY_DISABLE_DOCKER_CPU_WARNING"] = "1"
os.environ["RAY_DEDUP_LOGS"] = "0"
os.environ["RAY_DISABLE_CRASH_REPORTS"] = "1"

@dataclass
class ModelParams:
    """Combined parameters for optimized TextCellAI with full mathematical framework"""
    # Core cellular parameters
    dt: float             # Time step for memory dynamics
    D: float              # Diffusion coefficient for state propagation
    gamma: float          # Decay rate for memory
    eta: float            # Noise amplitude (for η(t))
    num_partitions: int   # Number of parallel partitions
    state_size: int       # Size of state vector per partition
    
    # State transition parameters (CellAI Math)
    temperature: float        # Temperature for Boltzmann distribution (kT)
    energy_scale: float       # Scale factor for energy calculations
    
    # Temporal memory parameters (CellAI Math)
    memory_tau: float         # Memory time constant
    kernel_terms: int         # Number of terms in memory kernel expansion
    kernel_decays: List[float]  # Decay rates for memory kernel terms
    
    # Boundary condition parameters (CellAI Math)
    boundary_strength: float  # Coupling strength at boundaries
    
    # Emergent properties parameters (CellAI Math)
    collective_threshold: float  # Threshold for collective behavior emergence
    
    # NLP parameters
    embedding_size: int       # Size of text embeddings
    vocab_size: int           # Size of vocabulary
    max_seq_length: int       # Maximum sequence length
    
    # Training parameters
    learning_rate: float      # Learning rate for training
    batch_size: int           # Batch size for training
    accumulation_steps: int   # Steps for gradient accumulation
    early_stopping_patience: int  # Patience for early stopping


class TextEncoder(nn.Module):
    """Encodes text into vector representations"""
    def __init__(self, vocab_size: int, embedding_size: int, state_size: int, use_checkpoint: bool = False):
        super().__init__()
        self.use_checkpoint = use_checkpoint
        self.embedding = nn.Embedding(
            vocab_size, 
            embedding_size,
            sparse=True  # Enable sparse gradients for embeddings
        )
        self.encoder = nn.LSTM(
            input_size=embedding_size,
            hidden_size=state_size // 2,  # Bidirectional, so half size
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            proj_size=0,  # Disable projection for speed
        )
        # Handle bidirectional LSTM with 2 layers correctly (4x state_size//2 = 2x state_size)
        self.projection = nn.Linear(state_size * 2, state_size)
        
    def _run_encoder(self, embedded):
        """Helper function for use with checkpoint to avoid keyword arguments"""
        return self.encoder(embedded)
        
    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        """
        Convert token IDs to state vector
        
        Args:
            token_ids: Tensor of shape [batch_size, seq_len]
            
        Returns:
            Tensor of shape [batch_size, state_size]
        """
        # [batch_size, seq_len] -> [batch_size, seq_len, embedding_size]
        embedded = self.embedding(token_ids)
        
        # Conditionally use checkpoint to save memory during backprop
        if self.use_checkpoint and self.training:
            # Use checkpoint with explicit use_reentrant=False parameter
            # Suppress warnings by setting a dummy floating point requires_grad tensor
            dummy = torch.zeros(1, requires_grad=True, device=embedded.device)
            output, (hidden, _) = checkpoint(lambda x, _: self._run_encoder(x), embedded, dummy, use_reentrant=False)
        else:
            # Direct forward pass without checkpointing
            output, (hidden, _) = self.encoder(embedded)
        
        # Combine directions and layers of LSTM
        # [num_layers*2, batch_size, state_size//2] -> [batch_size, state_size]
        hidden = hidden.permute(1, 0, 2).contiguous()
        hidden = hidden.view(hidden.size(0), -1)
        
        # Final projection
        state = self.projection(hidden)
        return state

    def get_sparse_params(self):
        """Return parameters that should use sparse optimizer"""
        return [self.embedding.weight]
        
    def get_dense_params(self):
        """Return parameters that should use dense optimizer"""
        return [p for n, p in self.named_parameters() if 'embedding.weight' not in n]


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
        self.register_buffer('state_history', torch.zeros(0, state_size))
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
            memory_state += kernel_value * self.state_history[i].squeeze(0)
            kernel_sum += kernel_value
        
        # Normalize by sum of weights to maintain scale
        if kernel_sum > 0:
            memory_state = memory_state / kernel_sum
            
        return memory_state


class CellularMemory(nn.Module):
    """
    Implementation of the complete cellular memory dynamics
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
        
        # State transition matrix - use sparse initialization
        self.E = nn.Parameter(torch.zeros(state_size, state_size).to_sparse() * 0.1)
        
        # Cellular gates
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
            
        # Combine state and input for gating (like in LSTM/CDE)
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
        if neighbor_states.numel() > 0:
            # Ensure correct shape for neighbor_states
            if neighbor_states.dim() == 3:  # [num_neighbors, batch_size, state_size]
                neighbor_states = neighbor_states.transpose(0, 1)  # [batch_size, num_neighbors, state_size]
                neighbor_means = torch.mean(neighbor_states, dim=1)  # [batch_size, state_size]
            else:
                neighbor_means = torch.mean(neighbor_states, dim=0)
                
            diffusion = self.params.D * (neighbor_means - state)
        else:
            diffusion = torch.zeros_like(state)
        
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
        
        # Detect emergent properties (if we have neighbor states)
        if neighbor_states.numel() > 0:
            # FIX: Ensure compatible dimensions for concatenation
            if new_state.dim() == 1:
                new_state_for_concat = new_state.unsqueeze(0)  # [state_size] -> [1, state_size]
            else:
                new_state_for_concat = new_state  # Already [batch_size, state_size]
                
            # Ensure neighbor_states is 2D for concatenation with new_state
            if neighbor_states.dim() == 3:  # [batch_size, num_neighbors, state_size]
                # Reshape to [batch_size*num_neighbors, state_size]
                bs, nn, ss = neighbor_states.size()
                neighbor_states_for_concat = neighbor_states.reshape(-1, ss)
            elif neighbor_states.dim() == 2:  # [num_neighbors, state_size]
                neighbor_states_for_concat = neighbor_states
            else:
                # Fallback for unexpected dimensions
                neighbor_states_for_concat = neighbor_states.view(-1, neighbor_states.size(-1))
                
            # Now both should be 2D tensors that can be concatenated on dim=0
            all_states = torch.cat([new_state_for_concat, neighbor_states_for_concat], dim=0)
            emergence = self.detect_emergence(all_states)
        else:
            emergence = torch.zeros(1, device=new_state.device)
            
        return {
            'new_state': new_state,
            'transition_prob': transition_prob,
            'memory_state': memory_state,
            'emergence': emergence
        }


class TextDecoder(nn.Module):
    """Decodes state vectors back to text"""
    def __init__(self, state_size: int, embedding_size: int, vocab_size: int, use_checkpoint: bool = False):
        super().__init__()
        self.use_checkpoint = use_checkpoint
        # Define hidden size for the decoder LSTM
        self.hidden_size = state_size // 2
        self.num_layers = 2
        
        self.projection = nn.Linear(state_size, self.hidden_size * self.num_layers)
        self.decoder = nn.LSTM(
            input_size=embedding_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            batch_first=True,
            bidirectional=False,
            proj_size=0,  # Disable projection for speed
        )
        self.embedding = nn.Embedding(
            vocab_size, 
            embedding_size,
            sparse=True  # Enable sparse gradients
        )
        self.output_projection = nn.Linear(self.hidden_size, vocab_size)
        
    def init_state(self, state_vector: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Initialize decoder state from encoded state vector"""
        batch_size = state_vector.size(0)
        
        # Project state vector to appropriate size for decoder hidden state
        hidden_projection = self.projection(state_vector)
        
        # Reshape to [num_layers, batch_size, hidden_size]
        h_init = hidden_projection.view(batch_size, self.num_layers, self.hidden_size)
        h_init = h_init.transpose(0, 1).contiguous()  # [num_layers, batch_size, hidden_size]
        
        # Create cell state initialized to zeros
        c_init = torch.zeros_like(h_init)
        
        return (h_init, c_init)
    
    def _run_decoder(self, embedded, hidden):
        """Helper function for use with checkpoint to avoid keyword arguments"""
        return self.decoder(embedded, hidden)
    
    def forward(self, state_vector: torch.Tensor, 
               target_ids: Optional[torch.Tensor] = None, 
               max_length: int = 50) -> torch.Tensor:
        """
        Decode state vector to token IDs
        
        Args:
            state_vector: Tensor of shape [batch_size, state_size]
            target_ids: Optional target tokens for teacher forcing
            max_length: Maximum sequence length to generate
            
        Returns:
            Logits of shape [batch_size, seq_len, vocab_size]
        """
        batch_size = state_vector.size(0)
        device = state_vector.device
        
        # Initialize hidden state from state vector
        hidden = self.init_state(state_vector)
        
        # Teacher forcing if target_ids provided, otherwise generate
        if target_ids is not None:
            # Use teacher forcing
            seq_len = target_ids.size(1)
            embedded = self.embedding(target_ids)
            
            # Conditionally use checkpoint to save memory during backprop
            if self.use_checkpoint and self.training:
                # Use checkpoint with a helper function and explicit use_reentrant=False
                # Suppress warnings by setting a dummy floating point requires_grad tensor
                dummy = torch.zeros(1, requires_grad=True, device=embedded.device)
                output, _ = checkpoint(
                    lambda x, h, _: self._run_decoder(x, h),
                    embedded, hidden, dummy, 
                    use_reentrant=False
                )
            else:
                # Direct forward pass without checkpointing
                output, _ = self.decoder(embedded, hidden)
                
            logits = self.output_projection(output)
            return logits
        else:
            # Start with BOS token (ID 1)
            input_token = torch.ones(batch_size, 1, dtype=torch.long, device=device)
            
            outputs = []
            
            # Generate tokens one by one
            for i in range(max_length):
                embedded = self.embedding(input_token)
                output, hidden = self.decoder(embedded, hidden)
                logits = self.output_projection(output[:, -1:, :])
                outputs.append(logits)
                
                # Get the most likely token
                next_token = torch.argmax(logits, dim=-1)
                input_token = next_token
                
                # Stop if we hit the EOS token (ID 2)
                if (next_token == 2).all():
                    break
                    
            return torch.cat(outputs, dim=1)

    def get_sparse_params(self):
        """Return parameters that should use sparse optimizer"""
        return [self.embedding.weight]
        
    def get_dense_params(self):
        """Return parameters that should use dense optimizer"""
        return [p for n, p in self.named_parameters() if 'embedding.weight' not in n]


@ray.remote
class CellPartition:
    """
    Ray actor for parallel cellular processing
    Implements the complete CellAI mathematical model
    """
    def __init__(self, partition_id: int, params: ModelParams):
        self.id = partition_id
        self.params = params
        
        # Initialize device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Partition size
        self.partition_size = params.state_size // params.num_partitions
        
        # Initialize cellular memory with full mathematical components
        self.cell = CellularMemory(
            self.partition_size,
            params
        ).to(self.device)
        
        # Initialize state
        self.state = torch.zeros(self.partition_size, device=self.device)
        
        # Track current time for temporal integration
        self.current_time = 0.0
        
        # Get neighboring partition IDs
        self.neighbor_ids = []
        if partition_id > 0:
            self.neighbor_ids.append(partition_id - 1)
        if partition_id < params.num_partitions - 1:
            self.neighbor_ids.append(partition_id + 1)
    
    def update(self, 
              input_signal, 
              neighbor_states: Dict[int, np.ndarray],
              time_increment: float = 0.1) -> Dict[str, np.ndarray]:
        """
        Update partition state with all mathematical components
        
        Args:
            input_signal: Input signal [partition_size]
            neighbor_states: States of neighboring partitions {id: state}
            time_increment: Time increment for this update
            
        Returns:
            Dict with updated state and metadata
        """
        # Update current time
        self.current_time += time_increment
        
        # Convert inputs to tensors
        if isinstance(input_signal, np.ndarray):
            input_tensor = torch.tensor(input_signal, dtype=torch.float32, device=self.device)
        else:
            input_tensor = input_signal
            
        # Convert neighbor states to tensors
        if neighbor_states:
            neighbor_tensors = torch.stack([
                torch.tensor(state, dtype=torch.float32, device=self.device)
                if isinstance(state, np.ndarray) else state
                for state in neighbor_states.values()
            ])
        else:
            neighbor_tensors = torch.empty((0, self.partition_size), dtype=torch.float32, device=self.device)
        
        # Update state with full cellular dynamics
        with torch.no_grad():
            result = self.cell(
                self.state,
                input_tensor,
                neighbor_tensors,
                self.current_time
            )
            
            # Extract updated state
            self.state = result['new_state'].squeeze(0)
            
            # Process emergence values to ensure they're scalar
            if isinstance(result['emergence'], torch.Tensor):
                if result['emergence'].numel() > 0:
                    emergence_val = float(result['emergence'].mean().cpu().item())
                else:
                    emergence_val = 0.0
            else:
                emergence_val = float(result['emergence'])
            
            # Return state and metadata - ensure emergence is a scalar
            return {
                'state': self.state.cpu().numpy(),
                'transition_prob': result['transition_prob'].cpu().numpy(),
                'memory_state': result['memory_state'].cpu().numpy(),
                'emergence': emergence_val,  # Return as a scalar
                'time': self.current_time
            }
        
    def get_state(self) -> Dict[str, np.ndarray]:
        """Get current state and metadata"""
        return {
            'state': self.state.cpu().numpy(),
            'time': self.current_time
        }


class MemoryMappedWikiDataset(Dataset):
    """Memory-mapped dataset class for large Wikidata files"""
    def __init__(self, data_path: str, tokenizer, max_length: int = 512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Memory map the data file
        self.file = open(data_path, 'r+b')
        self.mm = mmap.mmap(self.file.fileno(), 0)
        
        # Index line offsets
        logging.info("Indexing file line offsets...")
        self.line_offsets = []
        offset = 0
        for _ in tqdm(range(self._count_lines(data_path))):
            line = self.mm.readline()
            if not line:
                break
            self.line_offsets.append(offset)
            offset = self.mm.tell()
        
        logging.info(f"Indexed {len(self.line_offsets)} lines")
        
    def _count_lines(self, filepath):
        """Count lines in a file"""
        with open(filepath, 'r') as f:
            return sum(1 for _ in f)
    
    def __len__(self):
        return len(self.line_offsets)
    
    def __getitem__(self, idx):
        # Seek to the correct position
        self.mm.seek(self.line_offsets[idx])
        line = self.mm.readline().decode('utf-8')
        
        try:
            item = json.loads(line)
            text = item.get('text', '')
        except:
            text = ''
            
        # Tokenize
        encodings = self.tokenizer(
            text, 
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encodings['input_ids'].squeeze(0),
            'attention_mask': encodings['attention_mask'].squeeze(0),
            'text': text
        }
        
    def __del__(self):
        """Ensure proper cleanup of file resources"""
        try:
            if hasattr(self, 'mm') and self.mm is not None:
                self.mm.close()
                self.mm = None
            if hasattr(self, 'file') and self.file is not None:
                self.file.close()
                self.file = None
        except Exception as e:
            logging.warning(f"Error during dataset cleanup: {e}")


class OptimizedTextCellularSystem:
    """
    Complete system implementing optimized traditional NLP with full CellAI math model
    """
    def __init__(self, params: ModelParams, pretrained_model: str = 'distilbert-base-uncased'):
        # Store params
        self.params = params
        
        # Configure Ray logging
        self._configure_ray_logging()
        
        # Ensure state_size is divisible by num_partitions
        if self.params.state_size % self.params.num_partitions != 0:
            original_size = self.params.state_size
            self.params.state_size = (self.params.state_size // self.params.num_partitions) * self.params.num_partitions
            logging.warning(f"Adjusted state_size from {original_size} to {self.params.state_size} to ensure divisibility by num_partitions")
        
        # Calculate partition state size
        self.partition_state_size = self.params.state_size // self.params.num_partitions
        logging.info(f"Using {self.params.num_partitions} partitions with state size {self.partition_state_size} each")
        
        # Initialize Ray with dynamic memory settings
        self._init_ray()
        
        # Initialize tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
        self.params.vocab_size = len(self.tokenizer)
        
        # Initialize device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize text encoder and decoder with optimization
        self.encoder = TextEncoder(
            vocab_size=self.params.vocab_size,
            embedding_size=self.params.embedding_size,
            state_size=self.params.state_size,
            use_checkpoint=True
        ).to(self.device)
        
        self.decoder = TextDecoder(
            state_size=self.params.state_size,
            embedding_size=self.params.embedding_size,
            vocab_size=self.params.vocab_size,
            use_checkpoint=True
        ).to(self.device)
        
        # Initialize cellular partitions with Ray
        self.partitions = [
            CellPartition.remote(i, self.params) 
            for i in range(self.params.num_partitions)
        ]
        
        # Get sparse parameters from encoder and decoder
        sparse_params = []
        sparse_params.extend(self.encoder.get_sparse_params())
        sparse_params.extend(self.decoder.get_sparse_params())
        
        # Get dense parameters from encoder and decoder
        dense_params = []
        dense_params.extend(self.encoder.get_dense_params())
        dense_params.extend(self.decoder.get_dense_params())
        
        # Initialize separate optimizers for sparse and dense parameters
        self.sparse_optimizer = optim.SparseAdam(
            sparse_params,
            lr=self.params.learning_rate
        )
        
        self.dense_optimizer = optim.AdamW(
            dense_params,
            lr=self.params.learning_rate,
            weight_decay=0.001,
            eps=1e-8
        )
        
        # Initialize loss function
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding token
        
        # System time for temporal memory
        self.current_time = 0.0
        
        # Training mode flag
        self.training = False

    def _configure_ray_logging(self):
        """Configure logging to silence Ray messages"""
        # Filter out Ray's loggers
        for logger_name in ["ray", "ray.worker", "ray.raylet", "ray.gcs_client", 
                          "ray.new_worker", "ray.client", "ray.gcs_client"]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.CRITICAL)  # Only show critical errors
            logger.propagate = False  # Don't propagate to root logger
            
        # Create a null handler for Ray loggers
        null_handler = logging.NullHandler()
        logging.getLogger("ray").addHandler(null_handler)
        
        # Disable Ray crash report uploading
        os.environ["RAY_DISABLE_CRASH_REPORTS"] = "1"

    def _init_ray(self):
        """Initialize Ray with optimized settings"""
        if not ray.is_initialized():
            # Use all available CPU cores
            num_cpus = multiprocessing.cpu_count()
            logging.info(f"Detected {num_cpus} CPU cores")
            
            # Dynamically determine memory availability
            try:
                import psutil
                
                # Get system memory information
                system_memory = psutil.virtual_memory()
                total_memory = system_memory.total
                available_memory = system_memory.available
                
                # Log memory information
                logging.info(f"Total system memory: {total_memory / (1024*1024*1024):.2f} GB")
                logging.info(f"Available memory: {available_memory / (1024*1024*1024):.2f} GB")
                
                # Calculate memory usage percentages based on available memory
                # More conservative when less memory is available
                if available_memory < 4 * 1024 * 1024 * 1024:  # Less than 4GB available
                    # Conservative allocation for low memory systems
                    obj_store_percent = 0.15  # 15% of available memory
                    ray_internal_percent = 0.05  # 5% of available memory
                    logging.info("Low memory detected - using conservative memory allocation")
                elif available_memory < 8 * 1024 * 1024 * 1024:  # Less than 8GB available
                    # Moderate allocation for medium memory systems
                    obj_store_percent = 0.25  # 25% of available memory
                    ray_internal_percent = 0.05  # 5% of available memory
                    logging.info("Moderate memory detected - using standard memory allocation")
                else:
                    # Higher allocation when plenty of memory is available
                    obj_store_percent = 0.30  # 30% of available memory
                    ray_internal_percent = 0.05  # 5% of available memory
                    logging.info("Sufficient memory detected - using optimal memory allocation")
                
                # Calculate memory allocations based on available memory
                obj_store_memory = int(available_memory * obj_store_percent)
                ray_memory = int(available_memory * ray_internal_percent)
                
                # Ensure minimum memory allocations
                MIN_OBJECT_STORE = 100 * 1024 * 1024  # 100MB minimum
                MIN_RAY_MEMORY = 50 * 1024 * 1024     # 50MB minimum
                
                obj_store_memory = max(obj_store_memory, MIN_OBJECT_STORE)
                ray_memory = max(ray_memory, MIN_RAY_MEMORY)
                
                # Cap memory usage to reasonable values
                MAX_OBJECT_STORE = 16 * 1024 * 1024 * 1024  # 16GB maximum
                MAX_RAY_MEMORY = 4 * 1024 * 1024 * 1024     # 4GB maximum
                
                obj_store_memory = min(obj_store_memory, MAX_OBJECT_STORE) 
                ray_memory = min(ray_memory, MAX_RAY_MEMORY)
                
                logging.info(f"Configuring Ray with {obj_store_memory / (1024*1024*1024):.2f} GB object store memory")
                logging.info(f"Configuring Ray with {ray_memory / (1024*1024*1024):.2f} GB internal memory")
                
            except ImportError:
                # If psutil isn't available, use conservative static allocations
                logging.warning("psutil not available - using conservative static memory allocation")
                obj_store_memory = 1 * 1024 * 1024 * 1024  # 1GB for object store
                ray_memory = 256 * 1024 * 1024             # 256MB for Ray internal
            
            # Create runtime env with aggressive log suppression
            runtime_env = {
                "env_vars": {
                    "RAY_verbose_spill_logs": "0",
                    "RAY_verbose_kill": "0",
                    "RAY_BACKEND_LOG_LEVEL": "error",
                    "RAY_memory_usage_threshold": "0.95",
                    "RAY_DISABLE_MEMORY_MONITOR": "1"
                }
            }
            
            # Try to initialize Ray with calculated memory settings
            try:
                ray.init(
                    num_cpus=num_cpus,
                    object_store_memory=obj_store_memory,
                    _memory=ray_memory,
                    ignore_reinit_error=True,
                    include_dashboard=False,
                    log_to_driver=False,     # Disable logging to driver
                    logging_level=logging.ERROR,  # Set logging level to ERROR
                    runtime_env=runtime_env,
                )
                logging.info("Ray initialized successfully")
            except Exception as e:
                logging.warning(f"Failed to initialize Ray with calculated settings: {e}")
                logging.warning("Falling back to minimal configuration")
                
                # Use half the cores with minimal memory
                ray.init(
                    num_cpus=max(1, num_cpus//2),
                    ignore_reinit_error=True,
                    include_dashboard=False,
                    log_to_driver=False,     # Disable logging to driver
                    logging_level=logging.ERROR,  # Set logging level to ERROR  
                    runtime_env=runtime_env,
                    log_level="ERROR"  # Explicitly set log_level to ERROR
                )
                logging.info("Ray initialized with fallback configuration")

    def process_text(self, text: str, context_history: List[str] = None) -> str:
        """Process text input through the system and generate a response"""
        start_time = time.time()
        
        try:
            # Update system time
            self.current_time += 0.1
            
            # Tokenize input text
            tokenized = self.tokenizer(
                text,
                padding=True,
                truncation=True,
                max_length=self.params.max_seq_length,
                return_tensors='pt'
            ).to(self.device)
            
            # Don't try to set requires_grad on integer tensors (token IDs)
            # Just use the tokenized input directly
            input_ids = tokenized['input_ids']
            
            # Encode text to state vector
            with torch.no_grad():
                state_vector = self.encoder(input_ids)
            
            # Split input across partitions
            try:
                # Split state vector into chunks for each partition
                partition_inputs = []
                for i in range(self.params.num_partitions):
                    start_idx = i * self.partition_state_size
                    end_idx = start_idx + self.partition_state_size
                    if len(state_vector.shape) > 1:  # Handle batch dimension
                        chunk = state_vector[:, start_idx:end_idx]
                    else:
                        chunk = state_vector[start_idx:end_idx]
                    partition_inputs.append(chunk.cpu().numpy().squeeze(0))
            except Exception as e:
                logging.error(f"Error splitting state vector: {e}")
                return "I encountered an error processing your request."
            
            # Get all states
            state_refs = [partition.get_state.remote() for partition in self.partitions]
            states_list = ray.get(state_refs)
            
            # Extract states and times
            states = {i: state_info['state'] for i, state_info in enumerate(states_list)}

            # Update all partitions in parallel
            update_refs = []
            for i, partition in enumerate(self.partitions):
                # Get neighbor states
                neighbor_ids = []
                if i > 0:
                    neighbor_ids.append(i - 1)
                if i < self.params.num_partitions - 1:
                    neighbor_ids.append(i + 1)
                
                neighbor_states = {j: states[j] for j in neighbor_ids}
                
                # Update partition
                update_refs.append(
                    partition.update.remote(
                        partition_inputs[i], 
                        neighbor_states,
                        self.params.dt
                    )
                )

            # Collect results
            update_results = ray.get(update_refs)
            
            # Extract updated states and metadata
            updated_states = np.concatenate([result['state'] for result in update_results])
            updated_states_tensor = torch.tensor(updated_states, dtype=torch.float32).unsqueeze(0).to(self.device)
            
            # Check for emergent properties - safely extract scalar values
            try:
                # Safely handle potential inhomogeneous emergence indicators
                emergence_values = []
                for result in update_results:
                    em = result['emergence']
                    # Extract a single scalar value if possible, or use mean/max/first value
                    if isinstance(em, np.ndarray) and em.size > 0:
                        if em.ndim == 0:
                            emergence_values.append(float(em))
                        else:
                            # Use the first value, or mean, or max - depending on what makes sense
                            emergence_values.append(float(em.flat[0]))
                    elif isinstance(em, (int, float)):
                        emergence_values.append(float(em))
                    else:
                        # Default to 0 if we can't extract a meaningful value
                        emergence_values.append(0.0)
                
                # Calculate system emergence if we have valid values
                if emergence_values:
                    system_emergence = np.mean(emergence_values) > 0.5
                    if system_emergence:
                        logging.info("Emergent properties detected during processing")
                else:
                    system_emergence = False
            except Exception as e:
                logging.warning(f"Error processing emergence indicators: {e}")
                system_emergence = False
            
            # Generate response
            with torch.no_grad():
                output_logits = self.decoder(updated_states_tensor, max_length=100)
                output_ids = torch.argmax(output_logits, dim=-1)
            
            # Decode response
            response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            elapsed_time = time.time() - start_time
            logging.info(f"Response generated in {elapsed_time:.2f} seconds")
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing text: {e}")
            import traceback
            traceback.print_exc()
            return "I'm sorry, I encountered an error processing your message."
    
    def train_on_wikidata(self, data_path: str, num_epochs: int = 3, 
                         save_path: str = './cellai_model_checkpoints', max_samples: int = 100000):
        """Train the model on Wikidata with high optimization"""
        # Set training mode
        self.training = True
        
        # Create save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Initialize system time for temporal memory
        self.current_time = 0.0
        
        # Monitor memory usage
        try:
            import psutil
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / (1024 * 1024)
            logging.info(f"Initial memory usage: {initial_memory:.2f} MB")
            
            # Get system memory info for optimization
            total_memory = psutil.virtual_memory().total / (1024 * 1024 * 1024)
            available_memory = psutil.virtual_memory().available / (1024 * 1024 * 1024)
            logging.info(f"System memory: {total_memory:.2f} GB total, {available_memory:.2f} GB available")
            
            # Set thread count for optimized CPU usage
            if available_memory < 2:  # Less than 2GB available
                optimal_threads = max(1, multiprocessing.cpu_count() // 4)
            elif available_memory < 4:  # Less than 4GB available
                optimal_threads = max(2, multiprocessing.cpu_count() // 2)
            else:
                optimal_threads = multiprocessing.cpu_count() - 1  # Leave one core for system processes
                
            torch.set_num_threads(optimal_threads)
            logging.info(f"Setting PyTorch thread count to {optimal_threads}")
            
        except ImportError:
            # If psutil not available, use conservative thread count
            num_cpus = multiprocessing.cpu_count()
            optimal_threads = max(2, num_cpus // 2)  # Conservative default
            torch.set_num_threads(optimal_threads)
            logging.info(f"Setting PyTorch thread count to {optimal_threads} (conservative default)")
        
        # Create memory-mapped dataset for efficiency
        dataset = MemoryMappedWikiDataset(
            data_path, 
            self.tokenizer, 
            self.params.max_seq_length
        )
        
        # Memory-aware adaptive batch sizes based on available memory
        try:
            if 'available_memory' in locals():
                # Scale batch size based on available memory
                if available_memory < 2:  # Less than 2GB available
                    memory_factor = 0.25  # Very small batches
                elif available_memory < 4:  # Less than 4GB available
                    memory_factor = 0.5   # Small batches
                elif available_memory < 8:  # Less than 8GB available
                    memory_factor = 0.75  # Medium batches
                else:
                    memory_factor = 1.0   # Full-sized batches
                
                # Base batch size calculation
                threads = torch.get_num_threads()
                base_batch_size = max(8, min(32, self.params.batch_size))
                
                # Adjust batch size by memory factor and thread count
                adaptive_batch_size = max(4, int(base_batch_size * memory_factor * (threads / 4)))
                adaptive_batch_size = min(64, adaptive_batch_size)  # Cap at 64 to prevent memory issues
            else:
                # Conservative defaults if memory info not available
                threads = torch.get_num_threads()
                adaptive_batch_size = max(8, min(32, self.params.batch_size * (threads // 4)))
        except Exception as e:
            logging.warning(f"Error calculating adaptive batch size: {e}. Using conservative defaults.")
            adaptive_batch_size = max(8, min(16, self.params.batch_size))
        
        # Adjust accumulation steps inversely with batch size
        self.params.accumulation_steps = max(1, int(32 / (adaptive_batch_size / 8)))
        
        logging.info(f"Using adaptive batch size: {adaptive_batch_size} with accumulation steps: {self.params.accumulation_steps}")
        
        # Create optimized dataloader
        dataloader = DataLoader(
            dataset, 
            batch_size=adaptive_batch_size, 
            shuffle=True,
            num_workers=min(4, multiprocessing.cpu_count()),
            pin_memory=True
        )
        
        # For early stopping
        best_loss = float('inf')
        no_improve_count = 0
        
        print(f"\n{'='*60}")
        print(f"Starting training for {num_epochs} epochs on {len(dataset)} samples")
        print(f"Using {torch.get_num_threads()} CPU threads with batch size {adaptive_batch_size}")
        print(f"{'='*60}\n")
        
        # Training loop
        for epoch in range(num_epochs):
            # Update system time for this epoch
            self.current_time += 1.0
            
            total_loss = 0
            logging.info(f"Starting epoch {epoch+1}/{num_epochs}")
            print(f"\nEpoch {epoch+1}/{num_epochs}")
            
            # Zero gradients
            self.sparse_optimizer.zero_grad()
            self.dense_optimizer.zero_grad()
            
            # Create a progress bar
            progress_bar = tqdm(
                dataloader, 
                desc=f"Epoch {epoch+1}", 
                position=0,
                leave=True,
                unit="batch"
            )
            
            # Track batch timing
            batch_times = []
            
            for batch_idx, batch in enumerate(progress_bar):
                batch_start = time.time()
                
                # Get batch data
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device) if 'attention_mask' in batch else None
                
                # Current time point for this batch
                batch_time = self.current_time + batch_idx * self.params.dt
                
                # Forward pass
                state_vector = self.encoder(input_ids)
                logits = self.decoder(state_vector, target_ids=input_ids)
                
                # Calculate loss - shift targets for language modeling
                shift_logits = logits[:, :-1, :].contiguous()
                shift_labels = input_ids[:, 1:].contiguous()
                
                loss = self.criterion(
                    shift_logits.view(-1, self.params.vocab_size),
                    shift_labels.view(-1)
                ) / self.params.accumulation_steps  # Scale for accumulation
                
                # Backward pass
                loss.backward()
                
                # Update only after accumulation steps
                if (batch_idx + 1) % self.params.accumulation_steps == 0 or (batch_idx + 1) == len(dataloader):
                    # Apply gradient clipping for dense parameters
                    dense_params = self.encoder.get_dense_params() + self.decoder.get_dense_params()
                    torch.nn.utils.clip_grad_norm_(dense_params, max_norm=1.0)
                    
                    # Step both optimizers
                    self.sparse_optimizer.step()
                    self.dense_optimizer.step()
                    
                    # Zero gradients
                    self.sparse_optimizer.zero_grad()
                    self.dense_optimizer.zero_grad()
                
                # Track metrics
                batch_loss = loss.item() * self.params.accumulation_steps
                total_loss += batch_loss
                
                # Track batch processing time
                batch_end = time.time()
                batch_time = batch_end - batch_start
                batch_times.append(batch_time)
                
                # Calculate samples per second
                samples_per_sec = adaptive_batch_size / batch_time
                
                # Update progress bar with stats
                progress_bar.set_postfix({
                    'loss': f"{batch_loss:.4f}",
                    'avg_loss': f"{total_loss / (batch_idx + 1):.4f}",
                    'samples/sec': f"{samples_per_sec:.1f}"
                })
            
            # Calculate average loss
            avg_loss = total_loss / len(dataloader)
            print(f"\nEpoch {epoch+1} completed with average loss: {avg_loss:.4f}")
            
            # Calculate and report training speed
            total_time = sum(batch_times)
            total_samples = len(dataset)
            samples_per_sec = total_samples / total_time
            print(f"Training speed: {samples_per_sec:.1f} samples/second")
            
            # Save checkpoint
            checkpoint_path = os.path.join(save_path, f"checkpoint_epoch_{epoch+1}.pt")
            torch.save({
                'encoder': self.encoder.state_dict(),
                'decoder': self.decoder.state_dict(),
                'sparse_optimizer': self.sparse_optimizer.state_dict(),
                'dense_optimizer': self.dense_optimizer.state_dict(),
                'params': vars(self.params),
                'epoch': epoch,
                'loss': avg_loss,
                'system_time': self.current_time
            }, checkpoint_path)
            logging.info(f"Checkpoint saved to {checkpoint_path}")
            
            # Early stopping
            if avg_loss < best_loss:
                best_loss = avg_loss
                no_improve_count = 0
                # Save best model
                best_model_path = os.path.join(save_path, "best_model.pt")
                torch.save({
                    'encoder': self.encoder.state_dict(),
                    'decoder': self.decoder.state_dict(),
                    'sparse_optimizer': self.sparse_optimizer.state_dict(),
                    'dense_optimizer': self.dense_optimizer.state_dict(),
                    'params': vars(self.params),
                    'epoch': epoch,
                    'loss': avg_loss,
                    'system_time': self.current_time
                }, best_model_path)
                logging.info(f"New best model saved with loss: {avg_loss:.4f}")
            else:
                no_improve_count += 1
                
            if no_improve_count >= self.params.early_stopping_patience:
                logging.info(f"Early stopping triggered after {epoch+1} epochs")
                print(f"Early stopping triggered after {epoch+1} epochs")
                break
                
        print(f"\n{'='*60}")
        print(f"Training completed. Best loss: {best_loss:.4f}")
        print(f"Model checkpoints saved to {save_path}")
        print(f"{'='*60}\n")
        
        # Reset training mode
        self.training = False
    
    def load_model(self, model_path: str):
        """Load a trained model"""
        try:
            logging.info(f"Loading model from {model_path}")
            checkpoint = torch.load(model_path, map_location=self.device)
            
            # Load model parameters
            if 'params' in checkpoint:
                param_dict = checkpoint['params']
                # Update parameters from checkpoint
                for key, value in param_dict.items():
                    if hasattr(self.params, key):
                        setattr(self.params, key, value)
            
            # Load encoder and decoder
            self.encoder.load_state_dict(checkpoint['encoder'])
            self.decoder.load_state_dict(checkpoint['decoder'])
            
            # Load optimizer states
            if 'sparse_optimizer' in checkpoint:
                self.sparse_optimizer.load_state_dict(checkpoint['sparse_optimizer'])
                
            if 'dense_optimizer' in checkpoint:
                self.dense_optimizer.load_state_dict(checkpoint['dense_optimizer'])
            
            # Load system time
            if 'system_time' in checkpoint:
                self.current_time = checkpoint['system_time']
                
            logging.info(f"Model loaded successfully. Trained until epoch {checkpoint.get('epoch', 'unknown')}")
            return True
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return False
            
    def benchmark(self, test_data_path: str, num_samples: int = 100):
        """Benchmark model performance on test data"""
        try:
            logging.info(f"Benchmarking model on {num_samples} samples from {test_data_path}")
            
            # Load test data
            if os.path.exists(test_data_path):
                samples = []
                with open(test_data_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i >= num_samples:
                            break
                        try:
                            item = json.loads(line)
                            if 'text' in item:
                                samples.append(item['text'])
                        except:
                            continue
            else:
                logging.error(f"Test data file not found: {test_data_path}")
                return
            
            if not samples:
                logging.warning("No valid samples found for benchmarking")
                return
                
            logging.info(f"Loaded {len(samples)} samples for benchmarking")
            
            # Metrics to track
            processing_times = []
            total_tokens_input = 0
            total_tokens_output = 0
            
            # Process each sample
            for i, text in enumerate(samples):
                start_time = time.time()
                
                # Tokenize input
                input_tokens = self.tokenizer.encode(text)
                total_tokens_input += len(input_tokens)
                
                # Process text 
                response = self.process_text(text)
                
                # Measure output tokens
                output_tokens = self.tokenizer.encode(response)
                total_tokens_output += len(output_tokens)
                
                elapsed_time = time.time() - start_time
                processing_times.append(elapsed_time)
                
                if i % 10 == 0:
                    logging.info(f"Processed {i+1}/{len(samples)} samples")
            
            # Calculate statistics
            avg_time = sum(processing_times) / len(processing_times)
            avg_tokens_in = total_tokens_input / len(samples)
            avg_tokens_out = total_tokens_output / len(samples)
            tokens_per_second = total_tokens_output / sum(processing_times)
            
            # Print benchmark results
            logging.info("=" * 50)
            logging.info("Benchmark Results:")
            logging.info(f"Average processing time: {avg_time:.4f} seconds per sample")
            logging.info(f"Average input tokens: {avg_tokens_in:.2f}")
            logging.info(f"Average output tokens: {avg_tokens_out:.2f}")
            logging.info(f"Tokens per second: {tokens_per_second:.2f}")
            logging.info("=" * 50)
            
            # Return results as dictionary
            return {
                'avg_time': avg_time,
                'avg_tokens_in': avg_tokens_in,
                'avg_tokens_out': avg_tokens_out,
                'tokens_per_second': tokens_per_second
            }
            
        except Exception as e:
            logging.error(f"Benchmark error: {e}")
            return None
    
    def cleanup(self):
        """Clean up resources to prevent memory leaks"""
        # Silence multiprocessing cleanup errors on exit
        atexit._clear()  # Remove standard library exit handlers to avoid cleanup conflicts
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # Free CUDA cache if available
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Shutdown Ray if initialized
        if ray.is_initialized():
            # Suppress all output during shutdown
            original_stderr = sys.stderr
            original_stdout = sys.stdout
            try:
                sys.stderr = open(os.devnull, 'w')
                sys.stdout = open(os.devnull, 'w')
                ray.shutdown()
            finally:
                # Restore output streams
                sys.stderr = original_stderr
                sys.stdout = original_stdout
            
            logging.info("Ray shutdown completed")


def get_default_params():
    """Get default model parameters with full mathematical components"""
    # Define memory kernel decay rates for multiple timescales
    kernel_decays = [0.1, 0.5, 1.0, 5.0, 10.0]
    
    return ModelParams(
        # Core cellular parameters
        dt=0.1,                # Time step for memory dynamics
        D=0.2,                 # Diffusion coefficient
        gamma=0.1,             # Decay rate
        eta=0.01,              # Noise amplitude
        num_partitions=4,      # Number of partitions
        state_size=768,        # Size of state vector
        
        # State transition parameters (CellAI Math)
        temperature=1.0,       # Temperature for Boltzmann distribution
        energy_scale=0.1,      # Scale factor for energy calculations
        
        # Temporal memory parameters (CellAI Math)
        memory_tau=5.0,        # Memory time constant
        kernel_terms=len(kernel_decays),  # Number of terms in memory kernel
        kernel_decays=kernel_decays,  # Decay rates for memory kernel
        
        # Boundary condition parameters (CellAI Math)
        boundary_strength=0.5,  # Coupling strength at boundaries
        
        # Emergent properties parameters (CellAI Math)
        collective_threshold=0.7,  # Threshold for collective behavior
        
        # NLP parameters
        embedding_size=256,    # Size of text embeddings
        vocab_size=30522,      # Will be updated by tokenizer
        max_seq_length=512,    # Maximum sequence length
        
        # Training parameters
        learning_rate=5e-5,    # Learning rate for training
        batch_size=16,         # Batch size for training
        accumulation_steps=4,  # Steps for gradient accumulation
        early_stopping_patience=3  # Patience for early stopping
    )


def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description="OptimizedTextCellAI - Full Mathematical Model with Optimized Traditional NLP")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Train command
    train_parser = subparsers.add_parser("train", help="Train the model")
    train_parser.add_argument("--data", required=True, help="Path to training data file")
    train_parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    train_parser.add_argument("--output", default="./cellai_model", help="Output directory")
    train_parser.add_argument("--max_samples", type=int, default=100000, help="Maximum samples to use")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Interactive chat with model")
    chat_parser.add_argument("--model", required=True, help="Path to model checkpoint")
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark model performance")
    benchmark_parser.add_argument("--model", required=True, help="Path to model checkpoint")
    benchmark_parser.add_argument("--test", required=True, help="Path to test data")
    benchmark_parser.add_argument("--samples", type=int, default=100, help="Number of samples to test")
    
    args = parser.parse_args()
    
    # Get default parameters
    params = get_default_params()
    
    # Initialize system
    system = OptimizedTextCellularSystem(params)
    
    try:
        if args.command == "train":
            # Train the model
            system.train_on_wikidata(
                args.data,
                args.epochs,
                args.output,
                args.max_samples
            )
            
        elif args.command == "chat":
            # Load the model
            success = system.load_model(args.model)
            if not success:
                print(f"Failed to load model from {args.model}")
                return
                
            print("\nOptimizedTextCellAI - Full Mathematical Model with Optimized Traditional NLP")
            print("Type 'exit' to quit the chat session\n")
            
            while True:
                user_input = input("\nYou: ")
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nGoodbye!")
                    break
                
                response = system.process_text(user_input)
                print(f"\nOptimizedTextCellAI: {response}")
            
        elif args.command == "benchmark":
            # Load the model
            success = system.load_model(args.model)
            if not success:
                print(f"Failed to load model from {args.model}")
                return
                
            # Run benchmark
            result = system.benchmark(args.test, args.samples)
            if result:
                print("\nBenchmark Results:")
                print(f"Average processing time: {result['avg_time']:.4f} seconds per sample")
                print(f"Average input tokens: {result['avg_tokens_in']:.2f}")
                print(f"Average output tokens: {result['avg_tokens_out']:.2f}")
                print(f"Tokens per second: {result['tokens_per_second']:.2f}")
            else:
                print("Benchmark failed")
            
        else:
            # Show help if no command provided
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up resources
        system.cleanup()


if __name__ == "__main__":
    main()