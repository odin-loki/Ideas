"""
CellAI_TradCode - Complete Cellular AI Framework for Software Analysis and Generation

This implementation combines:
1. The complete CellAI mathematical framework adapted for code:
   - Cellular Equation: dS/dt = f(I, S, t) - γS + D∇²S + η(t)
   - Probabilistic State Transitions: P(Si→Sj) = exp(-ΔEij/kT) / Z
   - Temporal Memory Integration: M(t) = ∫[t-τ, t] w(t-s)I(s)ds + ∫[0, t] K(t-s)S(s)ds
   - Detailed Boundary Conditions: B(Sᵢ, Sⱼ) = 0 for adjacent partitions
   - Emergent Properties Framework for collective code pattern recognition

2. Comprehensive code processing using ALL features from Code-Dataset-Processor:
   - Complete AST (Abstract Syntax Tree) processing
   - Full graph-based representations (CFG, DFG, PDG, dependency graphs)
   - Bytecode compilation and analysis
   - Execution trace generation and analysis
   - Version history tracking and analysis
   - Code metrics and quality analysis
   - Algorithm pattern recognition
   - Security vulnerability detection
   - Natural language description processing

3. Highly optimized processing pipeline:
   - Memory-mapped dataset handling for large codebases
   - Efficient checkpointing for reduced memory usage
   - Parallel data loading and preprocessing
   - Batch processing with gradient accumulation
   - Optimized Ray configuration for multicore processing

Usage:
  - Train: python CellAI_TradCode.py train --data /path/to/code_dataset.jsonl.gz --epochs 3
  - Generate: python CellAI_TradCode.py generate --model /path/to/model.pt --prompt "def fibonacci"
  - Analyze: python CellAI_TradCode.py analyze --model /path/to/model.pt --code /path/to/code.py
  - Benchmark: python CellAI_TradCode.py benchmark --model /path/to/model.pt --test /path/to/test.jsonl
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
import ast
import json
import gzip
import time
import os
import multiprocessing
import mmap
import argparse
from tqdm import tqdm
from torch.utils.checkpoint import checkpoint
import networkx as nx
import atexit
import math
import re
import marshal
import base64
import tempfile
import importlib.util
import dis
import traceback
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union, Set

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

# ============================================================================
# Core Parameters Definition
# ============================================================================

@dataclass
class ModelParams:
    """Combined parameters for optimized CodeCellAI with full mathematical framework"""
    # Core cellular parameters
    dt: float                 # Time step for memory dynamics
    D: float                  # Diffusion coefficient for state propagation
    gamma: float              # Decay rate for memory
    eta: float                # Noise amplitude (for η(t))
    num_partitions: int       # Number of parallel partitions
    state_size: int           # Size of state vector per partition
    
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
    
    # Code parameters
    embedding_size: int       # Size of code embeddings
    vocab_size: int           # Size of code token vocabulary
    max_seq_length: int       # Maximum sequence length
    max_ast_nodes: int        # Maximum number of AST nodes
    max_graph_nodes: int      # Maximum number of graph nodes (CFG, DFG, PDG)
    max_bytecode_instr: int   # Maximum number of bytecode instructions
    max_trace_events: int     # Maximum number of execution trace events
    max_versions: int         # Maximum number of version history entries
    
    # Training parameters
    learning_rate: float      # Learning rate for training
    batch_size: int           # Batch size for training
    accumulation_steps: int   # Steps for gradient accumulation
    early_stopping_patience: int  # Patience for early stopping

# ============================================================================
# Data Loading and Processing
# ============================================================================

class MemoryMappedCodeDataset(Dataset):
    """Memory-mapped dataset class for large code datasets"""
    def __init__(self, data_path: str, tokenizer, max_length: int = 512, include_graphs: bool = True):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.include_graphs = include_graphs
        
        # Check if the file is gzipped
        self.is_gzipped = data_path.endswith('.gz')
        
        if not self.is_gzipped:
            # Memory map the data file for uncompressed files
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
        else:
            # For gzipped files, we'll need a different approach
            # We'll read the entire file into memory and parse it
            logging.info("Reading gzipped dataset...")
            with gzip.open(data_path, 'rt') as f:
                self.data = [line for line in tqdm(f)]
            logging.info(f"Loaded {len(self.data)} samples")
    
    def _count_lines(self, filepath):
        """Count lines in a file"""
        with open(filepath, 'r') as f:
            return sum(1 for _ in f)
    
    def __len__(self):
        if hasattr(self, 'line_offsets'):
            return len(self.line_offsets)
        else:
            return len(self.data)
    
    def __getitem__(self, idx):
        """Get item with consistent dimensions for batching"""
        if hasattr(self, 'mm'):
            # Seek to the correct position in memory-mapped file
            self.mm.seek(self.line_offsets[idx])
            line = self.mm.readline().decode('utf-8')
        else:
            # Get line from in-memory data
            line = self.data[idx]
        
        # Default values
        code = ''
        metrics = {}
        labels = {}
        algorithms = []
        vulnerabilities = []
        
        # Fixed dimensions for output tensors
        fixed_metrics_size = 5
        fixed_patterns_size = 5
        fixed_vulnerabilities_size = 3
        
        try:
            item = json.loads(line)
            code = item.get('code', '')
            
            # Get metrics and labels
            metrics = item.get('metrics', {})
            labels = item.get('labels', {})
            algorithms = item.get('algorithms', [])
            vulnerabilities = item.get('security_vulnerabilities', [])
            nl_description = item.get('natural_language_description', '')
        except:
            # If there's an error parsing, use default values
            nl_description = ''
            
        # Tokenize code
        encodings = self.tokenizer.encode(
            code, 
            max_length=self.max_length,
            padding=True
        )
        
        # Create feature vector with FIXED dimensions
        features = [0.0] * fixed_metrics_size  # Start with all zeros
        
        # Try to extract meaningful metrics
        if 'cyclomatic_complexity' in metrics:
            features[0] = min(1.0, metrics['cyclomatic_complexity'] / 20.0)
        if 'function_count' in metrics:
            features[1] = min(1.0, metrics['function_count'] / 10.0)
        if 'class_count' in metrics:
            features[2] = min(1.0, metrics['class_count'] / 5.0)
        if 'loc' in metrics:
            features[3] = min(1.0, metrics['loc'] / 200.0)
        if 'cognitive_complexity' in metrics:
            features[4] = min(1.0, metrics['cognitive_complexity'] / 30.0)
                
        # Create algorithm pattern vector with FIXED dimensions
        pattern_vector = [0.0] * fixed_patterns_size  # Start with all zeros
        for i, algo in enumerate(algorithms[:fixed_patterns_size]):
            if isinstance(algo, dict) and 'name' in algo:
                pattern_vector[i] = 1.0
            elif isinstance(algo, str):
                pattern_vector[i] = 1.0
                
        # Create vulnerability vector with FIXED dimensions
        vuln_vector = [0.0] * fixed_vulnerabilities_size  # Start with all zeros
        for i, vuln in enumerate(vulnerabilities[:fixed_vulnerabilities_size]):
            if isinstance(vuln, dict) and 'type' in vuln:
                vuln_vector[i] = 1.0
            elif isinstance(vuln, str):
                vuln_vector[i] = 1.0
        
        # Create return dictionary with consistent keys and value dimensions
        return_dict = {
            'input_ids': encodings['input_ids'],
            'attention_mask': encodings['attention_mask'],
            'metrics': torch.tensor(features, dtype=torch.float32),
            'patterns': torch.tensor(pattern_vector, dtype=torch.float32),
            'vulnerabilities': torch.tensor(vuln_vector, dtype=torch.float32),
            'code': code,
            'nl_description': nl_description,
            
            # Use empty structures instead of None for complex types
            # This allows the default collate to work properly
            'ast': {},  # Empty dict instead of None
            'cfg': {},  # Empty dict instead of None
            'dfg': {},  # Empty dict instead of None
            'pdg': {},  # Empty dict instead of None
            'bytecode': {},  # Empty dict instead of None
            'execution_trace': {},  # Empty dict instead of None
            'version_history': []  # Empty list instead of None
        }
        
        return return_dict
        
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


# ============================================================================
# Code Tokenization
# ============================================================================

class CodeTokenizer:
    """Tokenizer for code with specialized handling for language syntax"""
    def __init__(self, vocab_size: int = 50000):
        self.vocab_size = vocab_size
        
        # Predefined special tokens
        self.special_tokens = {
            "<PAD>": 0,
            "<BOS>": 1,
            "<EOS>": 2,
            "<UNK>": 3,
            "<MASK>": 4,
        }
        
        # Python-specific tokens
        self.python_keywords = {
            "def", "class", "if", "else", "elif", "for", "while", 
            "try", "except", "finally", "with", "import", "from", 
            "as", "return", "pass", "break", "continue", "in", "is", 
            "not", "and", "or", "False", "True", "None", "lambda",
            "async", "await", "yield"
        }
        
        # Common code tokens and operators
        self.operators = {
            "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", 
            ">=", "+=", "-=", "*=", "/=", "&", "|", "^", "~", "<<", ">>",
            "->", ".", ",", ":", ";", "(", ")", "[", "]", "{", "}", "@"
        }
        
        # Initialize vocabulary with special tokens
        self.token_to_id = {token: idx for token, idx in self.special_tokens.items()}
        self.id_to_token = {idx: token for token, idx in self.special_tokens.items()}
        
        # Add Python keywords and operators to the vocabulary
        current_idx = len(self.token_to_id)
        for token in self.python_keywords:
            self.token_to_id[token] = current_idx
            self.id_to_token[current_idx] = token
            current_idx += 1
            
        for token in self.operators:
            self.token_to_id[token] = current_idx
            self.id_to_token[current_idx] = token
            current_idx += 1
        
        # Remaining vocabulary slots will be filled during training
        self.next_idx = current_idx
    
    def tokenize(self, code: str) -> List[str]:
        """Tokenize code string into list of tokens"""
        # Basic tokenization using regex
        # This is a simplified version - a full tokenizer would use a code-specific lexer
        pattern = r'[\w\.]+|[^\w\s]'
        tokens = re.findall(pattern, code)
        
        # Add special tokens
        tokens = ["<BOS>"] + tokens + ["<EOS>"]
        return tokens
    
    def encode(self, code: str, max_length: int = 512, padding: bool = True) -> Dict[str, torch.Tensor]:
        """Encode code string into token IDs"""
        tokens = self.tokenize(code)
        
        # Convert tokens to IDs
        token_ids = []
        for token in tokens:
            if token in self.token_to_id:
                token_ids.append(self.token_to_id[token])
            else:
                token_ids.append(self.token_to_id["<UNK>"])
        
        # Truncate if needed
        if len(token_ids) > max_length:
            token_ids = token_ids[:max_length-1] + [self.token_to_id["<EOS>"]]
        
        # Create attention mask
        attention_mask = [1] * len(token_ids)
        
        # Add padding if needed
        if padding and len(token_ids) < max_length:
            padding_length = max_length - len(token_ids)
            token_ids = token_ids + [self.token_to_id["<PAD>"]] * padding_length
            attention_mask = attention_mask + [0] * padding_length
        
        return {
            "input_ids": torch.tensor(token_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long)
        }
    
    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        """Decode token IDs back to code string"""
        tokens = []
        for token_id in token_ids:
            if token_id in self.id_to_token:
                token = self.id_to_token[token_id]
                if skip_special_tokens and token in self.special_tokens:
                    continue
                tokens.append(token)
            else:
                tokens.append(self.id_to_token[self.token_to_id["<UNK>"]])
        
        # Reconstruct code - this is simplified
        code = " ".join(tokens)
        
        # Fix spacing around operators and punctuation - a full tokenizer would do this better
        for op in self.operators:
            if len(op) == 1 and op not in {'.', '@'}:  # Don't add spaces around dots or decorators
                code = code.replace(f" {op} ", op)
                code = code.replace(f"{op} ", op)
                code = code.replace(f" {op}", op)
        
        # Fix common patterns
        code = code.replace("( ", "(").replace(" )", ")")
        code = code.replace("[ ", "[").replace(" ]", "]")
        code = code.replace("{ ", "{").replace(" }", "}")
        
        return code
    
    def update_vocabulary(self, code_samples: List[str], min_freq: int = 2):
        """Update vocabulary from code samples"""
        # Count token frequencies
        token_freq = {}
        for code in tqdm(code_samples, desc="Updating vocabulary"):
            tokens = self.tokenize(code)
            for token in tokens:
                if token not in self.token_to_id:
                    token_freq[token] = token_freq.get(token, 0) + 1
        
        # Sort by frequency and keep most common tokens
        sorted_tokens = sorted(token_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Add tokens that meet minimum frequency until vocab size is reached
        for token, freq in sorted_tokens:
            if freq >= min_freq and self.next_idx < self.vocab_size:
                self.token_to_id[token] = self.next_idx
                self.id_to_token[self.next_idx] = token
                self.next_idx += 1
        
        logging.info(f"Vocabulary updated to {len(self.token_to_id)} tokens")

# ============================================================================
# Advanced Graph Processing
# ============================================================================

class AdvancedGraphProcessor:
    """
    Advanced processor for code graphs that fully implements all graph representations
    from the Code-Dataset-Processor.
    """
    def __init__(self, max_nodes: int = 1000):
        self.max_nodes = max_nodes
        
    def generate_dfg(self, code: str) -> nx.DiGraph:
        """
        Generate a complete Data Flow Graph from code
        
        Implements the full DFG algorithm from Code-Dataset-Processor
        """
        try:
            tree = ast.parse(code)
            graph = nx.DiGraph()

            variables = {}
            node_id = 0

            def process_expression(expr, parent_id, graph, variables):
                """Process expressions to connect variable uses to their definitions"""
                if isinstance(expr, ast.Name) and isinstance(expr.ctx, ast.Load):
                    var_name = expr.id
                    if var_name in variables and variables[var_name]:
                        graph.add_edge(variables[var_name][-1], parent_id)
                elif isinstance(expr, ast.BinOp):
                    process_expression(expr.left, parent_id, graph, variables)
                    process_expression(expr.right, parent_id, graph, variables)
                elif isinstance(expr, ast.Call):
                    for arg in expr.args:
                        process_expression(arg, parent_id, graph, variables)

            def visit_node(node):
                nonlocal node_id

                # Track variable assignments and usages
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            if var_name not in variables:
                                variables[var_name] = []

                            # Create new definition node
                            def_id = node_id
                            node_id += 1
                            graph.add_node(def_id, label=f"Def: {var_name}")
                            variables[var_name].append(def_id)

                            # Connect to any variables used in the right side
                            process_expression(node.value, def_id, graph, variables)
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    var_name = node.id
                    if var_name in variables and variables[var_name]:
                        # This is a variable use - connect to most recent definition
                        use_id = node_id
                        node_id += 1
                        graph.add_node(use_id, label=f"Use: {var_name}")
                        graph.add_edge(variables[var_name][-1], use_id)

                # Visit child nodes
                for child in ast.iter_child_nodes(node):
                    visit_node(child)

            visit_node(tree)
            return graph
        except Exception as e:
            logging.error(f"Error generating DFG: {e}")
            return nx.DiGraph()
    
    def generate_pdg(self, code: str) -> nx.DiGraph:
        """
        Generate a complete Program Dependence Graph (combines control and data dependencies)
        
        Implements the full PDG algorithm from Code-Dataset-Processor
        """
        try:
            # Generate CFG first
            cfg = self.generate_cfg(code)
            # Generate DFG
            dfg = self.generate_dfg(code)
            
            # Create a new graph for the PDG
            pdg = nx.DiGraph()
            
            # Add all nodes from both graphs
            for node, data in cfg.nodes(data=True):
                pdg.add_node(f"c{node}", label=data.get("label", ""), type="control")
            
            for node, data in dfg.nodes(data=True):
                pdg.add_node(f"d{node}", label=data.get("label", ""), type="data")
            
            # Add all edges from both graphs
            for u, v in cfg.edges():
                pdg.add_edge(f"c{u}", f"c{v}", type="control")
            
            for u, v in dfg.edges():
                pdg.add_edge(f"d{u}", f"d{v}", type="data")
            
            return pdg
        except Exception as e:
            logging.error(f"Error generating PDG: {e}")
            return nx.DiGraph()

    def generate_cfg(self, code: str) -> nx.DiGraph:
        """
        Generate a complete Control Flow Graph with control structures
        
        Enhanced version of the CFG algorithm from Code-Dataset-Processor
        """
        try:
            tree = ast.parse(code)
            graph = nx.DiGraph()
            
            # For tracking nodes and edges
            node_id = 0
            entry_exit = {}  # Maps AST nodes to (entry_id, exit_id) tuples
            
            def create_graph_node(label):
                """Create a new node in the graph with the given label"""
                nonlocal node_id
                current_id = node_id
                graph.add_node(current_id, label=label)
                node_id += 1
                return current_id
            
            def process_node(node, parent_id=None):
                """Process an AST node and create CFG nodes and edges"""
                if isinstance(node, ast.FunctionDef):
                    # Function definition
                    func_entry = create_graph_node(f"Function: {node.name} [Entry]")
                    func_exit = create_graph_node(f"Function: {node.name} [Exit]")
                    entry_exit[node] = (func_entry, func_exit)
                    
                    if parent_id is not None:
                        graph.add_edge(parent_id, func_entry)
                    
                    # Process function body
                    last_node = func_entry
                    for stmt in node.body:
                        last_node = process_node(stmt, last_node)
                    
                    # Connect to exit
                    graph.add_edge(last_node, func_exit)
                    return func_exit
                    
                elif isinstance(node, ast.If):
                    # If statement
                    if_entry = create_graph_node(f"If")
                    if_exit = create_graph_node("If [Exit]")
                    entry_exit[node] = (if_entry, if_exit)
                    
                    if parent_id is not None:
                        graph.add_edge(parent_id, if_entry)
                    
                    # Process true branch
                    true_branch_last = if_entry
                    for stmt in node.body:
                        true_branch_last = process_node(stmt, true_branch_last)
                    graph.add_edge(true_branch_last, if_exit)
                    
                    # Process false branch (if it exists)
                    if node.orelse:
                        false_branch_last = if_entry
                        for stmt in node.orelse:
                            false_branch_last = process_node(stmt, false_branch_last)
                        graph.add_edge(false_branch_last, if_exit)
                    else:
                        # If no else branch, connect if_entry directly to if_exit
                        graph.add_edge(if_entry, if_exit)
                    
                    return if_exit
                    
                elif isinstance(node, ast.For) or isinstance(node, ast.While):
                    # For/While loop
                    is_for = isinstance(node, ast.For)
                    loop_type = "For" if is_for else "While"
                    
                    loop_entry = create_graph_node(f"{loop_type}")
                    loop_exit = create_graph_node(f"{loop_type} [Exit]")
                    entry_exit[node] = (loop_entry, loop_exit)
                    
                    if parent_id is not None:
                        graph.add_edge(parent_id, loop_entry)
                    
                    # Process loop body
                    last_node = loop_entry
                    for stmt in node.body:
                        last_node = process_node(stmt, last_node)
                    
                    # Loop back
                    graph.add_edge(last_node, loop_entry)
                    
                    # Process else clause if it exists
                    if node.orelse:
                        else_last = loop_entry
                        for stmt in node.orelse:
                            else_last = process_node(stmt, else_last)
                        graph.add_edge(else_last, loop_exit)
                    
                    # Exit path
                    graph.add_edge(loop_entry, loop_exit)
                    
                    return loop_exit
                    
                elif isinstance(node, ast.Try):
                    # Try-except-finally
                    try_entry = create_graph_node("Try")
                    try_exit = create_graph_node("Try [Exit]")
                    entry_exit[node] = (try_entry, try_exit)
                    
                    if parent_id is not None:
                        graph.add_edge(parent_id, try_entry)
                    
                    # Process try body
                    try_last = try_entry
                    for stmt in node.body:
                        try_last = process_node(stmt, try_last)
                    
                    # Connect try body to exit
                    graph.add_edge(try_last, try_exit)
                    
                    # Process except handlers
                    for handler in node.handlers:
                        except_entry = create_graph_node(f"Except")
                        graph.add_edge(try_entry, except_entry)
                        
                        # Process except body
                        except_last = except_entry
                        for stmt in handler.body:
                            except_last = process_node(stmt, except_last)
                        
                        # Connect to exit
                        graph.add_edge(except_last, try_exit)
                    
                    # Process else clause
                    if node.orelse:
                        else_last = try_last
                        for stmt in node.orelse:
                            else_last = process_node(stmt, else_last)
                        graph.add_edge(else_last, try_exit)
                    
                    # Process finally
                    if node.finalbody:
                        finally_entry = create_graph_node("Finally")
                        graph.add_edge(try_exit, finally_entry)
                        
                        finally_last = finally_entry
                        for stmt in node.finalbody:
                            finally_last = process_node(stmt, finally_last)
                        
                        # Create a new exit node after finally
                        finally_exit = create_graph_node("Finally [Exit]")
                        graph.add_edge(finally_last, finally_exit)
                        
                        return finally_exit
                    
                    return try_exit
                    
                elif isinstance(node, ast.Return):
                    # Return statement
                    return_node = create_graph_node(f"Return")
                    
                    if parent_id is not None:
                        graph.add_edge(parent_id, return_node)
                    
                    # Find enclosing function's exit node
                    func_node = next((n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and node in ast.walk(n)), None)
                    if func_node and func_node in entry_exit:
                        _, func_exit = entry_exit[func_node]
                        graph.add_edge(return_node, func_exit)
                    
                    return return_node
                    
                else:
                    # Default case: simple statement
                    stmt_node = create_graph_node(type(node).__name__)
                    
                    if parent_id is not None:
                        graph.add_edge(parent_id, stmt_node)
                    
                    return stmt_node
            
            # Start processing from the module level
            module_entry = create_graph_node("Module [Entry]")
            module_exit = create_graph_node("Module [Exit]")
            entry_exit[tree] = (module_entry, module_exit)
            
            # Process all top-level statements
            last_node = module_entry
            for stmt in tree.body:
                last_node = process_node(stmt, last_node)
            
            # Connect to module exit
            graph.add_edge(last_node, module_exit)
            
            return graph
            
        except Exception as e:
            logging.error(f"Error generating CFG: {e}")
            return nx.DiGraph()
            
    def generate_dependency_graph(self, code: str) -> nx.DiGraph:
        """
        Generate a dependency graph showing module/import dependencies
        
        Implements the full dependency graph algorithm from Code-Dataset-Processor
        """
        try:
            tree = ast.parse(code)
            graph = nx.DiGraph()

            # Track module name - we'll use the filename as a fallback
            module_name = "module"

            # Add the main module node
            graph.add_node(module_name, label=module_name, type="module")

            # Find all imports
            import_nodes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        import_name = name.name
                        graph.add_node(import_name, label=import_name, type="external")
                        graph.add_edge(module_name, import_name)
                        import_nodes.append(import_name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        import_name = node.module
                        for name in node.names:
                            full_name = f"{import_name}.{name.name}"
                            graph.add_node(full_name, label=full_name, type="external")
                            graph.add_edge(module_name, full_name)
                            import_nodes.append(full_name)

            # Find all function and class definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = f"{module_name}.{node.name}"
                    graph.add_node(func_name, label=node.name, type="function")
                    graph.add_edge(module_name, func_name)

                    # Check function body for calls to imported modules
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Call) and isinstance(
                            subnode.func, ast.Attribute
                        ):
                            if hasattr(subnode.func, "value") and hasattr(
                                subnode.func.value, "id"
                            ):
                                module_id = subnode.func.value.id
                                if module_id in import_nodes:
                                    attr_name = f"{module_id}.{subnode.func.attr}"
                                    if not graph.has_node(attr_name):
                                        graph.add_node(
                                            attr_name,
                                            label=attr_name,
                                            type="external_function",
                                        )
                                    graph.add_edge(func_name, attr_name)

                elif isinstance(node, ast.ClassDef):
                    class_name = f"{module_name}.{node.name}"
                    graph.add_node(class_name, label=node.name, type="class")
                    graph.add_edge(module_name, class_name)

                    # Add method definitions within class
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_name = f"{class_name}.{item.name}"
                            graph.add_node(method_name, label=item.name, type="method")
                            graph.add_edge(class_name, method_name)

            return graph
        except Exception as e:
            logging.error(f"Error generating dependency graph: {e}")
            return nx.DiGraph()
    
    def serialize_graph(self, graph: nx.DiGraph) -> Dict:
        """Convert a NetworkX graph to a serializable format for neural network processing"""
        # Extract node features
        node_types = []
        node_labels = []
        
        # Create mapping from node id to consecutive integers
        node_mapping = {node: i for i, node in enumerate(graph.nodes())}
        
        # Extract node information
        for node in graph.nodes():
            # Get node type
            node_type = graph.nodes[node].get('type', 'default')
            node_types.append(node_type)
            
            # Get node label
            label = graph.nodes[node].get('label', str(node))
            node_labels.append(label)
        
        # Create adjacency matrix
        n_nodes = len(node_mapping)
        adjacency = np.zeros((n_nodes, n_nodes))
        
        for u, v in graph.edges():
            i, j = node_mapping[u], node_mapping[v]
            adjacency[i, j] = 1.0
            
        # Create node mask (all 1s for now, as we don't have padding yet)
        node_mask = np.ones(n_nodes)
        
        # Handle case with no nodes
        if n_nodes == 0:
            node_types = ['default']
            node_labels = ['empty']
            adjacency = np.zeros((1, 1))
            node_mask = np.ones(1)
            
        # Create tensor-ready dictionary
        tensor_dict = {
            'node_types': node_types,
            'node_labels': node_labels,
            'adjacency': adjacency,
            'node_mask': node_mask
        }
        
        return tensor_dict
    
    def extract_ast_dict(self, code: str) -> Dict:
        """
        Extract Abstract Syntax Tree in dictionary format
        
        Based on AST extraction from Code-Dataset-Generator
        """
        try:
            tree = ast.parse(code)
            
            def ast_to_dict(node):
                if isinstance(node, ast.AST):
                    fields = {}
                    for name, value in ast.iter_fields(node):
                        fields[name] = ast_to_dict(value)
                    return {"node_type": type(node).__name__, "fields": fields}
                elif isinstance(node, list):
                    return [ast_to_dict(item) for item in node]
                else:
                    return node
                    
            return ast_to_dict(tree)
        except Exception as e:
            logging.error(f"Error extracting AST: {e}")
            return {"node_type": "Module", "fields": {}}
    
    def process_code_to_graph_tensors(self, code: str) -> Dict[str, Dict]:
        """Process code into all graph representations ready for tensor conversion"""
        # Generate all graph types
        try:
            ast_dict = self.extract_ast_dict(code)
            cfg = self.generate_cfg(code)
            dfg = self.generate_dfg(code)
            pdg = self.generate_pdg(code)
            dep_graph = self.generate_dependency_graph(code)
            
            # Serialize all graphs
            tensor_dict = {
                'ast': ast_dict,
                'cfg': self.serialize_graph(cfg),
                'dfg': self.serialize_graph(dfg),
                'pdg': self.serialize_graph(pdg),
                'dependency': self.serialize_graph(dep_graph)
            }
            
            return tensor_dict
        except Exception as e:
            logging.error(f"Error processing code to graphs: {e}")
            return {}

# ============================================================================
# Bytecode Analysis
# ============================================================================

class BytecodeAnalyzer:
    """
    Analyzes Python bytecode for performance optimization insights.
    Based on the bytecode analysis from Code-Dataset-Processor.
    """
    def __init__(self):
        self.python_version = sys.version
        
    def generate_bytecode(self, code: str) -> Dict:
        """Compile Python code to bytecode and extract relevant information"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                tmp_filename = tmp.name
                tmp.write(code.encode("utf-8"))

            # Compile to bytecode
            bytecode_filename = tmp_filename + "c"
            py_compile.compile(tmp_filename, bytecode_filename)

            # Check if bytecode file was created
            if not os.path.exists(bytecode_filename):
                logging.warning(f"Bytecode file not created at {bytecode_filename}")
                return {
                    "error": "Bytecode compilation failed",
                    "disassembly": [],
                    "bytecode_b64": "",
                    "python_version": sys.version,
                }
                
            # Read the bytecode file
            with open(bytecode_filename, "rb") as f:
                header_size = 16  # Size of the header for Python 3.7+
                f.read(header_size)  # Skip the header
                code_obj = marshal.load(f)

            # Clean up temporary files
            os.unlink(tmp_filename)
            if os.path.exists(bytecode_filename):
                os.unlink(bytecode_filename)

            # Get disassembly
            disassembly = []
            for instruction in dis.get_instructions(code_obj):
                disassembly.append(
                    {
                        "offset": instruction.offset,
                        "opcode": instruction.opcode,
                        "opname": instruction.opname,
                        "arg": instruction.arg,
                        "argval": repr(instruction.argval),
                        "argrepr": instruction.argrepr,
                    }
                )

            # Get bytecode as base64 for serialization
            with tempfile.NamedTemporaryFile(suffix=".pyc", delete=False) as tmp:
                tmp_filename = tmp.name
                # Write the code to the file
                with open(tmp_filename, "w", encoding="utf-8") as code_file:
                    code_file.write(code)
                # Compile the file
                py_compile.compile(tmp_filename, cfile=tmp_filename + "c", doraise=True)
                with open(tmp_filename + "c", "rb") as f:
                    bytecode_raw = f.read()
                    bytecode_b64 = base64.b64encode(bytecode_raw).decode("ascii")
                os.unlink(tmp_filename)
                if os.path.exists(tmp_filename + "c"):
                    os.unlink(tmp_filename + "c")

            # Return complete bytecode information
            return {
                "disassembly": disassembly,
                "bytecode_b64": bytecode_b64,
                "python_version": sys.version,
            }
        except Exception as e:
            logging.error(f"Error generating bytecode: {e}")
            traceback.print_exc()
            return {
                "error": str(e),
                "disassembly": [],
                "bytecode_b64": "",
                "python_version": sys.version,
            }
    
    def analyze_bytecode_metrics(self, bytecode_info: Dict) -> Dict:
        """Extract metrics and optimization opportunities from bytecode"""
        metrics = {}
        
        if "error" in bytecode_info:
            metrics["error"] = bytecode_info["error"]
            return metrics
            
        disassembly = bytecode_info.get("disassembly", [])
        
        if not disassembly:
            metrics["error"] = "No disassembly available"
            return metrics
            
        # Count total instructions
        metrics["instruction_count"] = len(disassembly)
        
        # Count by opcode type
        opcode_counts = {}
        for instr in disassembly:
            opname = instr["opname"]
            opcode_counts[opname] = opcode_counts.get(opname, 0) + 1
        metrics["opcode_counts"] = opcode_counts
        
        # Flag potential optimization opportunities
        optimizations = []
        
        # Check for excessive LOAD_GLOBAL (could be optimized with locals)
        load_global_count = opcode_counts.get("LOAD_GLOBAL", 0)
        if load_global_count > 20:
            optimizations.append({
                "type": "excessive_global_access",
                "count": load_global_count,
                "recommendation": "Consider using local variables for frequently accessed globals"
            })
            
        # Check for excessive attribute lookups (LOAD_ATTR)
        load_attr_count = opcode_counts.get("LOAD_ATTR", 0)
        if load_attr_count > 20:
            optimizations.append({
                "type": "excessive_attribute_lookup",
                "count": load_attr_count,
                "recommendation": "Consider caching frequently accessed attributes in local variables"
            })
            
        # Check for potentially inefficient list/dict comprehensions
        build_list_count = opcode_counts.get("BUILD_LIST", 0)
        if build_list_count > 10:
            optimizations.append({
                "type": "multiple_list_creation",
                "count": build_list_count,
                "recommendation": "Check for repeated list creation that could be optimized"
            })
            
        metrics["optimizations"] = optimizations
        
        return metrics
    
    def prepare_bytecode_tensors(self, bytecode_info: Dict) -> Dict:
        """Prepare bytecode information for neural processing"""
        result = {}
        
        # Extract opcodes and arguments
        if "disassembly" in bytecode_info:
            disassembly = bytecode_info["disassembly"]
            
            # Extract opcodes and args
            opcodes = [instr.get("opcode", 0) for instr in disassembly]
            args = [instr.get("arg", 0) if instr.get("arg") is not None else 0 for instr in disassembly]
            
            result["opcodes"] = opcodes
            result["args"] = args
            result["length"] = len(opcodes)
            
        return result

# ============================================================================
# Execution Trace Analysis
# ============================================================================

class ExecutionTraceAnalyzer:
    """
    Analyzes execution traces of Python code for dynamic behavior insights.
    Based on the execution tracing from Code-Dataset-Processor.
    """
    def __init__(self):
        pass
        
    def generate_trace_code(self, code: str) -> str:
        """Instrument code with tracing capabilities"""
        trace_header = """
import sys
import traceback
import json

_execution_trace = []

def _tracer(frame, event, arg):
    if event == 'line':
        _execution_trace.append({
            'event': event,
            'line': frame.f_lineno,
            'function': frame.f_code.co_name,
            'locals': {k: repr(v) for k, v in frame.f_locals.items() if not k.startswith('_')}
        })
    elif event == 'call':
        _execution_trace.append({
            'event': event,
            'line': frame.f_lineno,
            'function': frame.f_code.co_name,
            'locals': {k: repr(v) for k, v in frame.f_locals.items() if not k.startswith('_')}
        })
    elif event == 'return':
        _execution_trace.append({
            'event': event,
            'line': frame.f_lineno,
            'function': frame.f_code.co_name,
            'return_value': repr(arg),
            'locals': {k: repr(v) for k, v in frame.f_locals.items() if not k.startswith('_')}
        })
    return _tracer

# Original code starts below
"""

        trace_footer = """

# Execute traced code
if __name__ == "__main__":
    sys.settrace(_tracer)
    try:
        # Execute the main block
        pass
    except Exception as e:
        _execution_trace.append({
            'event': 'exception',
            'exception': repr(e),
            'traceback': traceback.format_exc()
        })
    finally:
        sys.settrace(None)
        print(json.dumps(_execution_trace))
"""

        # Combine the code with tracing
        return trace_header + code + trace_footer
        
    def execute_trace(self, code: str) -> Dict:
        """Execute code with tracing and return the trace results"""
        try:
            # Create instrumented code
            instrumented_code = self.generate_trace_code(code)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                tmp_filename = tmp.name
                tmp.write(instrumented_code.encode("utf-8"))
            
            # Execute the instrumented code
            import subprocess
            result = subprocess.run(
                [sys.executable, tmp_filename], 
                capture_output=True, 
                text=True,
                timeout=10  # Add timeout to avoid hanging
            )
            
            # Clean up temporary file
            os.unlink(tmp_filename)
            
            # Parse trace output
            trace = []
            if result.stdout:
                try:
                    trace = json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    logging.warning(f"Failed to parse execution trace: {result.stdout}")
                    
            return {
                "trace": trace,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "error": "Execution timed out",
                "trace": [],
                "stdout": "",
                "stderr": "Execution timed out after 10 seconds",
                "return_code": -1
            }
        except Exception as e:
            logging.error(f"Error generating execution trace: {e}")
            return {
                "error": str(e),
                "trace": [],
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }
    
    def analyze_trace(self, trace_info: Dict) -> Dict:
        """Analyze execution trace to extract metrics and insights"""
        metrics = {}
        
        if "error" in trace_info:
            metrics["error"] = trace_info["error"]
            return metrics
            
        trace = trace_info.get("trace", [])
        
        if not trace:
            metrics["error"] = "No trace data available"
            return metrics
            
        # Extract execution statistics
        functions_called = set()
        lines_executed = set()
        function_calls = 0
        function_returns = 0
        variable_values = {}
        
        for entry in trace:
            event = entry.get("event")
            
            if event == "call":
                function_calls += 1
                functions_called.add(entry.get("function", ""))
            elif event == "return":
                function_returns += 1
            elif event == "line":
                lines_executed.add(entry.get("line", 0))
                
            # Track variable values
            for var, val in entry.get("locals", {}).items():
                if var not in variable_values:
                    variable_values[var] = []
                variable_values[var].append(val)
        
        # Compute metrics
        metrics["function_call_count"] = function_calls
        metrics["unique_functions_called"] = len(functions_called)
        metrics["lines_executed"] = len(lines_executed)
        
        # Check for exceptions
        exceptions = [e for e in trace if e.get("event") == "exception"]
        metrics["exceptions"] = len(exceptions)
        if exceptions:
            metrics["exception_details"] = [{
                "type": e.get("exception", "Unknown"),
                "traceback": e.get("traceback", "").split("\n")[-2:]
            } for e in exceptions]
            
        # Hot paths analysis
        line_frequencies = {}
        for entry in trace:
            if entry.get("event") == "line":
                line = entry.get("line", 0)
                line_frequencies[line] = line_frequencies.get(line, 0) + 1
                
        # Find most frequently executed lines
        hot_lines = sorted(line_frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
        metrics["hot_lines"] = hot_lines
        
        # Variable analysis
        variable_changes = {}
        for var, values in variable_values.items():
            if len(values) > 1:
                variable_changes[var] = len(set(values))
                
        metrics["variable_changes"] = variable_changes
        
        return metrics
    
    def prepare_trace_tensors(self, trace_info: Dict) -> Dict:
        """Prepare execution trace for neural processing"""
        result = {}
        
        # Extract trace events
        if "trace" in trace_info:
            trace = trace_info["trace"]
            
            # Map event types
            event_map = {'line': 0, 'call': 1, 'return': 2, 'exception': 3}
            
            # Extract event data
            events = [event_map.get(e.get("event", ""), 0) for e in trace]
            functions = [hash(e.get("function", "")) % 1000 for e in trace]
            lines = [e.get("line", 0) % 1000 for e in trace]
            var_counts = [min(len(e.get("locals", {})), 99) for e in trace]
            
            result["events"] = events
            result["functions"] = functions
            result["lines"] = lines  
            result["var_counts"] = var_counts
            result["length"] = len(events)
            
        return result

# ============================================================================
# Version History Analysis
# ============================================================================

class VersionHistoryTracker:
    """
    Tracks and processes version history of code for temporal learning.
    Based on version history generation from Code-Dataset-Processor.
    """
    def __init__(self):
        pass
        
    def process_version_history(self, history: List[Dict]) -> Dict:
        """Process version history data to extract evolutionary patterns"""
        if not history:
            return {"error": "No version history provided"}
            
        metrics = {}
        
        # Count versions
        metrics["version_count"] = len(history)
        
        # Extract authors
        authors = set(version["author"] for version in history if "author" in version)
        metrics["author_count"] = len(authors)
        metrics["authors"] = list(authors)
        
        # Track changes over time
        changes_over_time = []
        for version in history:
            if "changes" in version:
                changes_over_time.append({
                    "version": version.get("version", 0),
                    "timestamp": version.get("timestamp", ""),
                    "additions": version["changes"].get("additions", 0),
                    "deletions": version["changes"].get("deletions", 0),
                    "files_changed": version["changes"].get("files_changed", 0)
                })
        
        metrics["changes_over_time"] = changes_over_time
        
        # Analyze message patterns
        message_types = {
            "feature": 0,
            "bugfix": 0,
            "refactor": 0,
            "other": 0
        }
        
        for version in history:
            message = version.get("message", "").lower()
            if "add" in message or "feature" in message or "new" in message:
                message_types["feature"] += 1
            elif "fix" in message or "bug" in message or "issue" in message:
                message_types["bugfix"] += 1
            elif "refactor" in message or "clean" in message or "improve" in message:
                message_types["refactor"] += 1
            else:
                message_types["other"] += 1
                
        metrics["message_types"] = message_types
        
        return metrics
        
    def generate_evolutionary_features(self, version_history: List[Dict]) -> Dict:
        """Extract features for learning from code evolution patterns"""
        features = {}
        
        if not version_history:
            return features
            
        # Get latest version code
        latest_code = version_history[-1].get("code", "")
        
        # Calculate change rate
        if len(version_history) > 1:
            first_timestamp = version_history[0].get("timestamp", "")
            last_timestamp = version_history[-1].get("timestamp", "")
            if first_timestamp and last_timestamp:
                try:
                    # Parse timestamps - assuming ISO format
                    from datetime import datetime
                    t1 = datetime.fromisoformat(first_timestamp.replace('Z', '+00:00'))
                    t2 = datetime.fromisoformat(last_timestamp.replace('Z', '+00:00'))
                    
                    # Calculate time difference in days
                    time_diff = (t2 - t1).total_seconds() / (24 * 3600)
                    
                    # Change rate = number of versions per day
                    if time_diff > 0:
                        features["change_rate"] = len(version_history) / time_diff
                    else:
                        features["change_rate"] = 0
                except:
                    features["change_rate"] = 0
        
        # Analyze code growth
        if len(version_history) > 1:
            first_code = version_history[0].get("code", "")
            features["code_growth"] = len(latest_code) - len(first_code)
            features["code_growth_percent"] = (len(latest_code) / max(1, len(first_code))) * 100 - 100
        
        # Calculate bug frequency
        bug_fixes = sum(1 for v in version_history if "fix" in v.get("message", "").lower())
        features["bug_fix_count"] = bug_fixes
        features["bug_fix_ratio"] = bug_fixes / len(version_history) if version_history else 0
        
        return features
    
    def prepare_version_tensors(self, version_history: List[Dict]) -> Dict:
        """Prepare version history for neural processing"""
        result = {}
        
        if not version_history:
            return result
            
        # Extract version numbers
        versions = [v.get("version", i) % 100 for i, v in enumerate(version_history)]
        
        # Extract change metrics (additions, deletions, files_changed)
        changes = []
        for v in version_history:
            if "changes" in v:
                changes.append([
                    v["changes"].get("additions", 0),
                    v["changes"].get("deletions", 0),
                    v["changes"].get("files_changed", 0)
                ])
            else:
                changes.append([0, 0, 0])
                
        result["versions"] = versions
        result["changes"] = changes  
        result["length"] = len(versions)
        
        return result

# ============================================================================
# Natural Language Description Processing
# ============================================================================

# ============================================================================
# Complete CodeCellAI System
# ============================================================================

class CodeCellularSystem:
    """
    Complete system implementing the CodeCellAI framework
    for software code processing and generation with all features from Code-Dataset-Processor
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
        
        # Initialize tokenizer
        self.tokenizer = CodeTokenizer(vocab_size=self.params.vocab_size)
        
        # Initialize device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize code encoder and decoder with all enhanced components
        self.encoder = EnhancedCodeEncoder(
            vocab_size=self.params.vocab_size,
            embedding_size=self.params.embedding_size,
            state_size=self.params.state_size,
            graph_embedding_size=self.params.embedding_size,
            max_ast_nodes=self.params.max_ast_nodes,
            max_graph_nodes=self.params.max_graph_nodes,
            max_bytecode_instructions=self.params.max_bytecode_instr,
            max_trace_events=self.params.max_trace_events,
            max_versions=self.params.max_versions,
            use_checkpoint=True
        ).to(self.device)
        
        self.decoder = CodeDecoder(
            state_size=self.params.state_size,
            embedding_size=self.params.embedding_size,
            vocab_size=self.params.vocab_size,
            use_checkpoint=True
        ).to(self.device)
        
        # Initialize cellular partitions with Ray
        self.partitions = [
            CodeCellPartition.remote(i, self.params) 
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
        
        # Initialize advanced processors
        self.graph_processor = AdvancedGraphProcessor(max_nodes=self.params.max_ast_nodes)
        self.bytecode_analyzer = BytecodeAnalyzer()
        self.trace_analyzer = ExecutionTraceAnalyzer()
        self.version_tracker = VersionHistoryTracker()
        self.code_quality = CodeQualityAnalyzer()
        self.nl_processor = NLDescriptionProcessor()
        
        # Pattern and vulnerability names for output mapping
        self.pattern_names = [
            "linear_search", "binary_search", "bubble_sort", 
            "factorial", "recursion", "dynamic_programming",
            "graph_traversal", "tree_traversal", "divide_conquer",
            "backtracking"
        ]
        
        self.security_vuln_names = [
            "sql_injection", "command_injection", "path_traversal", 
            "hardcoded_credentials", "insecure_random", "buffer_overflow",
            "integer_overflow", "race_condition"
        ]

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
                if available_memory < 4 * 1024 * 1024 * 1024:  # Less than 4GB available
                    obj_store_percent = 0.15  # Conservative for low memory
                    ray_internal_percent = 0.05
                elif available_memory < 8 * 1024 * 1024 * 1024:  # Less than 8GB available
                    obj_store_percent = 0.25  # Moderate for medium memory
                    ray_internal_percent = 0.05
                else:
                    obj_store_percent = 0.30  # Higher when plenty of memory
                    ray_internal_percent = 0.05
                
                # Calculate memory allocations
                obj_store_memory = int(available_memory * obj_store_percent)
                ray_memory = int(available_memory * ray_internal_percent)
                
                # Ensure minimum memory allocations
                MIN_OBJECT_STORE = 100 * 1024 * 1024  # 100MB minimum
                MIN_RAY_MEMORY = 50 * 1024 * 1024     # 50MB minimum
                
                obj_store_memory = max(obj_store_memory, MIN_OBJECT_STORE)
                ray_memory = max(ray_memory, MIN_RAY_MEMORY)
                
                # Cap memory usage
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
                    log_to_driver=False,
                    logging_level=logging.ERROR,
                    runtime_env=runtime_env,
                    log_level="ERROR"
                )
                logging.info("Ray initialized with fallback configuration")

    def preprocess_code_for_analysis(self, code: str) -> Dict[str, Any]:
        """
        Complete code preprocessing with ALL representations from Code-Dataset-Processor
        
        Args:
            code: Python code string
            
        Returns:
            Dictionary with all code representations
        """
        result = {
            'code': code,
        }
        
        try:
            # Parse AST
            tree = ast.parse(code)
            
            # Extract AST dictionary
            result['ast'] = self.graph_processor.extract_ast_dict(code)
            
            # Generate all graph representations
            result['cfg'] = self.graph_processor.serialize_graph(
                self.graph_processor.generate_cfg(code)
            )
            
            result['dfg'] = self.graph_processor.serialize_graph(
                self.graph_processor.generate_dfg(code)
            )
            
            result['pdg'] = self.graph_processor.serialize_graph(
                self.graph_processor.generate_pdg(code)
            )
            
            result['dependency_graph'] = self.graph_processor.serialize_graph(
                self.graph_processor.generate_dependency_graph(code)
            )
            
            # Generate bytecode representation
            result['bytecode'] = self.bytecode_analyzer.generate_bytecode(code)
            result['bytecode_metrics'] = self.bytecode_analyzer.analyze_bytecode_metrics(result['bytecode'])
            result['bytecode_tensors'] = self.bytecode_analyzer.prepare_bytecode_tensors(result['bytecode'])
            
            # Generate execution trace (optional - can be slow)
            # Using a very simple execution with timeout to avoid hanging
            result['execution_trace'] = self.trace_analyzer.execute_trace(code)
            result['trace_metrics'] = self.trace_analyzer.analyze_trace(result['execution_trace'])
            result['trace_tensors'] = self.trace_analyzer.prepare_trace_tensors(result['execution_trace'])
            
            # Generate code quality metrics
            result['metrics'] = self.code_quality.analyze_code_complexity(code, tree)
            result['algorithms'] = self.code_quality.identify_algorithms(code)
            result['patterns'] = self.code_quality.identify_design_patterns(code)
            result['security_vulnerabilities'] = self.code_quality.identify_security_vulnerabilities(code)
            result['performance'] = self.code_quality.estimate_performance(code, tree)
            
            # Generate natural language description
            result['natural_language_description'] = self.nl_processor.generate_nl_description(result['metrics'])
            result['nl_tensors'] = self.nl_processor.prepare_nl_tensors(result['natural_language_description'])
            
        except Exception as e:
            logging.error(f"Error preprocessing code: {e}")
            import traceback
            traceback.print_exc()
        
        return result

    def prepare_tensor_batch(self, preprocessed: Dict[str, Any]) -> Dict[str, torch.Tensor]:
        """Prepare tensor batch from preprocessed code data for the encoder"""
        batch = {}
        
        # Tokenize code
        if 'code' in preprocessed:
            code = preprocessed['code']
            encodings = self.tokenizer.encode(
                code, 
                max_length=self.params.max_seq_length,
                padding=True
            )
            
            # Add tokenized data to batch
            batch['input_ids'] = encodings['input_ids'].to(self.device).unsqueeze(0)
            batch['attention_mask'] = encodings['attention_mask'].to(self.device).unsqueeze(0)
            
        # Add graph data
        graph_types = ['ast', 'cfg', 'dfg', 'pdg', 'dependency_graph']
        for graph_type in graph_types:
            if graph_type in preprocessed:
                # Convert to tensor format
                graph_data = preprocessed[graph_type]
                if graph_data and isinstance(graph_data, dict):
                    # Extract node types and map to indices
                    node_types = graph_data.get('node_types', [])
                    if not node_types:
                        continue
                        
                    # Convert to tensor
                    node_type_tensor = torch.tensor(
                        [hash(t) % 200 for t in node_types], 
                        dtype=torch.long,
                        device=self.device
                    ).unsqueeze(0)  # Add batch dimension
                    
                    # Create adjacency matrix
                    adjacency = torch.tensor(
                        graph_data.get('adjacency', []),
                        dtype=torch.float32,
                        device=self.device
                    ).unsqueeze(0)  # Add batch dimension
                    
                    # Create mask
                    mask = torch.ones(
                        1, len(node_types), 
                        dtype=torch.float32, 
                        device=self.device
                    )
                    
                    # Add to batch
                    type_key = graph_type.split('_')[0] + '_graph'  # Convert to format expected by encoder
                    batch[type_key] = {
                        'node_types': node_type_tensor,
                        'adjacency': adjacency,
                        'node_mask': mask
                    }
                    
        # Add bytecode data
        if 'bytecode_tensors' in preprocessed:
            bytecode_data = preprocessed['bytecode_tensors']
            if bytecode_data:
                # Convert to tensor format
                opcodes = torch.tensor(
                    bytecode_data.get('opcodes', []), 
                    dtype=torch.long,
                    device=self.device
                ).unsqueeze(0)  # Add batch dimension
                
                args = torch.tensor(
                    bytecode_data.get('args', []), 
                    dtype=torch.long,
                    device=self.device
                ).unsqueeze(0)  # Add batch dimension
                
                # Create mask
                mask = torch.ones(
                    1, bytecode_data.get('length', 0), 
                    dtype=torch.float32, 
                    device=self.device
                )
                
                # Add to batch
                batch['bytecode_data'] = {
                    'opcodes': opcodes,
                    'args': args,
                    'mask': mask
                }
                
        # Add trace data
        if 'trace_tensors' in preprocessed:
            trace_data = preprocessed['trace_tensors']
            if trace_data:
                # Convert to tensor format
                events = torch.tensor(
                    trace_data.get('events', []), 
                    dtype=torch.long,
                    device=self.device
                ).unsqueeze(0)  # Add batch dimension
                
                functions = torch.tensor(
                    trace_data.get('functions', []), 
                    dtype=torch.long,
                    device=self.device
                ).unsqueeze(0)  # Add batch dimension
                
                lines = torch.tensor(
                    trace_data.get('lines', []), 
                    dtype=torch.long,
                    device=self.device
                ).unsqueeze(0)  # Add batch dimension
                
                var_counts = torch.tensor(
                    trace_data.get('var_counts', []), 
                    dtype=torch.long,
                    device=self.device
                ).unsqueeze(0)  # Add batch dimension
                
                # Create mask
                mask = torch.ones(
                    1, trace_data.get('length', 0), 
                    dtype=torch.float32, 
                    device=self.device
                )
                
                # Add to batch
                batch['trace_data'] = {
                    'event_types': events,
                    'functions': functions,
                    'lines': lines,
                    'var_counts': var_counts,
                    'mask': mask
                }
                
        # Add NL description data
        if 'nl_tensors' in preprocessed:
            nl_data = preprocessed['nl_tensors']
            if nl_data:
                # Convert to tensor format
                word_ids = torch.tensor(
                    nl_data.get('word_ids', []), 
                    dtype=torch.long,
                    device=self.device
                ).unsqueeze(0)  # Add batch dimension
                
                # Create mask
                mask = torch.ones(
                    1, nl_data.get('length', 0), 
                    dtype=torch.float32, 
                    device=self.device
                )
                
                # Add to batch
                batch['nl_data'] = {
                    'word_ids': word_ids,
                    'mask': mask
                }
                
        return batch
        
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Comprehensive code analysis using ALL features from Code-Dataset-Processor
        """
        start_time = time.time()
        
        try:
            # Update system time
            self.current_time += 0.1
            
            # Full preprocessing with all representations
            logging.info("Preprocessing code with ALL representations...")
            preprocessed = self.preprocess_code_for_analysis(code)
            
            # Prepare tensor batch for encoder
            logging.info("Preparing tensor batch...")
            batch = self.prepare_tensor_batch(preprocessed)
            
            # Process through encoder
            logging.info("Encoding code with enhanced encoder...")
            with torch.no_grad():
                state_vector = self.encoder(batch)
            
            # Split state vector for partitions
            partition_inputs = []
            for i in range(self.params.num_partitions):
                start_idx = i * self.partition_state_size
                end_idx = start_idx + self.partition_state_size
                chunk = state_vector[:, start_idx:end_idx]
                partition_inputs.append(chunk.cpu().numpy().squeeze(0))
            
            # Get all current states
            logging.info("Getting current partition states...")
            state_refs = [partition.get_state.remote() for partition in self.partitions]
            states_list = ray.get(state_refs)
            
            # Extract states
            states = {i: state_info['state'] for i, state_info in enumerate(states_list)}
            
            # Update all partitions in parallel
            logging.info("Updating partitions with cellular model...")
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
            
            # Extract pattern detection results
            pattern_scores = np.zeros(len(self.pattern_names))
            for result in update_results:
                if 'patterns' in result and len(result['patterns']) > 0:
                    pattern_chunk = result['patterns']
                    chunk_size = min(len(pattern_scores), len(pattern_chunk))
                    pattern_scores[:chunk_size] += pattern_chunk[:chunk_size]
            
            # Normalize pattern scores
            pattern_scores = pattern_scores / self.params.num_partitions
            pattern_results = {
                self.pattern_names[i]: float(score) 
                for i, score in enumerate(pattern_scores) 
                if i < len(self.pattern_names)
            }
            
            # Extract security analysis results
            security_scores = np.zeros(len(self.security_vuln_names))
            for result in update_results:
                if 'security' in result and len(result['security']) > 0:
                    security_chunk = result['security']
                    chunk_size = min(len(security_scores), len(security_chunk))
                    security_scores[:chunk_size] += security_chunk[:chunk_size]
            
            # Normalize security scores
            security_scores = security_scores / self.params.num_partitions
            security_results = {
                self.security_vuln_names[i]: float(score) 
                for i, score in enumerate(security_scores) 
                if i < len(self.security_vuln_names)
            }
            
            # Check for emergent properties
            emergence_values = [float(result.get('emergence', 0)) for result in update_results]
            system_emergence = np.mean(emergence_values) > 0.5
            
            # Add preprocessed detected patterns
            enhanced_patterns = pattern_results.copy()
            for algo in preprocessed.get("algorithms", []):
                algo_name = algo.get("name", "")
                if algo_name in enhanced_patterns:
                    enhanced_patterns[algo_name] = 1.0
                    
            # Add preprocessed detected vulnerabilities
            enhanced_vulns = security_results.copy()
            for vuln in preprocessed.get("security_vulnerabilities", []):
                vuln_type = vuln.get("type", "")
                if vuln_type in enhanced_vulns:
                    enhanced_vulns[vuln_type] = 1.0
            
            # Combine all analysis results
            analysis_results = {
                'code': code,
                'metrics': preprocessed.get('metrics', {}),
                'bytecode_metrics': preprocessed.get('bytecode_metrics', {}),
                'trace_metrics': preprocessed.get('trace_metrics', {}),
                'performance': preprocessed.get('performance', {}),
                'patterns': enhanced_patterns,
                'vulnerabilities': enhanced_vulns,
                'emergent_properties': system_emergence,
                'natural_language_description': preprocessed.get('natural_language_description', ''),
                'processing_time': time.time() - start_time
            }
            
            return analysis_results
            
        except Exception as e:
            logging.error(f"Error analyzing code: {e}")
            import traceback
            traceback.print_exc()
            return {
                'code': code,
                'error': str(e),
                'processing_time': time.time() - start_time
            }

    def generate_code(self, prompt: str, max_length: int = 200, temperature: float = 0.7) -> str:
        """Generate code based on a text prompt"""
        start_time = time.time()
        
        try:
            # Update system time
            self.current_time += 0.1
            
            # Tokenize prompt
            tokenized = self.tokenizer.encode(
                prompt,
                max_length=self.params.max_seq_length // 2,  # Use half the max length for prompt
                padding=True
            )
            
            # Convert to tensors
            input_ids = tokenized['input_ids'].to(self.device).unsqueeze(0)  # Add batch dimension
            
            # Prepare simplified batch for encoder
            batch = {
                'input_ids': input_ids,
                'attention_mask': torch.ones_like(input_ids)  # All tokens are valid
            }
            
            # Encode prompt to state vector
            with torch.no_grad():
                state_vector = self.encoder(batch)
            
            # Split state vector into chunks for each partition
            partition_inputs = []
            for i in range(self.params.num_partitions):
                start_idx = i * self.partition_state_size
                end_idx = start_idx + self.partition_state_size
                chunk = state_vector[:, start_idx:end_idx]
                partition_inputs.append(chunk.cpu().numpy().squeeze(0))
            
            # Get current states
            state_refs = [partition.get_state.remote() for partition in self.partitions]
            states_list = ray.get(state_refs)
            
            # Extract states
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
            
            # Extract updated states and apply memory integration if available
            updated_states = []
            for result in update_results:
                if 'memory_state' in result and result['memory_state'].size > 0:
                    updated_states.append(result['memory_state'])
                else:
                    updated_states.append(result['state'])
            
            # CRITICAL FIX: Reshape to match full state_size, not just concatenation
            updated_states_flat = np.concatenate(updated_states)
            
            # Ensure the tensor has shape [batch_size, state_size]
            updated_states_tensor = torch.tensor(updated_states_flat, dtype=torch.float32)
            updated_states_tensor = updated_states_tensor.reshape(1, self.params.state_size).to(self.device)
            
            # Apply temperature to influence generation diversity
            if temperature != 1.0:
                # Scale the state vector by temperature
                updated_states_tensor = updated_states_tensor / max(0.1, temperature)
            
            # Generate code with decoder
            with torch.no_grad():
                output_logits = self.decoder(updated_states_tensor, max_length=max_length)
                
                # Either sample with temperature or take argmax
                if temperature > 0 and temperature != 1.0:
                    # Apply temperature scaling and sample
                    scaled_logits = output_logits / temperature
                    probs = torch.softmax(scaled_logits, dim=-1)
                    
                    # Multinomial sampling
                    output_ids = torch.zeros(probs.size(0), probs.size(1), dtype=torch.long, device=probs.device)
                    for i in range(probs.size(1)):
                        output_ids[:, i] = torch.multinomial(probs[:, i, :], 1).squeeze(-1)
                else:
                    # Just take argmax
                    output_ids = torch.argmax(output_logits, dim=-1)
            
            # Decode to code
            code = self.tokenizer.decode(output_ids[0].cpu().tolist())
            
            # Process generation time
            generation_time = time.time() - start_time
            
            return code
            
        except Exception as e:
            logging.error(f"Error generating code: {e}")
            import traceback
            traceback.print_exc()
            return f"# Error generating code: {str(e)}"

    def train_on_dataset(self, data_path: str, num_epochs: int = 3, 
                         save_path: str = './codecellai_model_checkpoints', max_samples: int = 100000):
        """Train the model on code dataset with high optimization"""
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
        dataset = MemoryMappedCodeDataset(
            data_path, 
            self.tokenizer, 
            self.params.max_seq_length,
            include_graphs=True
        )
        
        # Memory-aware adaptive batch sizes
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
                
                # Prepare batch for encoder
                encoder_batch = {
                    'input_ids': input_ids,
                    'attention_mask': attention_mask
                }
                
                # Forward pass
                state_vector = self.encoder(encoder_batch)
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
                
                # Recalculate partition state size
                self.partition_state_size = self.params.state_size // self.params.num_partitions
                logging.info(f"Updated to {self.params.num_partitions} partitions with state size {self.partition_state_size} each")
            
            # CRITICAL FIX: Reinitialize model components with updated parameters
            # Recreate encoder and decoder with the updated parameters
            self.encoder = EnhancedCodeEncoder(
                vocab_size=self.params.vocab_size,
                embedding_size=self.params.embedding_size,
                state_size=self.params.state_size,
                graph_embedding_size=self.params.embedding_size,
                max_ast_nodes=self.params.max_ast_nodes,
                max_graph_nodes=self.params.max_graph_nodes,
                max_bytecode_instructions=self.params.max_bytecode_instr,
                max_trace_events=self.params.max_trace_events,
                max_versions=self.params.max_versions,
                use_checkpoint=True
            ).to(self.device)
            
            self.decoder = CodeDecoder(
                state_size=self.params.state_size,
                embedding_size=self.params.embedding_size,
                vocab_size=self.params.vocab_size,
                use_checkpoint=True
            ).to(self.device)
            
            # Recreate partitions with Ray
            self.partitions = [
                CodeCellPartition.remote(i, self.params) 
                for i in range(self.params.num_partitions)
            ]
            
            # Load encoder and decoder states
            self.encoder.load_state_dict(checkpoint['encoder'])
            self.decoder.load_state_dict(checkpoint['decoder'])
            
            # Get sparse parameters from encoder and decoder
            sparse_params = []
            sparse_params.extend(self.encoder.get_sparse_params())
            sparse_params.extend(self.decoder.get_sparse_params())
            
            # Get dense parameters from encoder and decoder
            dense_params = []
            dense_params.extend(self.encoder.get_dense_params())
            dense_params.extend(self.decoder.get_dense_params())
            
            # Recreate optimizers with the updated parameters
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
                if test_data_path.endswith('.gz'):
                    opener = gzip.open
                    mode = 'rt'
                else:
                    opener = open
                    mode = 'r'
                    
                with opener(test_data_path, mode, encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i >= num_samples:
                            break
                        try:
                            item = json.loads(line)
                            if 'code' in item:
                                samples.append(item['code'])
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
            analysis_times = []
            generation_times = []
            tokens_processed = 0
            
            # Process each sample
            for i, code in enumerate(samples):
                # 1. Analyze code
                start_time = time.time()
                analysis = self.analyze_code(code)
                analysis_time = time.time() - start_time
                analysis_times.append(analysis_time)
                
                # 2. Generate code from first line as prompt
                lines = code.strip().split('\n')
                prompt = lines[0] if lines else "def function"
                
                start_time = time.time()
                generated_code = self.generate_code(prompt, max_length=100)
                generation_time = time.time() - start_time
                generation_times.append(generation_time)
                
                # Track tokens
                input_tokens = self.tokenizer.tokenize(code)
                tokens_processed += len(input_tokens)
                
                # Total processing time
                processing_times.append(analysis_time + generation_time)
                
                if i % 10 == 0:
                    logging.info(f"Processed {i+1}/{len(samples)} samples")
            
            # Calculate statistics
            avg_processing_time = sum(processing_times) / len(processing_times)
            avg_analysis_time = sum(analysis_times) / len(analysis_times)
            avg_generation_time = sum(generation_times) / len(generation_times)
            tokens_per_second = tokens_processed / sum(processing_times)
            
            # Print benchmark results
            logging.info("=" * 50)
            logging.info("Benchmark Results:")
            logging.info(f"Average processing time: {avg_processing_time:.4f} seconds per sample")
            logging.info(f"Average analysis time: {avg_analysis_time:.4f} seconds per sample")
            logging.info(f"Average generation time: {avg_generation_time:.4f} seconds per sample")
            logging.info(f"Tokens per second: {tokens_per_second:.2f}")
            logging.info("=" * 50)
            
            # Return results as dictionary
            return {
                'avg_processing_time': avg_processing_time,
                'avg_analysis_time': avg_analysis_time,
                'avg_generation_time': avg_generation_time,
                'tokens_per_second': tokens_per_second
            }
        except Exception as e:
            logging.error(f"Error during benchmarking: {str(e)}")
            import traceback
            traceback.print_exc()
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


class NLDescriptionProcessor:
    """
    Processes natural language descriptions of code for semantic understanding.
    Based on natural language description generation from Code-Dataset-Processor.
    """
    def __init__(self):
        # Keywords for code structure
        self.structure_keywords = {
            "contains", "defines", "implements", "includes", "uses",
            "imports", "initializes", "sets", "calculates", "computes",
            "returns", "checks", "validates", "processes", "handles"
        }
        
        # Keywords for algorithms
        self.algorithm_keywords = {
            "algorithm", "search", "sort", "recursion", "iteration",
            "linear", "binary", "tree", "graph", "path", "traversal",
            "dynamic programming", "backtracking", "greedy", "divide and conquer"
        }
        
        # Keywords for design patterns
        self.pattern_keywords = {
            "pattern", "singleton", "factory", "observer", "decorator",
            "adapter", "proxy", "strategy", "template", "composite",
            "command", "iterator", "visitor", "state", "builder"
        }
        
        # Keywords for complexity
        self.complexity_keywords = {
            "complexity", "simple", "moderate", "complex", "very complex",
            "O(1)", "O(n)", "O(n²)", "O(n log n)", "O(log n)", "exponential",
            "polynomial", "constant", "linear", "quadratic", "logarithmic"
        }
        
    def parse_nl_description(self, description: str) -> Dict:
        """Parse a natural language description into structured information"""
        result = {
            "structure": [],
            "algorithms": [],
            "patterns": [],
            "complexity": None,
            "security": []
        }
        
        if not description:
            return result
            
        # Normalize description
        description = description.lower()
        sentences = [s.strip() for s in description.split('.') if s.strip()]
        
        # Extract structure information
        for sentence in sentences:
            words = set(sentence.split())
            if any(keyword in words for keyword in self.structure_keywords):
                result["structure"].append(sentence)
                
        # Extract algorithms
        for algo_kw in self.algorithm_keywords:
            if algo_kw in description:
                result["algorithms"].append(algo_kw)
                
        # Extract design patterns
        for pattern_kw in self.pattern_keywords:
            if pattern_kw in description:
                result["patterns"].append(pattern_kw)
                
        # Extract complexity
        for complexity_kw in self.complexity_keywords:
            if complexity_kw in description:
                result["complexity"] = complexity_kw
                break
                
        # Extract security issues
        security_issues = ["vulnerability", "security", "injection", "overflow", 
                         "credentials", "insecure", "unsafe"]
        for issue in security_issues:
            if issue in description:
                result["security"].append(issue)
                
        return result
        
    def generate_nl_description(self, code_metrics: Dict) -> str:
        """Generate a natural language description from code metrics"""
        description = "This Python code "
        
        # Add information about imports
        if "imports" in code_metrics:
            imports = code_metrics["imports"]
            if imports:
                description += f"imports {len(imports)} module(s) including " + ", ".join(
                    imports[:3]
                )
                if len(imports) > 3:
                    description += f" and {len(imports) - 3} more"
                description += ". "
                
        # Add information about classes
        if "class_count" in code_metrics:
            class_count = code_metrics["class_count"]
            if class_count > 0:
                description += f"It defines {class_count} class(es). "
                
        # Add information about functions
        if "function_count" in code_metrics:
            function_count = code_metrics["function_count"]
            if function_count > 0:
                description += f"It contains {function_count} function(s). "
                
        # Add complexity information
        if "complexity_level" in code_metrics:
            description += f"The code has {code_metrics['complexity_level']} complexity. "
            
        # Add algorithm information
        if "algorithms" in code_metrics and code_metrics["algorithms"]:
            algo_names = [algo["name"].replace("_", " ") for algo in code_metrics["algorithms"]]
            description += "It appears to implement " + ", ".join(algo_names) + ". "
            
        # Add design pattern information
        if "design_patterns" in code_metrics and code_metrics["design_patterns"]:
            pattern_names = [pattern["name"] for pattern in code_metrics["design_patterns"]]
            description += "The code uses the " + ", ".join(pattern_names) + " design pattern(s). "
            
        # Add performance information
        if "time_complexity" in code_metrics:
            complexity = code_metrics.get("time_complexity", "unknown")
            description += f"The estimated time complexity is {complexity}. "
            
        # Add security information
        if "security_vulnerabilities" in code_metrics and code_metrics["security_vulnerabilities"]:
            vulns = code_metrics["security_vulnerabilities"]
            description += f"Warning: The code contains {len(vulns)} potential security issue(s) including "
            vuln_names = [vuln["type"].replace("_", " ") for vuln in vulns]
            description += ", ".join(vuln_names) + ". "
            
        return description.strip()
    
    def prepare_nl_tensors(self, description: str) -> Dict:
        """Prepare natural language description for neural processing"""
        result = {}
        
        if not description:
            return result
            
        # Simple word tokenization
        words = description.lower().split()
        
        # Create vocabulary - map words to indices
        vocab = {"<pad>": 0, "<unk>": 1}
        for word in set(words):
            if word not in vocab:
                vocab[word] = len(vocab)
                
        # Convert words to indices
        word_ids = [vocab.get(word, vocab["<unk>"]) for word in words]
        
        result["word_ids"] = word_ids
        result["vocab"] = vocab
        result["length"] = len(word_ids)
        
        return result

# ============================================================================
# Code Quality and Pattern Analysis
# ============================================================================

class CodeQualityAnalyzer:
    """
    Analyzes code quality, metrics, and patterns.
    Based on code quality analysis from Code-Dataset-Processor.
    """
    def __init__(self):
        # Algorithm patterns to detect
        self.algorithm_patterns = {
            "linear_search": {
                "pattern": r"for\s+\w+\s+in\s+.+:\s*\n\s+if\s+.+\s*==\s*.+:",
                "complexity": "O(n)",
            },
            "binary_search": {
                "pattern": r"while\s+\w+\s*<=\s*\w+\s*:\s*\n\s+\w+\s*=\s*\(\s*\w+\s*\+\s*\w+\s*\)\s*\/\/\s*2",
                "complexity": "O(log n)",
            },
            "bubble_sort": {
                "pattern": r"for\s+\w+\s+in\s+range\(.+\):\s*\n\s+for\s+\w+\s+in\s+range\(.+\):\s*\n\s+if\s+.+\[\w+\]\s*>\s*.+\[\w+\+1\]",
                "complexity": "O(n²)",
            },
            "factorial": {
                "pattern": r"if\s+\w+\s*<=\s*1:\s*\n\s+return\s+1\s*\n\s+return\s+\w+\s*\*\s*\w+\(\s*\w+\s*-\s*1\s*\)",
                "complexity": "O(n)",
            },
            "recursion": {
                "pattern": r"def\s+(\w+).*\n.*\n.*\1\s*\(",
                "complexity": "varies",
            },
            "dynamic_programming": {
                "pattern": r"(memo|dp|cache|table)\s*=\s*\{\}|\[\]",
                "complexity": "varies",
            },
            "graph_traversal": {
                "pattern": r"(visited|seen)\s*=\s*set\(\)",
                "complexity": "O(V+E)",
            },
            "tree_traversal": {
                "pattern": r"def\s+(in|pre|post)order",
                "complexity": "O(n)",
            },
        }
        
        # Design patterns to detect
        self.design_patterns = {
            "singleton": {
                "pattern": r"class\s+\w+\s*:.+\n\s+_instance\s*=\s*None.+\n.+\s+@classmethod\s*\n\s+def\s+get_instance",
            },
            "factory": {
                "pattern": r"class\s+\w+\s*:.+\n.+\s+def\s+create_\w+\(.+\):\s*\n\s+if\s+.+:\s*\n\s+return\s+\w+\(\)",
            },
            "observer": {
                "pattern": r"def\s+add_observer\(.+\):.+\n.+\s+def\s+notify_observers",
            },
            "decorator": {
                "pattern": r"class\s+\w+\(.+\):.+\n.+\s+def\s+__init__\(self,\s*\w+\):",
            },
        }
        
        # Security vulnerability patterns
        self.security_vulnerabilities = {
            "sql_injection": {
                "pattern": r'execute\(\s*[\'"].+\s*\+\s*.+\s*[\'"]',
                "severity": "high",
            },
            "command_injection": {
                "pattern": r"os\.system\(\s*.+\s*\+\s*.+\s*\)",
                "severity": "high",
            },
            "path_traversal": {
                "pattern": r"open\(\s*.+\s*\+\s*.+\s*\)",
                "severity": "medium",
            },
            "hardcoded_credentials": {
                "pattern": r'password\s*=\s*[\'"].+[\'"]',
                "severity": "medium",
            },
            "insecure_random": {
                "pattern": r"random\.\w+\(\)",
                "severity": "low"
            },
        }
        
    def analyze_code_complexity(self, code: str, ast_tree: Optional[ast.AST] = None) -> Dict:
        """Analyze code complexity using various metrics"""
        metrics = {}

        # Basic metrics
        metrics["loc"] = len(code.splitlines())
        metrics["sloc"] = len(
            [
                line
                for line in code.splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]
        )

        try:
            # Parse AST if not provided
            if ast_tree is None:
                ast_tree = ast.parse(code)
                
            if ast_tree:
                # Count functions and classes
                functions = [
                    node
                    for node in ast.walk(ast_tree)
                    if isinstance(node, ast.FunctionDef)
                ]
                metrics["function_count"] = len(functions)

                # Average function complexity (lines per function)
                if metrics["function_count"] > 0:
                    function_lines = []
                    for func in functions:
                        start_line = func.lineno
                        end_line = (
                            func.end_lineno
                            if hasattr(func, "end_lineno")
                            else start_line
                        )
                        for node in ast.walk(func):
                            if hasattr(node, "end_lineno"):
                                end_line = max(end_line, node.end_lineno)
                        function_lines.append(end_line - start_line + 1)

                    metrics["avg_function_length"] = sum(function_lines) / len(
                        function_lines
                    )
                else:
                    metrics["avg_function_length"] = 0

                # Count classes
                metrics["class_count"] = len(
                    [
                        node
                        for node in ast.walk(ast_tree)
                        if isinstance(node, ast.ClassDef)
                    ]
                )

                # Complexity metrics
                metrics["cyclomatic_complexity"] = (
                    len(
                        [
                            node
                            for node in ast.walk(ast_tree)
                            if isinstance(
                                node, (ast.If, ast.For, ast.While, ast.FunctionDef)
                            )
                        ]
                    )
                    + 1
                )

                # Cognitive complexity approximation (simplified)
                cognitive = 0
                nesting_level = 0

                for node in ast.walk(ast_tree):
                    if isinstance(node, (ast.If, ast.For, ast.While)):
                        cognitive += 1 + nesting_level  # Base + nesting bonus
                        nesting_level += 1
                    elif isinstance(node, ast.FunctionDef):
                        nesting_level = 0  # Reset nesting at function boundaries

                metrics["cognitive_complexity"] = cognitive
                
                # Add complexity level labels
                cc = metrics.get("cyclomatic_complexity", 0)
                if cc <= 5:
                    metrics["complexity_level"] = "simple"
                elif cc <= 10:
                    metrics["complexity_level"] = "moderate"
                elif cc <= 20:
                    metrics["complexity_level"] = "complex"
                else:
                    metrics["complexity_level"] = "very_complex"
        except Exception as e:
            logging.error(f"Error analyzing code complexity: {e}")

        return metrics
        
    def identify_algorithms(self, code: str) -> List[Dict]:
        """Identify algorithms in the code"""
        algorithms = []

        for algo_name, algo_info in self.algorithm_patterns.items():
            if re.search(algo_info["pattern"], code, re.MULTILINE):
                algorithms.append(
                    {"name": algo_name, "complexity": algo_info["complexity"]}
                )

        return algorithms
        
    def identify_design_patterns(self, code: str) -> List[Dict]:
        """Identify design patterns in the code"""
        patterns = []

        for pattern_name, pattern_info in self.design_patterns.items():
            if re.search(pattern_info["pattern"], code, re.MULTILINE):
                patterns.append({"name": pattern_name})

        return patterns
        
    def identify_security_vulnerabilities(self, code: str) -> List[Dict]:
        """Identify potential security vulnerabilities in the code"""
        vulnerabilities = []

        for vuln_name, vuln_info in self.security_vulnerabilities.items():
            if re.search(vuln_info["pattern"], code, re.MULTILINE):
                vulnerabilities.append(
                    {"type": vuln_name, "severity": vuln_info["severity"]}
                )

        return vulnerabilities
        
    def estimate_performance(self, code: str, ast_tree: Optional[ast.AST] = None) -> Dict:
        """Estimate performance characteristics of the code"""
        performance = {"estimation_method": "static_analysis"}

        # Try to identify time complexity from loops and recursion
        if ast_tree is None:
            try:
                ast_tree = ast.parse(code)
            except Exception as e:
                logging.error(f"Error parsing AST for performance estimation: {e}")
                return performance
                
        if ast_tree:
            # Count nested loops
            max_loop_depth = 0
            current_depth = 0

            class LoopVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.max_depth = 0
                    self.current_depth = 0

                def visit_For(self, node):
                    self.current_depth += 1
                    self.max_depth = max(self.max_depth, self.current_depth)
                    self.generic_visit(node)
                    self.current_depth -= 1

                def visit_While(self, node):
                    self.current_depth += 1
                    self.max_depth = max(self.max_depth, self.current_depth)
                    self.generic_visit(node)
                    self.current_depth -= 1

            loop_visitor = LoopVisitor()
            loop_visitor.visit(ast_tree)
            max_loop_depth = loop_visitor.max_depth

            # Check for recursion
            has_recursion = False
            function_names = set()

            for node in ast.walk(ast_tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.add(node.name)

            for node in ast.walk(ast_tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in function_names:
                        has_recursion = True
                        break

            # Estimate time complexity
            if has_recursion:
                if max_loop_depth > 0:
                    performance["time_complexity"] = (
                        "exponential"  # Recursion with loops
                    )
                else:
                    performance["time_complexity"] = (
                        "unknown_recursive"  # Simple recursion
                    )
            elif max_loop_depth == 0:
                performance["time_complexity"] = "O(1)"  # Constant time
            elif max_loop_depth == 1:
                performance["time_complexity"] = "O(n)"  # Linear time
            elif max_loop_depth == 2:
                performance["time_complexity"] = "O(n²)"  # Quadratic time
            elif max_loop_depth == 3:
                performance["time_complexity"] = "O(n³)"  # Cubic time
            else:
                performance["time_complexity"] = (
                    f"O(n^{max_loop_depth})"  # Polynomial time
                )

            # Estimate space complexity based on data structures
            has_growing_structures = False
            for node in ast.walk(ast_tree):
                if isinstance(node, (ast.List, ast.Dict, ast.Set)):
                    has_growing_structures = True
                    break

            if has_growing_structures:
                if max_loop_depth > 0:
                    performance["space_complexity"] = (
                        "O(n)"  # Growing structures inside loops
                    )
                else:
                    performance["space_complexity"] = "O(1)"  # Fixed size structures
            else:
                performance["space_complexity"] = "O(1)"  # Constant space

        return performance

# ============================================================================
# Neural Network Components
# ============================================================================

class EnhancedGraphEncoder(nn.Module):
    """Neural network module to encode graph-based code representations"""
    def __init__(self, node_embedding_size: int, state_size: int, max_nodes: int = 1000):
        super().__init__()
        self.node_embedding_size = node_embedding_size
        self.state_size = state_size
        self.max_nodes = max_nodes
        
        # Node type embedding - handles more node types than basic version
        self.node_type_embedding = nn.Embedding(200, node_embedding_size)
        
        # 3-layer GNN for better graph understanding
        self.gnn_layers = nn.ModuleList([
            nn.Linear(node_embedding_size, node_embedding_size),
            nn.Linear(node_embedding_size, node_embedding_size),
            nn.Linear(node_embedding_size, node_embedding_size)
        ])
        
        # Additional attention layer for graph nodes
        self.attention = nn.Linear(node_embedding_size, 1)
        
        # Final projection
        self.projection = nn.Linear(node_embedding_size, state_size)
        
        # Activations
        self.activation = nn.ReLU()
        
    def forward(self, graph_data: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Process graph data into embeddings"""
        batch_size = graph_data["node_types"].size(0)
        device = graph_data["node_types"].device
        
        # Initial node embeddings
        node_embeds = self.node_type_embedding(graph_data["node_types"])
        
        # Get adjacency matrix and node mask
        adj_matrix = graph_data["adjacency"]
        node_mask = graph_data["node_mask"].unsqueeze(-1)  # Add dimension for broadcasting
        
        # Apply GNN layers with residual connections
        hidden = node_embeds
        for layer in self.gnn_layers:
            # Message passing
            messages = torch.bmm(adj_matrix, hidden)
            
            # Update with residual connection
            hidden = self.activation(layer(messages)) + hidden
            
            # Apply mask
            hidden = hidden * node_mask
            
        # Apply attention for weighted node aggregation
        attn_scores = self.attention(hidden)
        attn_weights = torch.softmax(attn_scores + (1 - node_mask) * -10000.0, dim=1)
        
        # Weighted sum of node features
        graph_embedding = torch.sum(hidden * attn_weights, dim=1)
        
        # Project to state size
        state = self.projection(graph_embedding)
        
        return state


class BytecodeEncoder(nn.Module):
    """Neural network module to encode bytecode information"""
    def __init__(self, embedding_size: int, state_size: int, max_instructions: int = 500):
        super().__init__()
        self.embedding_size = embedding_size
        self.state_size = state_size
        self.max_instructions = max_instructions
        
        # Opcode embedding
        self.opcode_embedding = nn.Embedding(256, embedding_size // 2)
        
        # Arg embedding
        self.arg_embedding = nn.Embedding(1000, embedding_size // 2)
        
        # LSTM for sequential processing
        self.lstm = nn.LSTM(
            input_size=embedding_size,
            hidden_size=state_size // 2,
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )
        
        # Projection
        self.projection = nn.Linear(state_size, state_size)
        
    def forward(self, bytecode_data: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Process bytecode data into embeddings"""
        # Get opcode and arg tensors
        opcodes = bytecode_data["opcodes"]
        args = bytecode_data["args"]
        
        # Get mask for valid instructions
        mask = bytecode_data["mask"]
        
        # Embed opcodes and args
        opcode_embeds = self.opcode_embedding(opcodes)
        arg_embeds = self.arg_embedding(args)
        
        # Combine embeddings
        combined_embeds = torch.cat([opcode_embeds, arg_embeds], dim=-1)
        
        # Apply LSTM
        packed_embeds = nn.utils.rnn.pack_padded_sequence(
            combined_embeds, 
            lengths=mask.sum(dim=1).cpu(),
            batch_first=True,
            enforce_sorted=False
        )
        
        _, (hidden, _) = self.lstm(packed_embeds)
        
        # Combine directions
        hidden = hidden.transpose(0, 1).contiguous()
        hidden = hidden.view(hidden.size(0), -1)
        
        # Final projection
        state = self.projection(hidden)
        
        return state


class TraceEncoder(nn.Module):
    """Neural network module to encode execution trace information"""
    def __init__(self, embedding_size: int, state_size: int, max_trace_events: int = 300):
        super().__init__()
        self.embedding_size = embedding_size
        self.state_size = state_size
        self.max_trace_events = max_trace_events
        
        # Event type embedding
        self.event_embedding = nn.Embedding(10, embedding_size // 4)
        
        # Function name embedding
        self.function_embedding = nn.Embedding(1000, embedding_size // 4)
        
        # Line number embedding
        self.line_embedding = nn.Embedding(1000, embedding_size // 4)
        
        # Variable count embedding
        self.var_count_embedding = nn.Embedding(100, embedding_size // 4)
        
        # LSTM for sequential processing
        self.lstm = nn.LSTM(
            input_size=embedding_size,
            hidden_size=state_size // 2,
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )
        
        # Projection
        self.projection = nn.Linear(state_size, state_size)
        
    def forward(self, trace_data: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Process execution trace data into embeddings"""
        # Get trace tensors
        event_types = trace_data["event_types"]
        functions = trace_data["functions"]
        lines = trace_data["lines"]
        var_counts = trace_data["var_counts"]
        
        # Get mask for valid events
        mask = trace_data["mask"]
        
        # Embed components
        event_embeds = self.event_embedding(event_types)
        func_embeds = self.function_embedding(functions)
        line_embeds = self.line_embedding(lines)
        var_embeds = self.var_count_embedding(var_counts)
        
        # Combine embeddings
        combined_embeds = torch.cat([event_embeds, func_embeds, line_embeds, var_embeds], dim=-1)
        
        # Apply LSTM
        packed_embeds = nn.utils.rnn.pack_padded_sequence(
            combined_embeds, 
            lengths=mask.sum(dim=1).cpu(),
            batch_first=True,
            enforce_sorted=False
        )
        
        _, (hidden, _) = self.lstm(packed_embeds)
        
        # Combine directions
        hidden = hidden.transpose(0, 1).contiguous()
        hidden = hidden.view(hidden.size(0), -1)
        
        # Final projection
        state = self.projection(hidden)
        
        return state


class VersionHistoryEncoder(nn.Module):
    """Neural network module to encode version history information"""
    def __init__(self, embedding_size: int, state_size: int, max_versions: int = 10):
        super().__init__()
        self.embedding_size = embedding_size
        self.state_size = state_size
        self.max_versions = max_versions
        
        # Version embedding
        self.version_embedding = nn.Embedding(100, embedding_size // 2)
        
        # Changes embedding
        self.changes_fc = nn.Linear(3, embedding_size // 2)  # [additions, deletions, files_changed]
        
        # LSTM for sequential processing
        self.lstm = nn.LSTM(
            input_size=embedding_size,
            hidden_size=state_size // 2,
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )
        
        # Projection
        self.projection = nn.Linear(state_size, state_size)
        
    def forward(self, history_data: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Process version history data into embeddings"""
        # Get history tensors
        versions = history_data["versions"]
        changes = history_data["changes"]  # [batch_size, max_versions, 3]
        
        # Get mask for valid versions
        mask = history_data["mask"]
        
        # Embed versions
        version_embeds = self.version_embedding(versions)
        
        # Embed changes
        changes_embeds = self.changes_fc(changes)
        
        # Combine embeddings
        combined_embeds = torch.cat([version_embeds, changes_embeds], dim=-1)
        
        # Apply mask
        combined_embeds = combined_embeds * mask.unsqueeze(-1)
        
        # Apply LSTM
        packed_embeds = nn.utils.rnn.pack_padded_sequence(
            combined_embeds, 
            lengths=mask.sum(dim=1).cpu(),
            batch_first=True,
            enforce_sorted=False
        )
        
        _, (hidden, _) = self.lstm(packed_embeds)
        
        # Combine directions
        hidden = hidden.transpose(0, 1).contiguous()
        hidden = hidden.view(hidden.size(0), -1)
        
        # Final projection
        state = self.projection(hidden)
        
        return state


# ============================================================================
# Enhanced Neural Network Modules
# ============================================================================

class NLDescriptionEncoder(nn.Module):
    """Neural network module to encode natural language descriptions"""
    def __init__(self, vocab_size: int, embedding_size: int, state_size: int):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.state_size = state_size
        
        # Word embedding
        self.word_embedding = nn.Embedding(vocab_size, embedding_size)
        
        # LSTM for sequential processing
        self.lstm = nn.LSTM(
            input_size=embedding_size,
            hidden_size=state_size // 2,
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )
        
        # Projection
        self.projection = nn.Linear(state_size, state_size)
        
    def forward(self, nl_data: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Process natural language data into embeddings"""
        # Get word tokens and mask
        word_ids = nl_data["word_ids"]
        mask = nl_data["mask"]
        
        # Embed words
        word_embeds = self.word_embedding(word_ids)
        
        # Apply mask
        word_embeds = word_embeds * mask.unsqueeze(-1)
        
        # Apply LSTM
        packed_embeds = nn.utils.rnn.pack_padded_sequence(
            word_embeds, 
            lengths=mask.sum(dim=1).cpu(),
            batch_first=True,
            enforce_sorted=False
        )
        
        _, (hidden, _) = self.lstm(packed_embeds)
        
        # Combine directions
        hidden = hidden.transpose(0, 1).contiguous()
        hidden = hidden.view(hidden.size(0), -1)
        
        # Final projection
        state = self.projection(hidden)
        
        return state


class EnhancedCodeEncoder(nn.Module):
    """Comprehensive encoder for code with ALL available representations"""
    def __init__(
        self, 
        vocab_size: int, 
        embedding_size: int, 
        state_size: int,
        graph_embedding_size: int,
        max_ast_nodes: int = 1000,
        max_graph_nodes: int = 1000,
        max_bytecode_instructions: int = 500,
        max_trace_events: int = 300,
        max_versions: int = 10,
        use_checkpoint: bool = False
    ):
        super().__init__()
        self.use_checkpoint = use_checkpoint
        self.state_size = state_size
        
        # Token embedding layer
        self.token_embedding = nn.Embedding(
            vocab_size, 
            embedding_size,
            sparse=True  # Enable sparse gradients for embeddings
        )
        
        # Token-based code encoder - bidirectional doubles the output size
        self.code_encoder = nn.LSTM(
            input_size=embedding_size,
            hidden_size=state_size // 2,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            proj_size=0
        )
        
        # Graph encoders for all graph types
        self.ast_encoder = EnhancedGraphEncoder(
            graph_embedding_size, 
            state_size,
            max_nodes=max_ast_nodes
        )
        
        self.cfg_encoder = EnhancedGraphEncoder(
            graph_embedding_size, 
            state_size,
            max_nodes=max_graph_nodes
        )
        
        self.dfg_encoder = EnhancedGraphEncoder(
            graph_embedding_size, 
            state_size,
            max_nodes=max_graph_nodes
        )
        
        self.pdg_encoder = EnhancedGraphEncoder(
            graph_embedding_size, 
            state_size,
            max_nodes=max_graph_nodes
        )
        
        self.dep_encoder = EnhancedGraphEncoder(
            graph_embedding_size, 
            state_size,
            max_nodes=max_graph_nodes
        )
        
        # Bytecode encoder
        self.bytecode_encoder = BytecodeEncoder(
            embedding_size,
            state_size,
            max_instructions=max_bytecode_instructions
        )
        
        # Execution trace encoder
        self.trace_encoder = TraceEncoder(
            embedding_size,
            state_size,
            max_trace_events=max_trace_events
        )
        
        # Version history encoder
        self.version_encoder = VersionHistoryEncoder(
            embedding_size,
            state_size,
            max_versions=max_versions
        )
        
        # Natural language description encoder
        self.nl_encoder = NLDescriptionEncoder(
            vocab_size,
            embedding_size,
            state_size
        )
        
        # Calculate number of encoders
        self.num_encoders = 10  # tokens, AST, CFG, DFG, PDG, dep, bytecode, trace, version, NL
        
        # Final projection to combine all representations
        self.combined_projection = nn.Linear(state_size * self.num_encoders, state_size)
        
        # FIX: The feature attention should match the state_size (not state_size*2)
        # We'll project the LSTM hidden state first, then all encoders will have the same size
        self.feature_attention = nn.Linear(state_size, 1)
        
        # Optional projection to reduce LSTM hidden state from state_size*2 to state_size
        self.hidden_projection = nn.Linear(state_size * 2, state_size)
    
    def _run_encoder(self, embedded):
        """Helper function for use with checkpoint"""
        return self.code_encoder(embedded)
    
    def forward(self, batch: Dict[str, Any]) -> torch.Tensor:
        """
        Process code with all available representations
        
        Args:
            batch: Dictionary containing various code representations
                
        Returns:
            Tensor of shape [batch_size, state_size]
        """
        # Process code tokens
        input_ids = batch["input_ids"]
        embedded = self.token_embedding(input_ids)
        
        # Apply token encoder with checkpointing if needed
        if self.use_checkpoint and self.training:
            # Use checkpoint with explicit use_reentrant=False parameter
            dummy = torch.zeros(1, requires_grad=True, device=embedded.device)
            output, (hidden, _) = torch.utils.checkpoint.checkpoint(
                lambda x, _: self._run_encoder(x), 
                embedded, 
                dummy, 
                use_reentrant=False
            )
        else:
            # Direct forward pass without checkpointing
            output, (hidden, _) = self.code_encoder(embedded)
        
        # Combine directions and layers of LSTM
        hidden = hidden.permute(1, 0, 2).contiguous()
        hidden = hidden.view(hidden.size(0), -1)
        
        # Project the hidden state from state_size*2 to state_size to match other encoders
        projected_hidden = self.hidden_projection(hidden)
        
        # Initialize list of all encodings
        all_encodings = [projected_hidden]  # Token-based encoding with consistent size
        
        # Process AST if available
        if "ast_graph" in batch:
            ast_state = self.ast_encoder(batch["ast_graph"])
            all_encodings.append(ast_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process CFG if available
        if "cfg_graph" in batch:
            cfg_state = self.cfg_encoder(batch["cfg_graph"])
            all_encodings.append(cfg_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process DFG if available
        if "dfg_graph" in batch:
            dfg_state = self.dfg_encoder(batch["dfg_graph"])
            all_encodings.append(dfg_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process PDG if available
        if "pdg_graph" in batch:
            pdg_state = self.pdg_encoder(batch["pdg_graph"])
            all_encodings.append(pdg_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process dependency graph if available
        if "dep_graph" in batch:
            dep_state = self.dep_encoder(batch["dep_graph"])
            all_encodings.append(dep_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process bytecode if available
        if "bytecode_data" in batch:
            bytecode_state = self.bytecode_encoder(batch["bytecode_data"])
            all_encodings.append(bytecode_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process execution trace if available
        if "trace_data" in batch:
            trace_state = self.trace_encoder(batch["trace_data"])
            all_encodings.append(trace_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process version history if available
        if "version_data" in batch:
            version_state = self.version_encoder(batch["version_data"])
            all_encodings.append(version_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Process natural language description if available
        if "nl_data" in batch:
            nl_state = self.nl_encoder(batch["nl_data"])
            all_encodings.append(nl_state)
        else:
            all_encodings.append(torch.zeros_like(projected_hidden))
        
        # Stack all encodings - each encoder outputs state_size-dimensional vectors
        stacked_encodings = torch.stack(all_encodings, dim=1)  # [batch_size, num_encoders, state_size]
        
        # Get batch size and num_encoders for reshaping
        batch_size, num_encoders, _ = stacked_encodings.size()
        
        # Apply attention to weight different encodings
        # Reshape to combine batch and encoder dimensions for linear layer
        reshaped_encodings = stacked_encodings.reshape(batch_size * num_encoders, -1)
        attn_scores = self.feature_attention(reshaped_encodings)  # [batch_size * num_encoders, 1]
        attn_scores = attn_scores.reshape(batch_size, num_encoders, 1)
        
        # Weighted sum of encodings
        attn_weights = torch.softmax(attn_scores, dim=1)
        weighted_encoding = torch.sum(stacked_encodings * attn_weights, dim=1)  # [batch_size, state_size]
        
        return weighted_encoding

    def get_sparse_params(self):
        """Return parameters that should use sparse optimizer"""
        return [self.token_embedding.weight]
        
    def get_dense_params(self):
        """Return parameters that should use dense optimizer"""
        return [p for n, p in self.named_parameters() if 'token_embedding.weight' not in n]

# ============================================================================
# Core Neural Network Modules
# ============================================================================

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


class CodeCellularMemory(nn.Module):
    """
    Implementation of the complete cellular memory dynamics for code
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
        
        # Emergent properties detector - for code patterns
        self.emergence_detector = nn.Linear(state_size, 1)
        self.collective_threshold = params.collective_threshold
        
        # Code-specific analyzers
        self.complexity_analyzer = nn.Linear(state_size, 5)  # Outputs complexity metrics
        self.pattern_detector = nn.Linear(state_size, 10)    # Outputs algorithm pattern scores
        self.security_analyzer = nn.Linear(state_size, 8)    # Outputs security vulnerability scores
        
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
    
    def analyze_code_patterns(self, state: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Analyze code state for complexity and patterns"""
        # Compute complexity metrics
        complexity_scores = self.complexity_analyzer(state)
        
        # Compute algorithm pattern detection scores
        pattern_scores = torch.sigmoid(self.pattern_detector(state))
        
        # Compute security vulnerability scores
        security_scores = torch.sigmoid(self.security_analyzer(state))
        
        return {
            'complexity': complexity_scores,
            'patterns': pattern_scores,
            'security': security_scores
        }
    
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
        
        # Analyze code patterns
        code_analysis = self.analyze_code_patterns(new_state)
            
        return {
            'new_state': new_state,
            'transition_prob': transition_prob,
            'memory_state': memory_state,
            'emergence': emergence,
            'complexity': code_analysis['complexity'],
            'patterns': code_analysis['patterns'],
            'security': code_analysis['security']
        }


class CodeDecoder(nn.Module):
    """Decodes state vectors back to code"""
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
               max_length: int = 100) -> torch.Tensor:
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

# ============================================================================
# Distributed Processing Components
# ============================================================================

@ray.remote
class CodeCellPartition:
    """
    Ray actor for parallel cellular processing of code
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
        self.cell = CodeCellularMemory(
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
            
            # Return state and metadata
            return {
                'state': self.state.cpu().numpy(),
                'transition_prob': result['transition_prob'].cpu().numpy(),
                'memory_state': result['memory_state'].cpu().numpy(),
                'emergence': emergence_val,
                'time': self.current_time,
                'complexity': result['complexity'].cpu().numpy(),
                'patterns': result['patterns'].cpu().numpy(),
                'security': result['security'].cpu().numpy()
            }
        
    def get_state(self) -> Dict[str, np.ndarray]:
        """Get current state and metadata"""
        return {
            'state': self.state.cpu().numpy(),
            'time': self.current_time
        }

# ============================================================================
# Main Entry Point
# ============================================================================

def create_default_params() -> ModelParams:
    """Create default parameters for the CodeCellAI model"""
    return ModelParams(
        # Core cellular parameters
        dt=0.1,                 # Time step for memory dynamics
        D=0.05,                 # Diffusion coefficient for state propagation
        gamma=0.01,             # Decay rate for memory
        eta=0.001,              # Noise amplitude
        num_partitions=8,       # Number of parallel partitions
        state_size=1024,        # Size of state vector per partition
        
        # State transition parameters
        temperature=0.7,        # Temperature for Boltzmann distribution
        energy_scale=1.0,       # Scale factor for energy calculations
        
        # Temporal memory parameters
        memory_tau=5.0,         # Memory time constant
        kernel_terms=3,         # Number of terms in memory kernel expansion
        kernel_decays=[1.0, 5.0, 10.0],  # Decay rates for memory kernel terms
        
        # Boundary condition parameters
        boundary_strength=0.1,  # Coupling strength at boundaries
        
        # Emergent properties parameters
        collective_threshold=0.6,  # Threshold for collective behavior emergence
        
        # Code parameters
        embedding_size=256,     # Size of code embeddings
        vocab_size=50000,       # Size of code token vocabulary
        max_seq_length=512,     # Maximum sequence length
        max_ast_nodes=1000,     # Maximum number of AST nodes
        max_graph_nodes=1000,   # Maximum number of graph nodes
        max_bytecode_instr=500, # Maximum number of bytecode instructions
        max_trace_events=300,   # Maximum number of execution trace events
        max_versions=10,        # Maximum number of version history entries
        
        # Training parameters
        learning_rate=0.001,    # Learning rate for training
        batch_size=32,          # Batch size for training
        accumulation_steps=4,   # Steps for gradient accumulation
        early_stopping_patience=3  # Patience for early stopping
    )

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="CodeCellAI - Complete Cellular AI Framework for Software Analysis and Generation")
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Train command
    train_parser = subparsers.add_parser("train", help="Train the model on a code dataset")
    train_parser.add_argument("--data", type=str, required=True, help="Path to code dataset (.jsonl or .jsonl.gz)")
    train_parser.add_argument("--epochs", type=int, default=3, help="Number of epochs to train for")
    train_parser.add_argument("--save_path", type=str, default="./codecellai_model_checkpoints", help="Path to save model checkpoints")
    train_parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training")
    train_parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    train_parser.add_argument("--state_size", type=int, default=1024, help="State vector size")
    train_parser.add_argument("--num_partitions", type=int, default=8, help="Number of cellular partitions")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate code from a prompt")
    generate_parser.add_argument("--model", type=str, required=True, help="Path to model checkpoint")
    generate_parser.add_argument("--prompt", type=str, required=True, help="Prompt for code generation")
    generate_parser.add_argument("--max_length", type=int, default=200, help="Maximum length of generated code")
    generate_parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for sampling")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze code with full CellAI framework")
    analyze_parser.add_argument("--model", type=str, required=True, help="Path to model checkpoint")
    analyze_parser.add_argument("--code", type=str, help="Path to code file to analyze")
    analyze_parser.add_argument("--code_string", type=str, help="Code string to analyze (alternative to --code)")
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark model performance")
    benchmark_parser.add_argument("--model", type=str, required=True, help="Path to model checkpoint")
    benchmark_parser.add_argument("--test", type=str, required=True, help="Path to test dataset (.jsonl or .jsonl.gz)")
    benchmark_parser.add_argument("--num_samples", type=int, default=100, help="Number of samples to use for benchmarking")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create default parameters
    params = create_default_params()
    
    # Update parameters from command line
    if args.command == "train":
        params.batch_size = args.batch_size
        params.learning_rate = args.lr
        params.state_size = args.state_size
        params.num_partitions = args.num_partitions
    
    # Initialize the model
    model = CodeCellularSystem(params)
    
    try:
        # Handle commands
        if args.command == "train":
            model.train_on_dataset(args.data, args.epochs, args.save_path)
            
        elif args.command == "generate":
            # Load model
            model.load_model(args.model)
            
            # Generate code
            generated_code = model.generate_code(args.prompt, args.max_length, args.temperature)
            
            # Print generated code
            print("\nGenerated Code:\n")
            print("```python")
            print(generated_code)
            print("```\n")
            
        elif args.command == "analyze":
            # Load model
            model.load_model(args.model)
            
            # Get code to analyze
            if args.code:
                with open(args.code, "r", encoding="utf-8") as f:
                    code = f.read()
            elif args.code_string:
                code = args.code_string
            else:
                parser.error("Either --code or --code_string must be provided")
                
            # Analyze code
            analysis = model.analyze_code(code)
            
            # Print analysis results
            print("\nCode Analysis Results:\n")
            print(f"Natural Language Description: {analysis.get('natural_language_description', '')}")
            print("\nComplexity Metrics:")
            for key, value in analysis.get("metrics", {}).items():
                print(f"  {key}: {value}")
                
            print("\nDetected Algorithm Patterns:")
            for pattern, score in analysis.get("patterns", {}).items():
                if score > 0.5:
                    print(f"  {pattern}: {score:.2f}")
                    
            print("\nPotential Security Vulnerabilities:")
            for vuln, score in analysis.get("vulnerabilities", {}).items():
                if score > 0.3:
                    print(f"  {vuln}: {score:.2f}")
                    
            print("\nPerformance Estimates:")
            for key, value in analysis.get("performance", {}).items():
                print(f"  {key}: {value}")
                
            print(f"\nProcessing Time: {analysis.get('processing_time', 0):.2f} seconds")
            
        elif args.command == "benchmark":
            # Load model
            model.load_model(args.model)
            
            # Run benchmark
            benchmark_results = model.benchmark(args.test, args.num_samples)
            
            # Print benchmark results
            if benchmark_results:
                print("\nBenchmark Results:\n")
                print(f"Average Processing Time: {benchmark_results['avg_processing_time']:.4f} seconds per sample")
                print(f"Average Analysis Time: {benchmark_results['avg_analysis_time']:.4f} seconds per sample")
                print(f"Average Generation Time: {benchmark_results['avg_generation_time']:.4f} seconds per sample")
                print(f"Tokens per Second: {benchmark_results['tokens_per_second']:.2f}")
        else:
            parser.print_help()
            
    finally:
        # Clean up resources
        model.cleanup()
        
if __name__ == "__main__":
    main()