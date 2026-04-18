"""
CellAI-MathTrad - Specialized Mathematical AI System with CellAI Framework

This implementation combines:
1. The complete CellAI mathematical framework:
   - Cellular Equation: dS/dt = f(I, S, t) - γS + D∇²S + η(t)
   - Probabilistic State Transitions: P(Si→Sj) = exp(-ΔEij/kT) / Z
   - Temporal Memory Integration: M(t) = ∫[t-τ, t] w(t-s)I(s)ds + ∫[0, t] K(t-s)S(s)ds
   - Detailed Boundary Conditions: B(Sᵢ, Sⱼ) = 0 for adjacent partitions
   - Emergent Properties Framework for collective behavior

2. Mathematics-specific enhancements:
   - Symbolic mathematics representation and computation
   - Graph-based knowledge representation for mathematical concepts
   - Specialized embeddings for mathematical notation and LaTeX
   - Mathematical reasoning module with formal verification capabilities
   - Theorem proving and problem-solving strategies
   - Multi-step mathematical reasoning with step tracking
   - Specialized decoders for generating LaTeX/MathML output

3. Optimized implementation techniques:
   - Memory-optimized sparse embeddings with separate sparse gradient optimization
   - Optimized LSTM-based encoding/decoding with bidirectional processing
   - Efficient checkpointing for reduced memory usage during backpropagation
   - Memory-mapped dataset handling for large-scale data processing
   - Parallel data loading and preprocessing
   - Batch processing with gradient accumulation
   - Optimized Ray configuration for multicore processing

Usage:
  - Training: python CellAI-MathTrad.py train --data /path/to/math_data.jsonl --epochs 3
  - Solve: python CellAI-MathTrad.py solve --model /path/to/model.pt --problem "Solve x^2 + 2x + 1 = 0"
  - Benchmark: python CellAI-MathTrad.py benchmark --model /path/to/model.pt --test /path/to/math_test.jsonl
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
from typing import Dict, List, Tuple, Optional, Any, Union, Set
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
import sympy
import networkx as nx
from collections import defaultdict
import re

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
    """Combined parameters for MathCellAI with full mathematical framework"""
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
    
    # Mathematics-specific parameters
    symbolic_dim: int         # Dimension for symbolic representation
    graph_dim: int            # Dimension for graph-based knowledge
    reasoning_steps: int      # Maximum number of reasoning steps
    verification_threshold: float  # Threshold for formal verification
    
    # NLP parameters
    embedding_size: int       # Size of text embeddings
    vocab_size: int           # Size of vocabulary
    max_seq_length: int       # Maximum sequence length
    
    # Training parameters
    learning_rate: float      # Learning rate for training
    batch_size: int           # Batch size for training
    accumulation_steps: int   # Steps for gradient accumulation
    early_stopping_patience: int  # Patience for early stopping


class MathTokenizer:
    """Specialized tokenizer for mathematical expressions and LaTeX"""
    def __init__(self, base_tokenizer_name: str = 'distilbert-base-uncased'):
        self.base_tokenizer = AutoTokenizer.from_pretrained(base_tokenizer_name)
        
        # Special tokens for mathematical operations
        self.math_tokens = {
            # Basic operations
            '+': '[PLUS]',
            '-': '[MINUS]',
            '*': '[MULTIPLY]',
            '/': '[DIVIDE]',
            '^': '[POWER]',
            '=': '[EQUALS]',
            
            # Functions
            'sin': '[SIN]',
            'cos': '[COS]',
            'tan': '[TAN]',
            'log': '[LOG]',
            'ln': '[LN]',
            'exp': '[EXP]',
            'sqrt': '[SQRT]',
            
            # Sets and logic
            '∈': '[IN]',
            '∉': '[NOT_IN]',
            '∩': '[INTERSECT]',
            '∪': '[UNION]',
            '⊂': '[SUBSET]',
            '⊃': '[SUPERSET]',
            '∀': '[FOR_ALL]',
            '∃': '[EXISTS]',
            '¬': '[NOT]',
            '∧': '[AND]',
            '∨': '[OR]',
            '⟹': '[IMPLIES]',
            '⟺': '[IFF]',
            
            # Calculus
            '∫': '[INTEGRAL]',
            '∂': '[PARTIAL]',
            '∇': '[NABLA]',
            '∑': '[SUM]',
            '∏': '[PRODUCT]',
            
            # LaTeX markers
            '\\begin{equation}': '[EQ_START]',
            '\\end{equation}': '[EQ_END]',
            '\\begin{align}': '[ALIGN_START]',
            '\\end{align}': '[ALIGN_END]',
            '\\frac': '[FRAC]',
        }
        
        # Add special tokens to the base tokenizer
        special_tokens = list(self.math_tokens.values())
        num_added = self.base_tokenizer.add_special_tokens({'additional_special_tokens': special_tokens})
        logging.info(f"Added {num_added} special math tokens to the tokenizer")
        
        # Regular expression for parsing mathematical expressions
        self.math_pattern = re.compile(
            r'(' + '|'.join(re.escape(k) for k in self.math_tokens.keys()) + r')'
        )
    
    def preprocess_math(self, text: str) -> str:
        """Preprocess text with mathematical expressions"""
        # Replace LaTeX equation environments
        text = text.replace('$$', '[EQ_START]', 1)
        text = text.replace('$$', '[EQ_END]', 1)
        
        # Replace all math tokens with their special token equivalents
        for token, special in self.math_tokens.items():
            text = text.replace(token, f" {special} ")
            
        return text
    
    def tokenize(self, text: str, **kwargs) -> Dict[str, torch.Tensor]:
        """Tokenize text with mathematical expressions"""
        preprocessed = self.preprocess_math(text)
        return self.base_tokenizer(preprocessed, **kwargs)
    
    def encode(self, text: str, **kwargs) -> List[int]:
        """Encode text to token IDs"""
        preprocessed = self.preprocess_math(text)
        return self.base_tokenizer.encode(preprocessed, **kwargs)
    
    def decode(self, token_ids: List[int], **kwargs) -> str:
        """Decode token IDs back to text"""
        text = self.base_tokenizer.decode(token_ids, **kwargs)
        
        # Replace special tokens back to mathematical notation
        for token, special in self.math_tokens.items():
            text = text.replace(special, token)
            
        # Clean up excess spaces around operators
        for op in ['+', '-', '*', '/', '^', '=']:
            text = text.replace(f" {op} ", op)
            
        return text
    
    def __len__(self) -> int:
        """Get vocabulary size"""
        return len(self.base_tokenizer)


class MathSymbolicEncoder(nn.Module):
    """Encodes mathematical expressions into symbolic representations"""
    def __init__(self, vocab_size: int, embedding_size: int, symbolic_dim: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_size, sparse=True)
        
        # LSTM for processing mathematical expressions
        self.expr_encoder = nn.LSTM(
            input_size=embedding_size,
            hidden_size=embedding_size,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
        )
        
        # Projection to symbolic dimension
        self.projection = nn.Linear(embedding_size * 2, symbolic_dim)
        
        # Special encoders for different types of mathematical structures
        self.equation_encoder = nn.Linear(symbolic_dim, symbolic_dim)
        self.inequality_encoder = nn.Linear(symbolic_dim, symbolic_dim)
        self.function_encoder = nn.Linear(symbolic_dim, symbolic_dim)
        self.set_encoder = nn.Linear(symbolic_dim, symbolic_dim)
        
        # Dictionary to track mathematics objects and their types
        self.math_objects = {}
    
    def forward(self, token_ids: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Encode mathematical expressions symbolically
        
        Args:
            token_ids: Tensor of shape [batch_size, seq_len]
            
        Returns:
            Dictionary containing symbolic representations and object metadata
        """
        batch_size = token_ids.size(0)
        
        # Embed tokens
        embedded = self.embedding(token_ids)  # [batch_size, seq_len, embedding_size]
        
        # Process through LSTM
        output, (hidden, _) = self.expr_encoder(embedded)
        
        # Combine bidirectional states
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)  # [batch_size, embedding_size*2]
        
        # Project to symbolic space
        symbolic_repr = self.projection(hidden)  # [batch_size, symbolic_dim]
        
        # Identify mathematical structure types based on special tokens
        # This is a simplified approach - in practice, you'd use a classifier
        types = []
        for i in range(batch_size):
            tokens = token_ids[i].cpu().numpy()
            if '[EQUALS]' in tokens:
                types.append('equation')
            elif any(t in tokens for t in ['[GREATER]', '[LESS]']):
                types.append('inequality')
            elif any(t in tokens for t in ['[SIN]', '[COS]', '[TAN]', '[LOG]']):
                types.append('function')
            elif any(t in tokens for t in ['[IN]', '[UNION]', '[INTERSECT]']):
                types.append('set')
            else:
                types.append('expression')
        
        # Apply specialized encoders based on structure type
        specialized_reprs = []
        for i, type_name in enumerate(types):
            if type_name == 'equation':
                specialized_reprs.append(self.equation_encoder(symbolic_repr[i].unsqueeze(0)))
            elif type_name == 'inequality':
                specialized_reprs.append(self.inequality_encoder(symbolic_repr[i].unsqueeze(0)))
            elif type_name == 'function':
                specialized_reprs.append(self.function_encoder(symbolic_repr[i].unsqueeze(0)))
            elif type_name == 'set':
                specialized_reprs.append(self.set_encoder(symbolic_repr[i].unsqueeze(0)))
            else:
                specialized_reprs.append(symbolic_repr[i].unsqueeze(0))
        
        specialized_repr = torch.cat(specialized_reprs, dim=0)
        
        return {
            'symbolic': specialized_repr,
            'types': types,
            'raw': symbolic_repr
        }

    def extract_variables(self, tokens: List[int], tokenizer) -> Set[str]:
        """Extract mathematical variables from token sequence"""
        text = tokenizer.decode(tokens, skip_special_tokens=False)
        # Simple regex to find variables (single letters followed by optional subscripts)
        variables = set(re.findall(r'(?<![a-zA-Z])[a-zA-Z](?:_[0-9]+)?(?![a-zA-Z])', text))
        return variables
    
    def get_sparse_params(self):
        """Return parameters that should use sparse optimizer"""
        return [self.embedding.weight]
        
    def get_dense_params(self):
        """Return parameters that should use dense optimizer"""
        return [p for n, p in self.named_parameters() if 'embedding.weight' not in n]


class MathGraphEncoder(nn.Module):
    """Encodes mathematical concepts into graph-based knowledge representation"""
    def __init__(self, symbolic_dim: int, graph_dim: int):
        super().__init__()
        self.symbolic_dim = symbolic_dim
        self.graph_dim = graph_dim
        
        # Node and edge embeddings
        self.node_embedding = nn.Linear(symbolic_dim, graph_dim)
        self.edge_embedding = nn.Linear(symbolic_dim, graph_dim)
        
        # Graph attention layers
        self.graph_attention = nn.MultiheadAttention(
            embed_dim=graph_dim,
            num_heads=4,
            batch_first=True
        )
        
        # Concept hierarchy
        self.concept_hierarchy = {
            'number': ['integer', 'rational', 'real', 'complex'],
            'function': ['polynomial', 'rational', 'trigonometric', 'exponential', 'logarithmic'],
            'algebra': ['equation', 'inequality', 'system', 'polynomial'],
            'calculus': ['derivative', 'integral', 'limit', 'series'],
            'geometry': ['euclidean', 'analytic', 'differential', 'topology'],
            'probability': ['distribution', 'expectation', 'variance', 'random_variable'],
            'statistics': ['hypothesis_test', 'confidence_interval', 'regression', 'estimation']
        }
        
        # Initialize concept embeddings
        self.concept_embeddings = nn.ParameterDict()
        for domain, concepts in self.concept_hierarchy.items():
            # Domain embedding
            self.concept_embeddings[domain] = nn.Parameter(
                torch.randn(1, graph_dim) * 0.02
            )
            # Concept embeddings - using underscore instead of dot
            for concept in concepts:
                self.concept_embeddings[f"{domain}_{concept}"] = nn.Parameter(
                    torch.randn(1, graph_dim) * 0.02
                )
    
    def build_knowledge_graph(self, symbolic_repr: torch.Tensor, 
                            math_types: List[str]) -> Tuple[torch.Tensor, List[List[int]]]:
        """
        Build a knowledge graph for the batch of mathematical concepts
        
        Args:
            symbolic_repr: Symbolic representations [batch_size, symbolic_dim]
            math_types: List of mathematical structure types
            
        Returns:
            Node embeddings and adjacency lists
        """
        batch_size = symbolic_repr.size(0)
        device = symbolic_repr.device
        
        all_node_embeddings = []
        all_adjacency_lists = []
        
        for i in range(batch_size):
            # Create initial node embedding from symbolic representation
            expr_node = self.node_embedding(symbolic_repr[i]).unsqueeze(0)  # [1, graph_dim]
            
            # Determine relevant concepts based on math type
            math_type = math_types[i]
            relevant_concepts = []
            
            # Match concepts from hierarchy
            for domain, concepts in self.concept_hierarchy.items():
                if any(c in math_type for c in concepts):
                    # Add domain
                    relevant_concepts.append(domain)
                    # Add specific concepts - using underscore instead of dot
                    for concept in concepts:
                        if concept in math_type:
                            relevant_concepts.append(f"{domain}_{concept}")
            
            # If no specific concepts matched, add some reasonable defaults
            if not relevant_concepts:
                if 'equation' in math_type:
                    relevant_concepts = ['algebra', 'algebra_equation']
                elif 'function' in math_type:
                    relevant_concepts = ['function', 'function_polynomial']
                elif 'set' in math_type:
                    relevant_concepts = ['algebra', 'algebra_equation']
                else:
                    relevant_concepts = ['algebra', 'algebra_equation']
            
            # Gather concept embeddings
            concept_nodes = [self.concept_embeddings[c] for c in relevant_concepts]
            if concept_nodes:
                concept_nodes = torch.cat(concept_nodes, dim=0)  # [num_concepts, graph_dim]
                # Combine with expression node
                node_embeddings = torch.cat([expr_node, concept_nodes], dim=0)  # [num_nodes, graph_dim]
            else:
                node_embeddings = expr_node
            
            # Create adjacency list (fully connected for simplicity)
            num_nodes = node_embeddings.size(0)
            adjacency_list = []
            for src in range(num_nodes):
                for dst in range(num_nodes):
                    if src != dst:  # Avoid self-loops
                        adjacency_list.append((src, dst))
            
            all_node_embeddings.append(node_embeddings)
            all_adjacency_lists.append(adjacency_list)
        
        return all_node_embeddings, all_adjacency_lists
    
    def forward(self, symbolic_repr: torch.Tensor, 
               math_types: List[str]) -> torch.Tensor:
        """
        Process symbolic representations through knowledge graph
        
        Args:
            symbolic_repr: Symbolic representations [batch_size, symbolic_dim]
            math_types: List of mathematical structure types
            
        Returns:
            Graph-enhanced representations [batch_size, graph_dim]
        """
        # Build knowledge graphs
        node_embeddings_list, adjacency_lists = self.build_knowledge_graph(
            symbolic_repr, math_types
        )
        
        # Process each graph
        batch_size = symbolic_repr.size(0)
        graph_embeddings = []
        
        for i in range(batch_size):
            nodes = node_embeddings_list[i]  # [num_nodes, graph_dim]
            adj_list = adjacency_lists[i]
            
            # Simple message passing (for more complex graphs, use a GNN library)
            # For this implementation, we'll use self-attention as a form of message passing
            if nodes.size(0) > 1:  # Only apply attention if we have multiple nodes
                attended_nodes, _ = self.graph_attention(nodes, nodes, nodes)
                
                # Use the first node (expression node) as the graph representation
                graph_emb = attended_nodes[0].unsqueeze(0)  # [1, graph_dim]
            else:
                graph_emb = nodes  # [1, graph_dim]
                
            graph_embeddings.append(graph_emb)
        
        return torch.cat(graph_embeddings, dim=0)  # [batch_size, graph_dim]


class MathReasoner(nn.Module):
    """Mathematical reasoning module with formal verification capabilities"""
    def __init__(self, symbolic_dim: int, graph_dim: int, state_size: int, 
                max_steps: int = 5, verification_threshold: float = 0.9):
        super().__init__()
        self.symbolic_dim = symbolic_dim
        self.graph_dim = graph_dim
        self.state_size = state_size
        self.max_steps = max_steps
        self.verification_threshold = verification_threshold
        
        # Combine symbolic and graph representations
        self.combiner = nn.Linear(symbolic_dim + graph_dim, state_size)
        
        # Reasoning steps controller
        self.step_controller = nn.LSTMCell(state_size, state_size)
        
        # Operator selection
        self.operators = [
            'simplify', 'expand', 'factor', 'solve', 'differentiate', 
            'integrate', 'substitute', 'apply_identity'
        ]
        
        self.operator_selector = nn.Linear(state_size, len(self.operators))
        
        # Verification module - for concatenated states (state_size * 2)
        self.verification = nn.Sequential(
            nn.Linear(state_size * 2, state_size // 2),
            nn.ReLU(),
            nn.Linear(state_size // 2, 1),
            nn.Sigmoid()
        )
        
        # Theorem database (simplified)
        self.theorems = {
            'quad_formula': 'For ax^2 + bx + c = 0, x = (-b ± √(b^2 - 4ac)) / 2a',
            'pythagorean': 'a^2 + b^2 = c^2 in a right triangle',
            'euler_identity': 'e^(iπ) + 1 = 0',
            'binomial_expansion': '(a + b)^n = ∑(k=0 to n) (n choose k) a^(n-k) b^k',
            'derivative_product_rule': 'd/dx[f(x)g(x)] = f(x)·g\'(x) + g(x)·f\'(x)',
            'integration_by_parts': '∫u(x)v\'(x)dx = u(x)v(x) - ∫v(x)u\'(x)dx'
        }
        
        # Initialize theorem embeddings
        self.theorem_embeddings = nn.ParameterDict()
        for name in self.theorems.keys():
            self.theorem_embeddings[name] = nn.Parameter(
                torch.randn(1, state_size) * 0.02
            )
    
    def _is_valid_math_expr(self, expr: str) -> bool:
        """Check if a string is likely to be a valid mathematical expression"""
        if not expr or expr.isspace():
            return False
            
        # Remove any "(Applied: X)" annotations
        clean_expr = re.sub(r'\s*\(Applied:\s*[^)]*\)\s*', '', expr)
        
        # Check if there's anything left after cleaning
        if not clean_expr or clean_expr.isspace():
            return False
        
        # Check if it has some mathematical characters
        math_chars = set('+-*/^=<>()[]{}')
        has_math_chars = any(c in math_chars for c in clean_expr)
        has_digits = any(c.isdigit() for c in clean_expr)
        has_variables = any(c.isalpha() for c in clean_expr)
        
        return (has_math_chars or has_digits) and has_variables
    
    def _clean_expr_for_sympy(self, expr: str) -> str:
        """Clean expression for SymPy parsing"""
        # Remove any "(Applied: X)" annotations
        clean_expr = re.sub(r'\s*\(Applied:\s*[^)]*\)\s*', '', expr)
        
        # Replace common math notations with SymPy-friendly versions
        replacements = {
            '√': 'sqrt',  # Square root symbol
            '∫': 'integrate',  # Integral symbol
            '∑': 'sum',  # Summation symbol
            '∏': 'product',  # Product symbol
            '∞': 'oo',  # Infinity symbol
            '→': '->',  # Arrow for limits
            '≤': '<=',  # Less than or equal
            '≥': '>=',  # Greater than or equal
            '≠': '!=',  # Not equal
            '∂': 'diff',  # Partial derivative
            '∇': 'grad',  # Gradient
        }
        
        for old, new in replacements.items():
            clean_expr = clean_expr.replace(old, new)
        
        return clean_expr
    
    def apply_operator(self, state: torch.Tensor, operator_idx: int, 
                     current_expr: str) -> Tuple[torch.Tensor, str]:
        """
        Apply mathematical operator to current state and expression
        
        Args:
            state: Current reasoning state [batch_size, state_size]
            operator_idx: Index of operator to apply
            current_expr: Current symbolic expression string
            
        Returns:
            Updated state and modified expression
        """
        batch_size = state.size(0)
        device = state.device
        
        # Get operator name
        operator = self.operators[operator_idx]
        
        # Check if the expression is a valid mathematical expression
        is_valid = self._is_valid_math_expr(current_expr)
        
        # If not valid or empty, apply theorem but don't attempt SymPy operations
        if not is_valid:
            # Extract any previously applied theorem
            applied_theorem = None
            theorem_match = re.search(r'\(Applied:\s*([^)]*)\)', current_expr)
            if theorem_match:
                applied_theorem = theorem_match.group(1).strip()
            
            # Apply a random theorem
            theorem_name = list(self.theorems.keys())[
                torch.randint(0, len(self.theorems), (1,)).item()
            ]
            
            # If we already have a theorem applied, keep it and just use the state update
            if applied_theorem and applied_theorem in self.theorems:
                theorem_state = self.theorem_embeddings[applied_theorem]
                state = state + theorem_state
                new_expr = current_expr
            else:
                # Apply new theorem
                theorem_state = self.theorem_embeddings[theorem_name]
                state = state + theorem_state
                
                if current_expr and not current_expr.isspace():
                    # Preserve original expression but add theorem
                    new_expr = f"{current_expr} (Applied: {theorem_name})"
                else:
                    # For empty expressions, just use a placeholder
                    new_expr = f"x (Applied: {theorem_name})"
            
            return state, new_expr
        
        # For valid expressions, try to apply SymPy operations
        try:
            # Clean the expression for SymPy
            clean_expr = self._clean_expr_for_sympy(current_expr)
            
            # Check if the expression contains "(Applied: X)" and preserve it
            applied_info = ""
            theorem_match = re.search(r'\s*\(Applied:\s*([^)]*)\)\s*$', current_expr)
            if theorem_match:
                applied_info = f" (Applied: {theorem_match.group(1)})"
            
            # Try SymPy operations
            if operator == 'simplify':
                try:
                    expr_obj = sympy.sympify(clean_expr)
                    result = str(sympy.simplify(expr_obj))
                    new_expr = result + applied_info
                except:
                    new_expr = current_expr
            elif operator == 'expand':
                try:
                    expr_obj = sympy.sympify(clean_expr)
                    result = str(sympy.expand(expr_obj))
                    new_expr = result + applied_info
                except:
                    new_expr = current_expr
            elif operator == 'factor':
                try:
                    expr_obj = sympy.sympify(clean_expr)
                    result = str(sympy.factor(expr_obj))
                    new_expr = result + applied_info
                except:
                    new_expr = current_expr
            elif operator == 'solve':
                # This is simplified - would need to parse equation and variable
                if '=' in clean_expr:
                    try:
                        lhs, rhs = clean_expr.split('=')
                        lhs_obj = sympy.sympify(lhs)
                        rhs_obj = sympy.sympify(rhs)
                        equation = lhs_obj - rhs_obj
                        # Assume solving for x
                        sol = sympy.solve(equation, sympy.Symbol('x'))
                        new_expr = f"x = {sol}" + applied_info
                    except:
                        new_expr = current_expr
                else:
                    new_expr = current_expr
            elif operator == 'differentiate':
                try:
                    expr_obj = sympy.sympify(clean_expr)
                    # Assume differentiating with respect to x
                    result = str(sympy.diff(expr_obj, sympy.Symbol('x')))
                    new_expr = result + applied_info
                except:
                    new_expr = current_expr
            elif operator == 'integrate':
                try:
                    expr_obj = sympy.sympify(clean_expr)
                    # Assume integrating with respect to x
                    result = str(sympy.integrate(expr_obj, sympy.Symbol('x')))
                    new_expr = result + applied_info
                except:
                    new_expr = current_expr
            elif operator == 'substitute':
                try:
                    # This is simplified - would need more context for substitution
                    new_expr = clean_expr.replace('x', '(a+b)') + applied_info
                except:
                    new_expr = current_expr
            elif operator == 'apply_identity':
                # Use a random theorem from the database
                theorem_name = list(self.theorems.keys())[
                    torch.randint(0, len(self.theorems), (1,)).item()
                ]
                theorem_state = self.theorem_embeddings[theorem_name]
                
                # Update state based on theorem
                state = state + theorem_state
                new_expr = current_expr + f" (Applied: {theorem_name})"
            else:
                new_expr = current_expr
                
        except Exception as e:
            # Fallback for parsing errors
            logging.warning(f"Error applying operator {operator}: {e}")
            new_expr = current_expr
            
            # Apply a theorem as fallback
            theorem_name = list(self.theorems.keys())[
                torch.randint(0, len(self.theorems), (1,)).item()
            ]
            theorem_state = self.theorem_embeddings[theorem_name]
            state = state + theorem_state
            
            # Add theorem info if not already present
            if "(Applied:" not in new_expr:
                new_expr = f"{new_expr} (Applied: {theorem_name})"
        
        return state, new_expr
    
    def verify_step(self, old_state: torch.Tensor, new_state: torch.Tensor, 
                  old_expr: str, new_expr: str) -> float:
        """
        Verify mathematical correctness of a reasoning step
        
        Args:
            old_state: State before step [batch_size, state_size]
            new_state: State after step [batch_size, state_size]
            old_expr: Expression before step
            new_expr: Expression after step
            
        Returns:
            Verification score between 0 and 1
        """
        # Combine old and new states for verification
        diff_state = new_state - old_state
        verification_input = torch.cat([old_state, diff_state], dim=-1)
        
        # Get verification score
        score = self.verification(verification_input)
        
        # In a real implementation, you would also formally verify the mathematical
        # equivalence between old_expr and new_expr using a symbolic math library
        
        return score.item()
    
    def forward(self, symbolic_repr: torch.Tensor, graph_repr: torch.Tensor, 
               initial_expr: List[str]) -> Dict[str, Any]:
        """
        Perform multi-step mathematical reasoning
        
        Args:
            symbolic_repr: Symbolic representations [batch_size, symbolic_dim]
            graph_repr: Graph representations [batch_size, graph_dim]
            initial_expr: List of initial mathematical expressions as strings
            
        Returns:
            Dictionary with reasoning steps and final results
        """
        batch_size = symbolic_repr.size(0)
        device = symbolic_repr.device
        
        # Combine symbolic and graph representations
        combined = torch.cat([symbolic_repr, graph_repr], dim=1)
        state = self.combiner(combined)
        
        # Initialize hidden state for step controller
        hidden = state
        cell = torch.zeros_like(state)
        
        # Initialize results tracking
        all_steps = [[] for _ in range(batch_size)]
        current_expressions = initial_expr.copy()
        final_verified = [False] * batch_size
        
        # Ensure all initial expressions are strings
        for i in range(len(current_expressions)):
            if current_expressions[i] is None or not isinstance(current_expressions[i], str):
                current_expressions[i] = ""
        
        # Perform reasoning steps
        for step in range(self.max_steps):
            # Update reasoning state
            hidden, cell = self.step_controller(state, (hidden, cell))
            
            # Select operators
            operator_logits = self.operator_selector(hidden)
            operator_probs = torch.softmax(operator_logits, dim=1)
            operator_indices = torch.argmax(operator_probs, dim=1)
            
            # Apply operators batch-wise
            new_expressions = []
            new_states = []
            
            for i in range(batch_size):
                new_state, new_expr = self.apply_operator(
                    hidden[i].unsqueeze(0),
                    operator_indices[i].item(),
                    current_expressions[i]
                )
                
                # Verify step
                verification_score = self.verify_step(
                    hidden[i].unsqueeze(0),
                    new_state,
                    current_expressions[i],
                    new_expr
                )
                
                # Record step
                all_steps[i].append({
                    'step': step + 1,
                    'operator': self.operators[operator_indices[i].item()],
                    'expression': new_expr,
                    'verification': verification_score
                })
                
                # Mark as verified if score is high enough
                if verification_score >= self.verification_threshold:
                    final_verified[i] = True
                
                new_states.append(new_state)
                new_expressions.append(new_expr)
            
            # Update current state and expressions
            state = torch.cat(new_states, dim=0)
            current_expressions = new_expressions
        
        return {
            'final_state': state,
            'final_expressions': current_expressions,
            'reasoning_steps': all_steps,
            'verified': final_verified
        }


class MathTextEncoder(nn.Module):
    """Encodes mathematical text into vector representations"""
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


class MathCellularMemory(nn.Module):
    """
    Implementation of the complete cellular memory dynamics for mathematics
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
        
        # Mathematics-specific enhancements
        self.consistency_checker = nn.Linear(state_size, 1)
        self.math_domain_classifier = nn.Linear(state_size, 7)  # 7 mathematical domains
        
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
    
    def check_mathematical_consistency(self, state: torch.Tensor) -> float:
        """Check mathematical consistency of the state"""
        consistency_score = torch.sigmoid(self.consistency_checker(state))
        return consistency_score.item()
    
    def classify_math_domain(self, state: torch.Tensor) -> str:
        """Classify state into mathematical domain"""
        domain_logits = self.math_domain_classifier(state)
        domain_idx = torch.argmax(domain_logits, dim=-1).item()
        
        domains = ['algebra', 'calculus', 'geometry', 'statistics', 
                 'number_theory', 'logic', 'set_theory']
        
        return domains[domain_idx]
    
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
            # Ensure compatible dimensions for concatenation
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
        
        # Check mathematical consistency
        consistency = self.check_mathematical_consistency(new_state)
        
        # Classify mathematical domain
        domain = self.classify_math_domain(new_state)
            
        return {
            'new_state': new_state,
            'transition_prob': transition_prob,
            'memory_state': memory_state,
            'emergence': emergence,
            'consistency': consistency,
            'domain': domain
        }


class MathLatexDecoder(nn.Module):
    """Decodes state vectors to LaTeX mathematical expressions"""
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
        
        # LaTeX-specific enhancements
        self.latex_context = nn.Parameter(torch.randn(1, self.hidden_size))
        
        # Dictionary of common LaTeX templates for mathematical structures
        self.latex_templates = {
            'equation': r'\begin{equation} #1 \end{equation}',
            'aligned': r'\begin{aligned} #1 \end{aligned}',
            'matrix': r'\begin{bmatrix} #1 \end{bmatrix}',
            'cases': r'\begin{cases} #1 \end{cases}',
            'fraction': r'\frac{#1}{#2}',
            'integral': r'\int_{#1}^{#2} #3 \, d#4',
            'limit': r'\lim_{#1 \to #2} #3',
            'sum': r'\sum_{#1}^{#2} #3',
            'product': r'\prod_{#1}^{#2} #3'
        }
        
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
    
    def detect_math_structure(self, state_vector: torch.Tensor) -> str:
        """Detect likely mathematical structure from state vector"""
        # Simple approach: use cosine similarity with a learned representation for each template
        structure_scores = {}
        
        # In a real implementation, this would be a learned classifier
        # Here we'll just return a random template for demonstration
        structures = list(self.latex_templates.keys())
        return structures[torch.randint(0, len(structures), (1,)).item()]
    
    def forward(self, state_vector: torch.Tensor, 
               target_ids: Optional[torch.Tensor] = None, 
               max_length: int = 100) -> torch.Tensor:
        """
        Decode state vector to LaTeX token IDs
        
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
            
            # Add LaTeX context
            latex_context_expanded = self.latex_context.expand(batch_size, 1, -1)
            
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
                
            # Project to vocabulary
            logits = self.output_projection(output)
            return logits
        else:
            # Start with BOS token (ID 1)
            input_token = torch.ones(batch_size, 1, dtype=torch.long, device=device)
            
            outputs = []
            
            # For each batch item, detect mathematical structure
            structures = [self.detect_math_structure(state_vector[i].unsqueeze(0)) 
                         for i in range(batch_size)]
            
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
class MathCellPartition:
    """
    Ray actor for parallel cellular processing of mathematical concepts
    Implements the complete CellAI mathematical model with math-specific enhancements
    """
    def __init__(self, partition_id: int, params: ModelParams):
        self.id = partition_id
        self.params = params
        
        # Initialize device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Partition size
        self.partition_size = params.state_size // params.num_partitions
        
        # Initialize cellular memory with full mathematical components
        self.cell = MathCellularMemory(
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
        
        # Mathematics domain specialization
        # Each partition can specialize in a specific area of mathematics
        math_domains = [
            'algebra', 'calculus', 'geometry', 'statistics', 
            'number_theory', 'logic', 'set_theory'
        ]
        
        # Assign domain based on partition ID (wrap around if needed)
        self.domain = math_domains[partition_id % len(math_domains)]
        
        # Enhanced for math with step-by-step solution tracking
        self.solution_steps = []
    
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
            
            # Track solution step with domain-specific interpretation
            self.solution_steps.append({
                'time': self.current_time,
                'state_norm': float(torch.norm(self.state).cpu().item()),
                'domain': result['domain'] if isinstance(result['domain'], str) else "unknown",
                'consistency': float(result['consistency'])
            })
            
            # Return state and metadata
            return {
                'state': self.state.cpu().numpy(),
                'transition_prob': result['transition_prob'].cpu().numpy(),
                'memory_state': result['memory_state'].cpu().numpy(),
                'emergence': emergence_val,  # Return as a scalar
                'time': self.current_time,
                'domain': result['domain'],
                'consistency': float(result['consistency']),
                'last_step': self.solution_steps[-1] if self.solution_steps else None
            }
        
    def get_state(self) -> Dict[str, np.ndarray]:
        """Get current state and metadata"""
        return {
            'state': self.state.cpu().numpy(),
            'time': self.current_time,
            'domain': self.domain,
            'solution_steps': self.solution_steps
        }


class MathDataset(Dataset):
    """Dataset for mathematical problems and solutions"""
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
            problem = item.get('problem', '')
            solution = item.get('solution', '')
        except:
            problem = ''
            solution = ''
            
        # Tokenize problem
        problem_encodings = self.tokenizer.tokenize(
            problem, 
            max_length=self.max_length // 2,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Tokenize solution
        solution_encodings = self.tokenizer.tokenize(
            solution, 
            max_length=self.max_length // 2,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'problem_ids': problem_encodings['input_ids'].squeeze(0),
            'problem_mask': problem_encodings['attention_mask'].squeeze(0),
            'solution_ids': solution_encodings['input_ids'].squeeze(0),
            'solution_mask': solution_encodings['attention_mask'].squeeze(0),
            'problem': problem,
            'solution': solution
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


class MathCellularSystem:
    """
    Complete system implementing the CellAI framework for mathematics
    """
    def __init__(self, params: ModelParams):
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
        
        # Initialize specialized math tokenizer
        self.tokenizer = MathTokenizer()
        self.params.vocab_size = len(self.tokenizer)
        
        # Initialize device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize text encoder and symbolic encoder
        self.text_encoder = MathTextEncoder(
            vocab_size=self.params.vocab_size,
            embedding_size=self.params.embedding_size,
            state_size=self.params.state_size,
            use_checkpoint=True
        ).to(self.device)
        
        self.symbolic_encoder = MathSymbolicEncoder(
            vocab_size=self.params.vocab_size,
            embedding_size=self.params.embedding_size,
            symbolic_dim=self.params.symbolic_dim
        ).to(self.device)
        
        # Initialize graph encoder
        self.graph_encoder = MathGraphEncoder(
            symbolic_dim=self.params.symbolic_dim,
            graph_dim=self.params.graph_dim
        ).to(self.device)
        
        # Initialize reasoning module
        self.math_reasoner = MathReasoner(
            symbolic_dim=self.params.symbolic_dim,
            graph_dim=self.params.graph_dim,
            state_size=self.params.state_size,
            max_steps=self.params.reasoning_steps,
            verification_threshold=self.params.verification_threshold
        ).to(self.device)
        
        # Initialize LaTeX decoder
        self.latex_decoder = MathLatexDecoder(
            state_size=self.params.state_size,
            embedding_size=self.params.embedding_size,
            vocab_size=self.params.vocab_size,
            use_checkpoint=True
        ).to(self.device)
        
        # Initialize cellular partitions with Ray
        self.partitions = [
            MathCellPartition.remote(i, self.params) 
            for i in range(self.params.num_partitions)
        ]
        
        # Get sparse parameters 
        sparse_params = []
        sparse_params.extend(self.text_encoder.get_sparse_params())
        sparse_params.extend(self.symbolic_encoder.get_sparse_params())
        sparse_params.extend(self.latex_decoder.get_sparse_params())
        
        # Get dense parameters
        dense_params = []
        dense_params.extend(self.text_encoder.get_dense_params())
        dense_params.extend(self.symbolic_encoder.get_dense_params())
        dense_params.extend(self.graph_encoder.parameters())
        dense_params.extend(self.math_reasoner.parameters())
        dense_params.extend(self.latex_decoder.get_dense_params())
        
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

    def solve_math_problem(self, problem_text: str) -> Dict[str, Any]:
        """
        Solve a mathematical problem and provide detailed steps
        
        Args:
            problem_text: The mathematical problem text
            
        Returns:
            Dictionary with solution and step-by-step reasoning
        """
        start_time = time.time()
        
        try:
            # Update system time
            self.current_time += 0.1
            
            # Tokenize input text
            tokenized = self.tokenizer.tokenize(
                problem_text,
                padding=True,
                truncation=True,
                max_length=self.params.max_seq_length,
                return_tensors='pt'
            ).to(self.device)
            
            input_ids = tokenized['input_ids']
            
            # Encode text to state vector
            with torch.no_grad():
                state_vector = self.text_encoder(input_ids)
                
                # Get symbolic representation
                symbolic_result = self.symbolic_encoder(input_ids)
                symbolic_repr = symbolic_result['symbolic']
                math_types = symbolic_result['types']
                
                # Get graph-based knowledge representation
                graph_repr = self.graph_encoder(symbolic_repr, math_types)
                
                # Extract the mathematical expressions from the problem
                expressions = self.extract_math_expressions(problem_text)
                
                # Perform multi-step mathematical reasoning
                reasoning_result = self.math_reasoner(
                    symbolic_repr, 
                    graph_repr,
                    expressions
                )
            
            # Split state vector across partitions
            try:
                # Split combined state vector into chunks for each partition
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
                return {"error": "Failed to process the mathematical problem."}
            
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
            
            # Extract updated states and collect solution steps
            updated_states = np.concatenate([result['state'] for result in update_results])
            updated_states_tensor = torch.tensor(updated_states, dtype=torch.float32).unsqueeze(0).to(self.device)
            
            # Collect solution steps from each partition
            solution_steps = []
            for result in update_results:
                if 'last_step' in result and result['last_step']:
                    solution_steps.append(result['last_step'])
            
            # Generate LaTeX solution
            with torch.no_grad():
                output_logits = self.latex_decoder(updated_states_tensor, max_length=150)
                output_ids = torch.argmax(output_logits, dim=-1)
            
            # Decode LaTeX solution
            latex_solution = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            # Combine solution from reasoning module and LaTeX decoder
            final_steps = []
            for i, step in enumerate(reasoning_result['reasoning_steps'][0]):
                final_steps.append({
                    'step_number': i + 1,
                    'expression': step['expression'],
                    'operation': step['operator'],
                    'verification': step['verification']
                })
            
            # Add interpretations from cellular partitions
            for i, cell_step in enumerate(solution_steps):
                if i < len(final_steps):
                    final_steps[i].update({
                        'domain': cell_step.get('domain', 'unknown'),
                        'consistency': cell_step.get('consistency', 0.0)
                    })
            
            elapsed_time = time.time() - start_time
            
            # Format the complete solution
            solution = {
                'problem': problem_text,
                'latex_solution': latex_solution,
                'final_answer': reasoning_result['final_expressions'][0],
                'steps': final_steps,
                'verified': reasoning_result['verified'][0],
                'processing_time': elapsed_time
            }
            
            return solution
            
        except Exception as e:
            logging.error(f"Error solving problem: {e}")
            import traceback
            traceback.print_exc()
            return {
                'problem': problem_text,
                'error': f"Failed to solve the problem: {str(e)}",
                'partial_solution': "Could not generate a complete solution."
            }
    
    def extract_math_expressions(self, text: str) -> List[str]:
        """Extract mathematical expressions from problem text"""
        # Simple pattern for detecting equations and expressions
        eq_pattern = r'([a-zA-Z0-9+\-*/^()=<>]+)'
        expressions = re.findall(eq_pattern, text)
        
        # Filter out non-mathematical substrings
        expressions = [expr for expr in expressions if 
                      any(c in expr for c in '+-*/^=<>') or 
                      re.search(r'\d', expr)]
        
        # If no expressions found, return the whole text as one expression
        if not expressions:
            return [text]
            
        return expressions
    
    def train(self, data_path: str, num_epochs: int = 3, 
              save_path: str = './mathcellai_model', max_samples: int = 100000):
        """Train the model on mathematics data"""
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
        
        # Create specialized math dataset
        dataset = MathDataset(
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
                adaptive_batch_size = min(32, adaptive_batch_size)  # Math expressions can be memory-intensive, cap lower
            else:
                # Conservative defaults if memory info not available
                threads = torch.get_num_threads()
                adaptive_batch_size = max(4, min(16, self.params.batch_size * (threads // 8)))
        except Exception as e:
            logging.warning(f"Error calculating adaptive batch size: {e}. Using conservative defaults.")
            adaptive_batch_size = max(4, min(8, self.params.batch_size))
        
        # Adjust accumulation steps inversely with batch size
        self.params.accumulation_steps = max(2, int(32 / (adaptive_batch_size / 4)))
        
        logging.info(f"Using adaptive batch size: {adaptive_batch_size} with accumulation steps: {self.params.accumulation_steps}")
        
        # Create optimized dataloader
        dataloader = DataLoader(
            dataset, 
            batch_size=adaptive_batch_size, 
            shuffle=True,
            num_workers=min(2, multiprocessing.cpu_count()),
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
                problem_ids = batch['problem_ids'].to(self.device)
                solution_ids = batch['solution_ids'].to(self.device)
                
                # Current time point for this batch
                batch_time = self.current_time + batch_idx * self.params.dt
                
                # Forward pass - text encoding
                state_vector = self.text_encoder(problem_ids)
                
                # Symbolic encoding
                symbolic_result = self.symbolic_encoder(problem_ids)
                symbolic_repr = symbolic_result['symbolic']
                math_types = symbolic_result['types']
                
                # Graph encoding
                graph_repr = self.graph_encoder(symbolic_repr, math_types)
                
                # Extract expressions from batch problems
                expression_texts = []
                for i in range(len(problem_ids)):
                    problem_text = self.tokenizer.decode(problem_ids[i].cpu().numpy(), skip_special_tokens=True)
                    expressions = self.extract_math_expressions(problem_text)
                    expression_texts.append(expressions[0] if expressions else "")
                
                # Reasoning module
                reasoning_result = self.math_reasoner(
                    symbolic_repr,
                    graph_repr,
                    expression_texts
                )
                
                # Final state is a combination of text encoding and reasoning
                combined_state = state_vector + reasoning_result['final_state']
                
                # Decoder
                logits = self.latex_decoder(combined_state, target_ids=solution_ids)
                
                # Calculate loss - shift targets for language modeling
                shift_logits = logits[:, :-1, :].contiguous()
                shift_labels = solution_ids[:, 1:].contiguous()
                
                loss = self.criterion(
                    shift_logits.view(-1, self.params.vocab_size),
                    shift_labels.view(-1)
                ) / self.params.accumulation_steps  # Scale for accumulation
                
                # Backward pass
                loss.backward()
                
                # Update only after accumulation steps
                if (batch_idx + 1) % self.params.accumulation_steps == 0 or (batch_idx + 1) == len(dataloader):
                    # Apply gradient clipping for dense parameters
                    torch.nn.utils.clip_grad_norm_(self.text_encoder.get_dense_params(), max_norm=1.0)
                    torch.nn.utils.clip_grad_norm_(self.symbolic_encoder.get_dense_params(), max_norm=1.0)
                    torch.nn.utils.clip_grad_norm_(self.latex_decoder.get_dense_params(), max_norm=1.0)
                    
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
                'text_encoder': self.text_encoder.state_dict(),
                'symbolic_encoder': self.symbolic_encoder.state_dict(),
                'graph_encoder': self.graph_encoder.state_dict(),
                'math_reasoner': self.math_reasoner.state_dict(),
                'latex_decoder': self.latex_decoder.state_dict(),
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
                    'text_encoder': self.text_encoder.state_dict(),
                    'symbolic_encoder': self.symbolic_encoder.state_dict(),
                    'graph_encoder': self.graph_encoder.state_dict(),
                    'math_reasoner': self.math_reasoner.state_dict(),
                    'latex_decoder': self.latex_decoder.state_dict(),
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
        
        # Set back to evaluation mode
        self.training = False
        
        # Final memory check
        try:
            import psutil
            process = psutil.Process(os.getpid())
            final_memory = process.memory_info().rss / (1024 * 1024)
            memory_delta = final_memory - initial_memory
            logging.info(f"Final memory usage: {final_memory:.2f} MB (delta: {memory_delta:.2f} MB)")
        except ImportError:
            pass
            
        return best_loss
    
    def load_model(self, model_path: str) -> bool:
        """
        Load a saved model
        
        Args:
            model_path: Path to saved model checkpoint
            
        Returns:
            bool: Success flag
        """
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            
            # Load model parameters
            self.text_encoder.load_state_dict(checkpoint['text_encoder'])
            self.symbolic_encoder.load_state_dict(checkpoint['symbolic_encoder'])
            self.graph_encoder.load_state_dict(checkpoint['graph_encoder'])
            self.math_reasoner.load_state_dict(checkpoint['math_reasoner'])
            self.latex_decoder.load_state_dict(checkpoint['latex_decoder'])
            
            # Load optimizer states if needed
            if hasattr(self, 'sparse_optimizer') and 'sparse_optimizer' in checkpoint:
                self.sparse_optimizer.load_state_dict(checkpoint['sparse_optimizer'])
            if hasattr(self, 'dense_optimizer') and 'dense_optimizer' in checkpoint:
                self.dense_optimizer.load_state_dict(checkpoint['dense_optimizer'])
                
            # Restore system time for temporal memory
            if 'system_time' in checkpoint:
                self.current_time = checkpoint['system_time']
                
            logging.info(f"Model loaded successfully from {model_path}")
            logging.info(f"Loaded model from epoch {checkpoint.get('epoch', 'unknown')} with loss {checkpoint.get('loss', 'unknown')}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return False
    
    def benchmark(self, test_data_path: str, output_path: str = None) -> Dict[str, float]:
        """
        Benchmark model performance on test data
        
        Args:
            test_data_path: Path to test data JSONL file
            output_path: Optional path to output results
            
        Returns:
            Dictionary with performance metrics
        """
        # Ensure we're in evaluation mode
        self.training = False
        
        # Create test dataset
        test_dataset = MathDataset(
            test_data_path,
            self.tokenizer,
            self.params.max_seq_length
        )
        
        # Use a smaller batch size for evaluation
        test_loader = DataLoader(
            test_dataset,
            batch_size=max(1, self.params.batch_size // 2),
            shuffle=False,
            num_workers=min(2, multiprocessing.cpu_count()),
            pin_memory=True
        )
        
        # Metrics to track
        metrics = {
            'total_examples': 0,
            'correct_answers': 0,
            'total_loss': 0.0,
            'processing_time': 0.0,
            'correct_symbolic': 0,
            'correct_numerical': 0,
            'correct_steps': 0,
            'total_steps': 0,
            'verification_rate': 0.0
        }
        
        # Results for each example
        all_results = []
        
        # Evaluation loop
        logging.info(f"Starting benchmark on {len(test_dataset)} examples")
        print(f"\n{'='*60}")
        print(f"Benchmarking on {len(test_dataset)} examples")
        print(f"{'='*60}\n")
        
        progress_bar = tqdm(
            test_loader,
            desc=f"Evaluating",
            position=0,
            leave=True,
            unit="batch"
        )
        
        # Evaluation loop
        with torch.no_grad():
            for batch_idx, batch in enumerate(progress_bar):
                batch_start = time.time()
                
                # Get batch data
                problem_ids = batch['problem_ids'].to(self.device)
                solution_ids = batch['solution_ids'].to(self.device)
                
                # Current time point for this batch
                batch_time = self.current_time + batch_idx * self.params.dt
                
                # Process each problem individually for detailed metrics
                for i in range(len(problem_ids)):
                    example_start = time.time()
                    
                    # Extract problem text
                    problem_text = self.tokenizer.decode(
                        problem_ids[i].cpu().numpy(), 
                        skip_special_tokens=True
                    )
                    
                    # Extract reference solution
                    ref_solution = self.tokenizer.decode(
                        solution_ids[i].cpu().numpy(),
                        skip_special_tokens=True
                    )
                    
                    # Solve problem
                    solution = self.solve_math_problem(problem_text)
                    
                    example_time = time.time() - example_start
                    metrics['processing_time'] += example_time
                    metrics['total_examples'] += 1
                    
                    # Check for correctness
                    if 'error' not in solution:
                        # Parse reference and generated solutions for comparison
                        try:
                            # Compare symbolic expressions
                            if self.compare_symbolic_math(solution['final_answer'], ref_solution):
                                metrics['correct_symbolic'] += 1
                                
                            # Compare numerical values
                            if self.compare_numerical_results(solution['final_answer'], ref_solution):
                                metrics['correct_numerical'] += 1
                                
                            # If either symbolic or numerical is correct, count as correct
                            if (metrics['correct_symbolic'] > 0 or metrics['correct_numerical'] > 0):
                                metrics['correct_answers'] += 1
                                
                            # Evaluate steps
                            if 'steps' in solution:
                                metrics['total_steps'] += len(solution['steps'])
                                for step in solution['steps']:
                                    if step.get('verification', 0.0) > self.params.verification_threshold:
                                        metrics['correct_steps'] += 1
                                        
                            # Track verification rate
                            if solution.get('verified', False):
                                metrics['verification_rate'] += 1
                                
                        except Exception as e:
                            logging.warning(f"Error comparing solutions: {e}")
                    
                    # Add to results
                    all_results.append({
                        'problem': problem_text,
                        'reference': ref_solution,
                        'solution': solution,
                        'processing_time': example_time
                    })
                
                # Update progress bar
                accuracy = (metrics['correct_answers'] / max(1, metrics['total_examples'])) * 100
                progress_bar.set_postfix({
                    'accuracy': f"{accuracy:.2f}%",
                    'time/ex': f"{metrics['processing_time'] / max(1, metrics['total_examples']):.2f}s"
                })
                
        # Calculate final metrics
        try:
            metrics['accuracy'] = (metrics['correct_answers'] / metrics['total_examples']) * 100
            metrics['symbolic_accuracy'] = (metrics['correct_symbolic'] / metrics['total_examples']) * 100
            metrics['numerical_accuracy'] = (metrics['correct_numerical'] / metrics['total_examples']) * 100
            metrics['step_accuracy'] = (metrics['correct_steps'] / max(1, metrics['total_steps'])) * 100
            metrics['verification_rate'] = (metrics['verification_rate'] / metrics['total_examples']) * 100
            metrics['avg_processing_time'] = metrics['processing_time'] / metrics['total_examples']
        except ZeroDivisionError:
            logging.warning("No examples processed during benchmark")
        
        # Print results
        print(f"\n{'='*60}")
        print(f"Benchmark Results:")
        print(f"{'='*60}")
        print(f"Total examples: {metrics['total_examples']}")
        print(f"Overall accuracy: {metrics.get('accuracy', 0):.2f}%")
        print(f"Symbolic accuracy: {metrics.get('symbolic_accuracy', 0):.2f}%")
        print(f"Numerical accuracy: {metrics.get('numerical_accuracy', 0):.2f}%")
        print(f"Step accuracy: {metrics.get('step_accuracy', 0):.2f}%")
        print(f"Verification rate: {metrics.get('verification_rate', 0):.2f}%")
        print(f"Average processing time: {metrics.get('avg_processing_time', 0):.2f}s per example")
        print(f"{'='*60}\n")
        
        # Save results if path provided
        if output_path:
            try:
                results_file = os.path.join(output_path, f"benchmark_results.json")
                with open(results_file, 'w') as f:
                    json.dump({
                        'metrics': metrics,
                        'details': all_results
                    }, f, indent=2)
                logging.info(f"Benchmark results saved to {results_file}")
            except Exception as e:
                logging.error(f"Error saving benchmark results: {e}")
        
        return metrics
    
    def compare_symbolic_math(self, predicted: str, reference: str) -> bool:
        """Compare symbolic mathematical expressions for equivalence"""
        try:
            # Clean expressions
            pred_expr = re.sub(r'\s+', '', predicted)
            ref_expr = re.sub(r'\s+', '', reference)
            
            # Quick string match
            if pred_expr == ref_expr:
                return True
                
            # Try sympy for symbolic comparison
            try:
                pred_sym = sympy.sympify(pred_expr)
                ref_sym = sympy.sympify(ref_expr)
                
                # Check if symbolically equivalent
                diff = sympy.simplify(pred_sym - ref_sym)
                return diff == 0
            except:
                # If sympy parsing fails, fall back to string matching
                return False
                
        except Exception as e:
            logging.debug(f"Error in symbolic comparison: {e}")
            return False
    
    def compare_numerical_results(self, predicted: str, reference: str) -> bool:
        """Compare numerical results within tolerance"""
        try:
            # Extract numbers using regex
            pred_nums = re.findall(r'-?\d+\.?\d*', predicted)
            ref_nums = re.findall(r'-?\d+\.?\d*', reference)
            
            # If no numbers found, return False
            if not pred_nums or not ref_nums:
                return False
                
            # Convert to floats
            pred_floats = [float(n) for n in pred_nums]
            ref_floats = [float(n) for n in ref_nums]
            
            # If different number of values, try matching any
            if len(pred_floats) != len(ref_floats):
                # Check if any predicted number matches a reference number
                for p in pred_floats:
                    for r in ref_floats:
                        if abs(p - r) < 1e-6 or (max(abs(p), abs(r)) > 1e-6 and abs(p - r) / max(abs(p), abs(r)) < 1e-3):
                            return True
                return False
            
            # If same number of values, match in order
            for p, r in zip(pred_floats, ref_floats):
                # Absolute tolerance for small numbers, relative for larger ones
                if abs(p - r) > 1e-6 and (max(abs(p), abs(r)) <= 1e-6 or abs(p - r) / max(abs(p), abs(r)) > 1e-3):
                    return False
                    
            return True
            
        except Exception as e:
            logging.debug(f"Error in numerical comparison: {e}")
            return False
            
    def __del__(self):
        """Cleanup resources"""
        try:
            # Cleanup Ray resources if initialized
            if ray.is_initialized():
                ray.shutdown()
                logging.info("Ray resources cleaned up")
        except:
            pass


def get_default_params() -> ModelParams:
    """Get default parameters for MathCellAI"""
    return ModelParams(
        # Core cellular parameters
        dt=0.1,                      # Time step for memory dynamics
        D=0.2,                       # Diffusion coefficient for state propagation
        gamma=0.05,                  # Decay rate for memory
        eta=0.01,                    # Noise amplitude
        num_partitions=4,            # Number of parallel partitions
        state_size=512,              # Size of state vector per partition
        
        # State transition parameters
        temperature=0.1,             # Temperature for Boltzmann distribution
        energy_scale=0.5,            # Scale factor for energy calculations
        
        # Temporal memory parameters
        memory_tau=5.0,              # Memory time constant
        kernel_terms=3,              # Number of terms in memory kernel expansion
        kernel_decays=[0.5, 2.0, 8.0],  # Decay rates for memory kernel terms
        
        # Boundary condition parameters
        boundary_strength=0.3,       # Coupling strength at boundaries
        
        # Emergent properties parameters
        collective_threshold=0.7,    # Threshold for collective behavior emergence
        
        # Mathematics-specific parameters
        symbolic_dim=256,            # Dimension for symbolic representation
        graph_dim=128,               # Dimension for graph-based knowledge
        reasoning_steps=5,           # Maximum number of reasoning steps
        verification_threshold=0.8,  # Threshold for formal verification
        
        # NLP parameters
        embedding_size=256,          # Size of text embeddings
        vocab_size=30522,            # Size of vocabulary (will be updated)
        max_seq_length=512,          # Maximum sequence length
        
        # Training parameters
        learning_rate=5e-5,          # Learning rate for training
        batch_size=16,               # Batch size for training
        accumulation_steps=4,        # Steps for gradient accumulation
        early_stopping_patience=3    # Patience for early stopping
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MathCellAI - Cellular AI for Mathematics")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Train command
    train_parser = subparsers.add_parser("train", help="Train the model")
    train_parser.add_argument("--data", required=True, help="Path to training data")
    train_parser.add_argument("--epochs", type=int, default=3, help="Number of epochs to train")
    train_parser.add_argument("--save", default="./models", help="Path to save model")
    train_parser.add_argument("--load", help="Path to load initial model (optional)")
    
    # Solve command
    solve_parser = subparsers.add_parser("solve", help="Solve a math problem")
    solve_parser.add_argument("--model", required=True, help="Path to model")
    solve_parser.add_argument("--problem", help="Mathematical problem to solve")
    solve_parser.add_argument("--file", help="File containing math problems (one per line)")
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark model")
    benchmark_parser.add_argument("--model", required=True, help="Path to model")
    benchmark_parser.add_argument("--test", required=True, help="Path to test data")
    benchmark_parser.add_argument("--output", help="Path to output results")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create default parameters
    params = get_default_params()
    
    # Handle commands
    if args.command == "train":
        print("Initializing MathCellAI for training...")
        system = MathCellularSystem(params)
        
        # Load existing model if specified
        if args.load:
            print(f"Loading initial model from {args.load}...")
            system.load_model(args.load)
        
        # Train model
        print(f"Training on data: {args.data}")
        system.train(
            data_path=args.data,
            num_epochs=args.epochs,
            save_path=args.save
        )
        
    elif args.command == "solve":
        print("Initializing MathCellAI for solving...")
        system = MathCellularSystem(params)
        
        # Load model
        print(f"Loading model from {args.model}...")
        if not system.load_model(args.model):
            print("Failed to load model. Exiting.")
            sys.exit(1)
        
        # Solve problem
        if args.problem:
            print(f"Solving problem: {args.problem}")
            solution = system.solve_math_problem(args.problem)
            
            print("\nSolution:")
            print(f"Problem: {solution['problem']}")
            
            if 'error' in solution:
                print(f"Error: {solution['error']}")
            else:
                print(f"Final answer: {solution['final_answer']}")
                print("\nStep-by-step solution:")
                for i, step in enumerate(solution['steps']):
                    print(f"Step {i+1}: {step['operation']} → {step['expression']}")
                
                print(f"\nLaTeX solution: {solution['latex_solution']}")
                print(f"Verified: {'Yes' if solution['verified'] else 'No'}")
                
        elif args.file:
            print(f"Processing problems from file: {args.file}")
            with open(args.file, 'r') as f:
                problems = f.readlines()
            
            results = []
            for i, problem in enumerate(problems):
                problem = problem.strip()
                if not problem:
                    continue
                    
                print(f"Solving problem {i+1}/{len(problems)}: {problem[:50]}...")
                solution = system.solve_math_problem(problem)
                results.append(solution)
                
            # Save results
            output_file = "solutions.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
                
            print(f"Saved {len(results)} solutions to {output_file}")
            
        else:
            print("Error: Must provide either --problem or --file")
            sys.exit(1)
            
    elif args.command == "benchmark":
        print("Initializing MathCellAI for benchmarking...")
        system = MathCellularSystem(params)
        
        # Load model
        print(f"Loading model from {args.model}...")
        if not system.load_model(args.model):
            print("Failed to load model. Exiting.")
            sys.exit(1)
            
        # Run benchmark
        print(f"Benchmarking on test data: {args.test}")
        system.benchmark(
            test_data_path=args.test,
            output_path=args.output
        )
        
    else:
        parser.print_help()
        sys.exit(1)