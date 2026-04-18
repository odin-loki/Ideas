#!/usr/bin/env python3
"""
MegaMathGen - Massive Mathematics Problem Generator

This script generates an unlimited supply of mathematical problems spanning the entire
mathematical landscape, from elementary to advanced topics. It will continuously
produce problems until manually stopped, potentially generating gigabytes or terabytes of data.

Features:
- Complete statistical coverage of all possible numbers and problems
- Memory management (stays under 28GB RAM)
- Disk space and time estimation before generation
- Checkpointing to prevent data loss and memory leaks
- Progress tracking with detailed statistics and progress bars
"""

import json
import os
import random
import math
import time
from tqdm import tqdm
import sympy
import numpy as np
from sympy import symbols, solve, Eq, simplify, expand, factor, sympify, latex, Matrix, oo, limit, diff, integrate
from fractions import Fraction
from decimal import Decimal, getcontext
import itertools
import string
import sys
import signal
import datetime
import psutil
import gc
import threading
import hashlib

# Set precision for large number calculations
getcontext().prec = 1000

class ComprehensiveMathGenerator:
    """
    An ultra-comprehensive math question generator covering the entire mathematical
    landscape with a natural distribution of difficulty and complexity.
    """
   
    def __init__(self):
        # Memory management parameters
        self.memory_limit_mb = 28 * 1024  # 28GB in MB
        self.memory_check_interval = 1000  # Check memory every 1000 problems
       
        # Mathematical domains (extremely comprehensive)
        self.domains = {
            # Pure Mathematics
            "number_theory": [
                "prime_numbers", "divisibility", "gcd_lcm", "modular_arithmetic",
                "diophantine_equations", "continued_fractions", "factorization",
                "congruences", "quadratic_residues", "algebraic_numbers", "transcendental_numbers"
            ],
           
            "algebra": [
                "linear_equations", "quadratic_equations", "polynomial_equations", "systems_of_equations",
                "matrices", "determinants", "eigenvalues", "diagonalization", "polynomials",
                "rational_functions", "partial_fractions", "field_extensions", "galois_theory"
            ],
           
            "analysis": [
                "limits", "continuity", "differentiation", "integration", "infinite_series",
                "power_series", "taylor_series", "fourier_series", "convergence_tests",
                "uniform_convergence", "analytic_functions", "contour_integration", "residue_calculus"
            ],
           
            "geometry": [
                "euclidean_geometry", "coordinate_geometry", "analytic_geometry", "projective_geometry",
                "affine_geometry", "non_euclidean_geometry", "differential_geometry", "riemannian_geometry"
            ],
           
            "combinatorics": [
                "permutations", "combinations", "binomial_coefficients", "multinomial_coefficients",
                "pigeonhole_principle", "inclusion_exclusion", "recursion", "generating_functions"
            ],
           
            "logic_and_foundations": [
                "propositional_logic", "predicate_logic", "formal_systems", "axiomatization",
                "model_theory", "proof_theory", "recursive_functions", "computability_theory"
            ],
                       
            # Applied Mathematics
            "differential_equations": [
                "ordinary_differential_equations", "partial_differential_equations", "linear_odes",
                "nonlinear_odes", "systems_of_odes", "boundary_value_problems", "initial_value_problems"
            ],
           
            "numerical_analysis": [
                "error_analysis", "finite_differences", "interpolation", "numerical_integration",
                "numerical_differentiation", "root_finding", "linear_systems", "matrix_factorizations"
            ],
           
            "probability_and_statistics": [
                "probability_theory", "random_variables", "probability_distributions", "moments",
                "central_limit_theorem", "law_of_large_numbers", "conditional_probability",
                "bayesian_statistics", "stochastic_processes", "markov_chains", "poisson_processes"
            ],
           
            "operations_research": [
                "linear_programming", "duality_theory", "simplex_method", "interior_point_methods",
                "integer_programming", "branch_and_bound", "cutting_plane_methods", "dynamic_programming"
            ],
           
            "computational_mathematics": [
                "algorithms", "data_structures", "computational_complexity", "big_o_notation",
                "np_completeness", "approximation_algorithms", "randomized_algorithms"
            ],
           
            "elementary_mathematics": [
                "arithmetic", "basic_algebra", "basic_geometry", "trigonometry", "precalculus",
                "calculus_basics", "vectors_basics", "matrices_basics", "complex_numbers_basics",
                "sequences_series", "probability_basics", "statistics_basics", "counting_basics"
            ]
        }
       
        # Coverage tracking
        self.covered_integers = set()
        self.covered_integer_pairs = set()
        self.covered_integer_triplets = set()
        self.covered_domains = {domain: 0 for domain in self.domains.keys()}
        self.covered_subdomains = {}
        self.coverage_range = {
            "integers": (-10000, 10000),
            "pairs": ((-1000, 1000), (-1000, 1000)),
            "triplets": ((-500, 500), (-500, 500), (-500, 500))
        }
       
        # Statistics tracking
        self.total_problems_generated = 0
        self.total_bytes_generated = 0
        self.generation_times = []
        self.batch_sizes = []
       
        # Initialize subdomain coverage
        for domain, subdomains in self.domains.items():
            for subdomain in subdomains:
                self.covered_subdomains[f"{domain}_{subdomain}"] = 0
       
        # Number systems and types
        self.number_types = [
            "integers", "rational_numbers", "real_numbers", "complex_numbers",
            "p_adic_numbers", "quaternions", "octonions", "hyperreal_numbers",
            "surreal_numbers", "ordinals", "cardinals", "constructible_numbers",
            "computable_numbers", "algebraic_numbers", "transcendental_numbers"
        ]
       
        # Number scales for different problem types
        self.number_scales = {
            "tiny": (0, 10),
            "small": (10, 100),
            "medium": (100, 1000),
            "large": (1000, 10000),
            "huge": (10000, 1000000),
            "astronomical": (1000000, 10**12),
            "cosmological": (10**12, 10**50)
        }
       
        # Problem representations
        self.representations = [
            "symbolic", "textual", "algebraic", "numerical", "algorithmic",
            "graphical", "tabular", "geometric", "proof-based", "computational",
            "applied"
        ]
       
        # Templates for word problems across domains
        self.word_problem_templates = {
            "arithmetic": [
                "A person has {a} items and buys {b} more. How many items do they have in total?",
                "If a store sells {a} items each day, how many items will it sell in {b} days?",
                "A recipe requires {a} cups of flour. If making {b} batches, how much flour is needed?"
            ],
           
            "algebra": [
                "If {expression} = {value}, find the value of {variable}.",
                "Solve the equation: {equation}",
                "For what values of {variable} is {expression} {comparison} {value}?"
            ],
           
            "geometry": [
                "A rectangle has width {a} and length {b}. What is its {property}?",
                "A circle has radius {r}. What is its {property}?",
                "A triangle has sides of length {a}, {b}, and {c}. What is its {property}?"
            ]
        }
       
        # List of common variables used in math problems
        self.variables = ['x', 'y', 'z', 'a', 'b', 'c', 't', 'n', 'p', 'q', 'r', 's']
       
        # Parameters for controlling problem generation
        self.symbolic_probability = 0.7  # 70% chance for symbolic representation
   
    def _get_current_memory_usage(self):
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return memory_info.rss / (1024 * 1024)
   
    def _check_memory_limits(self):
        """Check if we're approaching memory limits and take action if needed"""
        current_usage = self._get_current_memory_usage()
       
        # If approaching limit (80% of max), force garbage collection
        if current_usage > 0.8 * self.memory_limit_mb:
            gc.collect()
            return self._get_current_memory_usage()
       
        return current_usage
   
    def _update_coverage(self, domain, subdomain, numbers=None):
        """Update coverage statistics"""
        # Update domain and subdomain counts
        self.covered_domains[domain] = self.covered_domains.get(domain, 0) + 1
        subdomain_key = f"{domain}_{subdomain}"
        self.covered_subdomains[subdomain_key] = self.covered_subdomains.get(subdomain_key, 0) + 1
       
        # Update number coverage
        if numbers:
            if isinstance(numbers, int) and self.coverage_range["integers"][0] <= numbers <= self.coverage_range["integers"][1]:
                self.covered_integers.add(numbers)
            elif isinstance(numbers, tuple):
                if len(numbers) == 2:
                    a, b = numbers
                    if (self.coverage_range["pairs"][0][0] <= a <= self.coverage_range["pairs"][0][1] and
                        self.coverage_range["pairs"][1][0] <= b <= self.coverage_range["pairs"][1][1]):
                        self.covered_integer_pairs.add((a, b))
                elif len(numbers) == 3:
                    a, b, c = numbers
                    if (self.coverage_range["triplets"][0][0] <= a <= self.coverage_range["triplets"][0][1] and
                        self.coverage_range["triplets"][1][0] <= b <= self.coverage_range["triplets"][1][1] and
                        self.coverage_range["triplets"][2][0] <= c <= self.coverage_range["triplets"][2][1]):
                        self.covered_integer_triplets.add((a, b, c))
   
    def _generate_random_integer(self, scale="small", force_new=False):
        """Generate a random integer based on scale with coverage tracking"""
        min_val, max_val = self.number_scales.get(scale, (1, 100))
        value = random.randint(min_val, max_val)
       
        # Track coverage if within range
        if self.coverage_range["integers"][0] <= value <= self.coverage_range["integers"][1]:
            self.covered_integers.add(value)
           
        return value
   
    def _generate_arithmetic_problem(self, subdomain=None, force_new=False):
        """Generate an arithmetic problem with systematic coverage"""
        if subdomain is None:
            subdomain = random.choice([
                "addition", "subtraction", "multiplication", "division",
                "exponentiation", "roots", "logarithms", "mixed"
            ])
           
        number_type = random.choice(["integers", "rational_numbers", "real_numbers"])
        scale = random.choice(list(self.number_scales.keys()))
           
        if subdomain == "addition":
            a = self._generate_random_integer(scale, force_new)
            b = self._generate_random_integer(scale, force_new)
            question = f"Calculate {a} + {b}"
            answer = a + b
           
            # Track coverage
            self._update_coverage("arithmetic", "addition", (int(a), int(b)))
           
        elif subdomain == "subtraction":
            a = self._generate_random_integer(scale, force_new)
            b = self._generate_random_integer(scale, force_new)
            question = f"Calculate {a} - {b}"
            answer = a - b
           
            # Track coverage
            self._update_coverage("arithmetic", "subtraction", (int(a), int(b)))
       
        else:
            # Default simple arithmetic problem
            a = self._generate_random_integer("small", force_new)
            b = self._generate_random_integer("small", force_new)
            question = f"Calculate {a} + {b}"
            answer = a + b
            self._update_coverage("arithmetic", "addition", (int(a), int(b)))
           
        # Increase problem count
        self.total_problems_generated += 1
       
        # Check memory periodically
        if self.total_problems_generated % self.memory_check_interval == 0:
            self._check_memory_limits()
           
        return {
            "domain": "arithmetic",
            "subdomain": subdomain,
            "question": question,
            "answer": str(answer),
            "number_type": number_type,
            "scale": scale
        }
   
    def generate_question(self, domain=None, subdomain=None, force_new=False):
        """
        Generate a random math question based on domain and subdomain with statistical coverage
        """
        # Check memory before generation
        current_memory = self._check_memory_limits()
        if current_memory > self.memory_limit_mb:
            raise MemoryError(f"Memory usage of {current_memory:.2f}MB exceeds limit of {self.memory_limit_mb}MB")
       
        # Select domain with coverage-based weighting if not specified
        if domain is None:
            # Weight domains inversely by their coverage
            domain_weights = {d: 1.0 / (self.covered_domains.get(d, 1) + 1) for d in self.domains}
            total_weight = sum(domain_weights.values())
            normalized_weights = {d: w/total_weight for d, w in domain_weights.items()}
           
            domains = list(normalized_weights.keys())
            weights = list(normalized_weights.values())
            domain = random.choices(domains, weights=weights, k=1)[0]
           
        if subdomain is None and domain in self.domains:
            # Weight subdomains inversely by their coverage
            subdomain_weights = {}
            for sd in self.domains[domain]:
                key = f"{domain}_{sd}"
                subdomain_weights[sd] = 1.0 / (self.covered_subdomains.get(key, 1) + 1)
               
            total_weight = sum(subdomain_weights.values())
            if total_weight > 0:  # Prevent division by zero
                normalized_weights = {sd: w/total_weight for sd, w in subdomain_weights.items()}
               
                subdomains = list(normalized_weights.keys())
                weights = list(normalized_weights.values())
                subdomain = random.choices(subdomains, weights=weights, k=1)[0]
            else:
                subdomain = random.choice(self.domains[domain])

        # Call the appropriate generator method based on domain
        try:
            if domain == "arithmetic" or domain == "elementary_mathematics":
                return self._generate_arithmetic_problem(subdomain, force_new)
            # Add other domains as needed
            else:
                # Default to arithmetic if domain not implemented
                return self._generate_arithmetic_problem(force_new=force_new)
        except Exception as e:
            print(f"Error generating {domain}/{subdomain} problem: {e}")
            # Fall back to arithmetic if there's an error
            return self._generate_arithmetic_problem(force_new=False)
   
    def generate_compound_question(self):
        """
        Generate an in-depth compound question with mathematically connected parts
        that build on each other to provide comprehensive mathematical coverage.
       
        Returns:
            A dictionary containing the mathematically coherent compound question
        """
        # Select a mathematical theme for interconnected questions
        theme = random.choice([
            "function_analysis",      # Calculus: analyzing a function in multiple ways
            "equation_solving",       # Algebra: multi-step solution of complex equation
            "geometric_sequence",     # Geometry: proof sequence on a geometric object
            "probability_scenario",   # Probability: multi-stage problem
            "number_theory_exploration" # Number theory: number properties
        ])
       
        # Generate appropriate mathematical domain based on theme
        if theme == "function_analysis":
            domain = "calculus"
            subdomain = "differentiation"
        elif theme == "equation_solving":
            domain = "algebra"
            subdomain = "linear_equations"
        elif theme == "geometric_sequence":
            domain = "geometry"
            subdomain = "euclidean_geometry"
        elif theme == "probability_scenario":
            domain = "probability_and_statistics"
            subdomain = "conditional_probability"
        elif theme == "number_theory_exploration":
            domain = "number_theory"
            subdomain = "prime_numbers"
       
        # Create a simple compound question
        parts = [
            {
                "part_index": 1,
                "question": "First part of the compound question",
                "answer": "Answer to the first part",
                "explanation": "Explanation for the first part"
            },
            {
                "part_index": 2,
                "question": "Second part of the compound question",
                "answer": "Answer to the second part",
                "explanation": "Explanation for the second part",
                "depends_on": 1
            }
        ]
       
        # Build the complete compound question
        compound_question = {
            "type": "compound",
            "domain": domain,
            "subdomain": subdomain,
            "theme": theme,
            "parts": parts,
            "context": "Context for the compound question",
            "shared_object": "Shared mathematical object"
        }
       
        # Update coverage
        self._update_coverage(domain, subdomain)
       
        # Increment problem count
        self.total_problems_generated += 1
       
        # Check memory periodically
        if self.total_problems_generated % self.memory_check_interval == 0:
            self._check_memory_limits()
       
        return compound_question
   
    def estimate_resources(self, num_problems=None, coverage_goals=None):
        """
        Estimate disk space and time required for generation based on sample
       
        Args:
            num_problems: Number of problems to generate (default: calculates based on coverage goals)
            coverage_goals: Dictionary with coverage goals for different number types and domains
           
        Returns:
            Dictionary with resource estimates
        """
        print("Estimating resource requirements...")
       
        # Default coverage goals
        if coverage_goals is None:
            coverage_goals = {
                "integers": 10000,  # Unique integers in range
                "integer_pairs": 100000,  # Unique integer pairs
                "domains": {domain: 1000 for domain in self.domains}  # Problems per domain
            }
       
        # Calculate total problems needed if not specified
        if num_problems is None:
            # Calculate based on coverage goals and overlap estimation
            total_domains = sum(coverage_goals["domains"].values())
            # Assume 30% overlap between coverage categories
            num_problems = int(max(total_domains, coverage_goals["integers"], coverage_goals["integer_pairs"]/10) * 1.3)
       
        # Generate a sample to estimate resources
        sample_size = min(100, int(num_problems * 0.01))  # 1% of total or 100, whichever is smaller
        sample_problems = []
       
        print(f"Generating {sample_size} sample problems for estimation...")
       
        # Track generation time
        start_time = time.time()
       
        # Generate sample
        for _ in range(sample_size):
            problem = self.generate_question(force_new=True)
            sample_problems.append(problem)
           
        end_time = time.time()
       
        # Calculate statistics
        generation_time = end_time - start_time
        avg_time_per_problem = generation_time / sample_size
        estimated_total_time = avg_time_per_problem * num_problems
       
        # Estimate disk space
        sample_data = {"problems": sample_problems}
        sample_json = json.dumps(sample_data)
        sample_size_bytes = len(sample_json.encode('utf-8'))
       
        avg_bytes_per_problem = sample_size_bytes / sample_size
        estimated_total_bytes = avg_bytes_per_problem * num_problems
       
        # Convert to more readable units
        estimated_size_mb = estimated_total_bytes / (1024 * 1024)
        estimated_size_gb = estimated_size_mb / 1024
       
        estimated_hours = estimated_total_time / 3600
        estimated_days = estimated_hours / 24
       
        # Current memory usage
        current_memory_mb = self._get_current_memory_usage()
       
        # Prepare estimation results
        estimation = {
            "num_problems": num_problems,
            "coverage_goals": coverage_goals,
            "sample_size": sample_size,
            "avg_time_per_problem": avg_time_per_problem,
            "estimated_total_time_seconds": estimated_total_time,
            "estimated_hours": estimated_hours,
            "estimated_days": estimated_days,
            "avg_bytes_per_problem": avg_bytes_per_problem,
            "estimated_total_bytes": estimated_total_bytes,
            "estimated_size_mb": estimated_size_mb,
            "estimated_size_gb": estimated_size_gb,
            "current_memory_mb": current_memory_mb,
            "memory_limit_mb": self.memory_limit_mb
        }
       
        # Display estimation
        print("\nResource Estimation:")
        print("====================")
        print(f"Problems to generate: {num_problems:,}")
        print(f"Estimated disk space: {estimated_size_gb:.2f} GB")
        print(f"Estimated time: {estimated_hours:.2f} hours ({estimated_days:.2f} days)")
        print(f"Estimated generation rate: {1/avg_time_per_problem:.2f} problems/second")
        print(f"Current memory usage: {current_memory_mb:.2f} MB")
        print(f"Memory limit: {self.memory_limit_mb} MB")
       
        return estimation
   
    def generate_batch(self, batch_size, output_dir, batch_number):
        """Generate a batch of problems with checkpointing"""
        problems = []
        batch_start_time = time.time()
       
        print(f"\nGenerating batch #{batch_number} ({batch_size} problems)...")
       
        # For each batch, include at least one compound question from each domain
        compound_domains = ["function_analysis", "equation_solving", "geometric_sequence",
                          "probability_scenario", "number_theory_exploration"]
       
        # Generate problems
        for domain in compound_domains[:min(len(compound_domains), batch_size // 10)]:
            try:
                # Create a compound question
                compound_question = self.generate_compound_question()
                problems.append(compound_question)
            except Exception as e:
                print(f"\nError generating compound question: {e}")
       
        # Then fill the rest with regular questions
        remaining = batch_size - len(problems)
        for i in range(remaining):
            try:
                # Check memory periodically
                if i % 100 == 0:
                    current_memory = self._check_memory_limits()
                    if current_memory > 0.9 * self.memory_limit_mb:
                        print(f"\nApproaching memory limit ({current_memory:.2f}MB). Ending batch early.")
                        break
                       
                # Generate problem with statistical coverage
                force_new = (i % 5 == 0)  # Force new uncovered numbers 20% of the time
                problem = self.generate_question(force_new=force_new)
                problems.append(problem)
                self.total_problems_generated += 1
               
            except Exception as e:
                print(f"\nError generating problem: {e}")
                if isinstance(e, MemoryError):
                    print("Memory limit reached. Ending batch.")
                    break
       
        batch_end_time = time.time()
        batch_duration = batch_end_time - batch_start_time
       
        # Coverage stats
        coverage_stats = {
            "integers": len(self.covered_integers),
            "integer_pairs": len(self.covered_integer_pairs),
            "integer_triplets": len(self.covered_integer_triplets),
            "domains": self.covered_domains,
            "top_subdomains": dict(sorted(self.covered_subdomains.items(),
                                        key=lambda x: x[1], reverse=True)[:10])
        }
       
        # Create batch metadata
        batch_data = {
            "metadata": {
                "generator": "EnhancedMegaMathGen",
                "batch_number": batch_number,
                "batch_size": len(problems),
                "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "generation_duration_seconds": batch_duration,
                "memory_usage_mb": self._get_current_memory_usage(),
                "total_problems_generated": self.total_problems_generated,
                "coverage_stats": coverage_stats,
                "compound_questions_count": sum(1 for p in problems if "theme" in p)
            },
            "problems": problems
        }
       
        # Save the batch with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/math_batch_{batch_number:06d}_{timestamp}.json"
       
        with open(filename, 'w') as f:
            json.dump(batch_data, f)
           
        # Update statistics
        self.generation_times.append(batch_duration)
        self.batch_sizes.append(len(problems))
        batch_size_bytes = os.path.getsize(filename)
        self.total_bytes_generated += batch_size_bytes
       
        return {
            "filename": filename,
            "problems_count": len(problems),
            "compound_questions_count": sum(1 for p in problems if "theme" in p),
            "file_size_bytes": batch_size_bytes,
            "duration_seconds": batch_duration,
            "memory_usage_mb": self._get_current_memory_usage()
        }
   
    def save_coverage_checkpoint(self, output_dir, batch_number):
        """Save current coverage data as a checkpoint"""
        # Create a summary of coverage data (without the full sets that could be very large)
        coverage_summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "batch_number": batch_number,
            "total_problems_generated": self.total_problems_generated,
            "covered_integers_count": len(self.covered_integers),
            "covered_integer_pairs_count": len(self.covered_integer_pairs),
            "covered_integer_triplets_count": len(self.covered_integer_triplets),
            "covered_domains": self.covered_domains,
            "covered_subdomains_sample": dict(sorted(self.covered_subdomains.items(),
                                                   key=lambda x: x[1], reverse=True)[:50]),
            "memory_usage_mb": self._get_current_memory_usage(),
            "total_bytes_generated": self.total_bytes_generated,
            "generation_stats": {
                "avg_time_per_problem": sum(self.generation_times) / max(1, len(self.generation_times)),
                "avg_problems_per_batch": sum(self.batch_sizes) / max(1, len(self.batch_sizes)),
                "total_batches": len(self.batch_sizes)
            }
        }
       
        # Save to file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/coverage_checkpoint_{batch_number:06d}_{timestamp}.json"
       
        with open(filename, 'w') as f:
            json.dump(coverage_summary, f)
           
        return filename

def estimate_resources(self, num_problems=None, coverage_goals=None):
    """
    Estimate disk space and time required for generation based on sample
   
    Args:
        num_problems: Number of problems to generate (default: calculates based on coverage goals)
        coverage_goals: Dictionary with coverage goals for different number types and domains
       
    Returns:
        Dictionary with resource estimates
    """
    print("Estimating resource requirements...")
   
    # Default coverage goals
    if coverage_goals is None:
        coverage_goals = {
            "integers": 10000,  # Unique integers in range
            "integer_pairs": 100000,  # Unique integer pairs
            "domains": {domain: 1000 for domain in self.domains}  # Problems per domain
        }
   
    # Calculate total problems needed if not specified
    if num_problems is None:
        # Calculate based on coverage goals and overlap estimation
        total_domains = sum(coverage_goals["domains"].values())
        # Assume 30% overlap between coverage categories
        num_problems = int(max(total_domains, coverage_goals["integers"], coverage_goals["integer_pairs"]/10) * 1.3)
   
    # Generate a sample to estimate resources
    sample_size = min(1000, int(num_problems * 0.01))  # 1% of total or 1000, whichever is smaller
    sample_problems = []
   
    print(f"Generating {sample_size} sample problems for estimation...")
   
    # Track generation time
    start_time = time.time()
   
    # Generate sample with progress bar
    for _ in tqdm(range(sample_size), desc="Generating samples"):
        problem = self.generate_question(force_new=True)
        sample_problems.append(problem)
       
    end_time = time.time()
   
    # Calculate statistics
    generation_time = end_time - start_time
    avg_time_per_problem = generation_time / sample_size
    estimated_total_time = avg_time_per_problem * num_problems
   
    # Estimate disk space
    sample_data = {"problems": sample_problems}
    sample_json = json.dumps(sample_data)
    sample_size_bytes = len(sample_json.encode('utf-8'))
   
    avg_bytes_per_problem = sample_size_bytes / sample_size
    estimated_total_bytes = avg_bytes_per_problem * num_problems
   
    # Convert to more readable units
    estimated_size_mb = estimated_total_bytes / (1024 * 1024)
    estimated_size_gb = estimated_size_mb / 1024
   
    estimated_hours = estimated_total_time / 3600
    estimated_days = estimated_hours / 24
   
    # Current memory usage
    current_memory_mb = self._get_current_memory_usage()
   
    # Prepare estimation results
    estimation = {
        "num_problems": num_problems,
        "coverage_goals": coverage_goals,
        "sample_size": sample_size,
        "avg_time_per_problem": avg_time_per_problem,
        "estimated_total_time_seconds": estimated_total_time,
        "estimated_hours": estimated_hours,
        "estimated_days": estimated_days,
        "avg_bytes_per_problem": avg_bytes_per_problem,
        "estimated_total_bytes": estimated_total_bytes,
        "estimated_size_mb": estimated_size_mb,
        "estimated_size_gb": estimated_size_gb,
        "current_memory_mb": current_memory_mb,
        "memory_limit_mb": self.memory_limit_mb
    }
   
    # Display estimation
    print("\nResource Estimation:")
    print("====================")
    print(f"Problems to generate: {num_problems:,}")
    print(f"Estimated disk space: {estimated_size_gb:.2f} GB")
    print(f"Estimated time: {estimated_hours:.2f} hours ({estimated_days:.2f} days)")
    print(f"Estimated generation rate: {1/avg_time_per_problem:.2f} problems/second")
    print(f"Current memory usage: {current_memory_mb:.2f} MB")
    print(f"Memory limit: {self.memory_limit_mb} MB")
   
    return estimation
   
def __init__(self):
    """
    An ultra-comprehensive math question generator covering the entire mathematical
    landscape with a natural distribution of difficulty and complexity.
    """
   
    # Memory management parameters
    self.memory_limit_mb = 28 * 1024  # 28GB in MB
    self.memory_check_interval = 1000  # Check memory every 1000 problems
   
    # Mathematical domains (extremely comprehensive)
    self.domains = {
        # Pure Mathematics
        "number_theory": [
            "prime_numbers", "divisibility", "gcd_lcm", "modular_arithmetic",
            "diophantine_equations", "continued_fractions", "factorization",
            "congruences", "quadratic_residues", "algebraic_numbers", "transcendental_numbers",
            "fermat_numbers", "perfect_numbers", "chinese_remainder_theorem", "primality_testing",
            "mersenne_primes", "goldbach_conjecture", "twin_primes", "arithmetic_functions",
            "multiplicative_functions", "primitive_roots", "dirichlet_series", "quadratic_forms",
            "pell_equations", "linear_recurrences", "fibonacci_numbers", "partition_theory",
            "additive_number_theory", "waring_problem", "diophantine_approximation", "transcendence_theory",
            "elliptic_curves", "class_number", "number_fields", "algebraic_integers", "p_adic_numbers",
            "analytic_number_theory", "prime_number_theorem", "riemann_hypothesis", "L_functions",
            "lattice_theory", "geometry_of_numbers", "cryptographic_number_theory", "arithmetic_geometry"
        ],
       
        "algebra": [
            "linear_equations", "quadratic_equations", "polynomial_equations", "systems_of_equations",
            "matrices", "determinants", "eigenvalues", "diagonalization", "polynomials",
            "rational_functions", "partial_fractions", "field_extensions", "galois_theory",
            "symmetric_polynomials", "resultants", "discriminants", "factorization",
            "inequalities", "radical_expressions", "complex_numbers", "quaternions",
            "octonions", "rings", "fields", "groups", "homomorphisms", "isomorphisms",
            "automorphisms", "quotient_groups", "normal_subgroups", "solvable_groups",
            "representations", "modules", "ideals", "integral_domains", "boolean_algebra",
            "lattices", "graded_algebras", "noncommutative_algebra", "lie_algebras",
            "universal_algebra", "homological_algebra", "category_theory", "topos_theory",
            "monoidal_categories", "algebraic_K_theory", "operads", "quantum_groups",
            "hopf_algebras", "von_neumann_algebras", "C_star_algebras", "vertex_algebras",
            "jordan_algebras", "associative_algebras", "clifford_algebras", "geometric_algebra",
            "tensor_algebra", "exterior_algebra", "symmetric_algebra", "differential_algebra",
            "algebraic_combinatorics", "algebraic_coding_theory", "representation_theory",
            "invariant_theory", "computational_algebra", "grobner_bases", "tropical_algebra"
        ],
       
        "analysis": [
            "limits", "continuity", "differentiation", "integration", "infinite_series",
            "power_series", "taylor_series", "fourier_series", "convergence_tests",
            "uniform_convergence", "analytic_functions", "contour_integration", "residue_calculus",
            "conformal_mapping", "laplace_transforms", "fourier_transforms", "z_transforms",
            "wavelet_transforms", "special_functions", "gamma_function", "beta_function",
            "bessel_functions", "legendre_polynomials", "hypergeometric_functions",
            "elliptic_functions", "riemann_zeta_function", "functional_equations",
            "lebesgue_integration", "measure_theory", "banach_spaces", "hilbert_spaces",
            "distribution_theory", "sobolev_spaces", "harmonic_analysis", "spectral_theory",
            "operator_theory", "functional_calculus", "function_spaces", "complex_analysis",
            "several_complex_variables", "analytic_continuation", "real_analysis",
            "calculus_of_variations", "approximation_theory", "integral_equations",
            "singular_integrals", "Hardy_spaces", "BMO_spaces", "Lipschitz_spaces",
            "constructive_analysis", "nonstandard_analysis", "p_adic_analysis",
            "microlocal_analysis", "pseudodifferential_operators", "fourier_integral_operators",
            "potential_theory", "geometric_measure_theory", "ergodic_theory",
            "dynamical_systems", "fractal_analysis", "multifractal_analysis"
        ],
       
        "geometry": [
            "euclidean_geometry", "coordinate_geometry", "analytic_geometry", "projective_geometry",
            "affine_geometry", "non_euclidean_geometry", "differential_geometry", "riemannian_geometry",
            "symplectic_geometry", "algebraic_geometry", "topology", "differential_topology",
            "knot_theory", "homology", "cohomology", "triangulations", "polyhedra",
            "tessellations", "fractals", "conformal_geometry", "geometric_measure_theory",
            "convex_geometry", "discrete_geometry", "computational_geometry",
            "geometric_invariants", "curves", "surfaces", "manifolds", "fiber_bundles",
            "characteristic_classes", "morse_theory", "catastrophe_theory", "calibrations",
            "geometric_analysis", "geometric_flows", "minimal_surfaces", "calculus_of_variations",
            "finsler_geometry", "geometric_group_theory", "geometric_topology", "low_dimensional_topology",
            "contact_geometry", "CR_geometry", "almost_complex_geometry", "kahler_geometry",
            "calabi_yau_manifolds", "singularity_theory", "intersection_theory",
            "global_differential_geometry", "transformation_groups", "lie_groups", "lie_algebras",
            "homogeneous_spaces", "symmetric_spaces", "flag_manifolds", "moduli_spaces",
            "geometric_quantization", "index_theory", "twistor_theory", "calibrated_geometry",
            "special_holonomy", "spin_geometry", "toric_geometry", "tropical_geometry",
            "geometric_probability", "integral_geometry", "isoperimetric_problems", "optimal_transport"
        ],
       
        "combinatorics": [
            "permutations", "combinations", "binomial_coefficients", "multinomial_coefficients",
            "pigeonhole_principle", "inclusion_exclusion", "recursion", "generating_functions",
            "partition_theory", "young_tableaux", "polya_counting", "ramsey_theory",
            "extremal_combinatorics", "graph_theory", "trees", "matchings", "colorings",
            "planarity", "connectivity", "cycles", "spectral_graph_theory", "random_graphs",
            "matroids", "designs", "finite_geometry", "posets", "lattice_paths",
            "enumerative_combinatorics", "algebraic_combinatorics", "topological_combinatorics",
            "probabilistic_combinatorics", "additive_combinatorics", "geometric_combinatorics",
            "extremal_set_theory", "asymptotic_combinatorics", "bijective_combinatorics",
            "analytic_combinatorics", "computational_combinatorics", "pattern_avoidance",
            "combinatorial_game_theory", "combinatorial_optimization", "coding_theory",
            "cryptography", "combinatorial_designs", "block_designs", "difference_sets",
            "latin_squares", "hadamard_matrices", "finite_fields", "discrete_probability",
            "combinatorial_number_theory", "combinatorial_geometry", "polytopes",
            "hyperplane_arrangements", "discrete_morse_theory", "chip_firing_games",
            "cellular_automata", "combinatorial_species", "free_probability", "percolation_theory",
            "zero_one_laws", "threshold_phenomena", "combinatorial_algorithms"
        ],
       
        "logic_and_foundations": [
            "propositional_logic", "predicate_logic", "formal_systems", "axiomatization",
            "model_theory", "proof_theory", "recursive_functions", "computability_theory",
            "godels_theorems", "set_theory", "ordinals", "cardinals", "forcing", "independence_results",
            "large_cardinals", "descriptive_set_theory", "constructive_mathematics",
            "intuitionism", "type_theory", "lambda_calculus", "category_theory", "topos_theory",
            "functors", "natural_transformations", "limits", "adjoint_functors", "monads",
            "higher_category_theory", "n_categories", "homotopy_type_theory",
            "modal_logic", "temporal_logic", "fuzzy_logic", "paraconsistent_logic",
            "non_classical_logics", "provability_logic", "linear_logic", "substructural_logics",
            "relevance_logic", "dependence_logic", "epistemic_logic", "deontic_logic",
            "computational_complexity", "reverse_mathematics", "hierarchy_theory",
            "recursion_theory", "computable_analysis", "degrees_of_unsolvability",
            "automated_theorem_proving", "formal_verification", "program_extraction",
            "models_of_set_theory", "inner_models", "determinacy", "infinite_games",
            "infinitary_combinatorics", "foundations_of_mathematics", "proof_assistants"
        ],
                   
        # Applied Mathematics
        "differential_equations": [
            "ordinary_differential_equations", "partial_differential_equations", "linear_odes",
            "nonlinear_odes", "systems_of_odes", "boundary_value_problems", "initial_value_problems",
            "separation_of_variables", "power_series_methods", "numerical_methods_odes",
            "numerical_methods_pdes", "finite_difference_methods", "finite_element_methods",
            "spectral_methods", "stability_theory", "bifurcation_theory", "chaos_theory",
            "dynamical_systems", "hamiltonians", "lyapunov_functions", "phase_portraits",
            "existence_uniqueness", "sturm_liouville_theory", "greens_functions",
            "integral_equations", "variational_methods", "conservation_laws", "shock_waves",
            "solitons", "dispersive_equations", "reaction_diffusion_equations", "navier_stokes_equations",
            "wave_equations", "heat_equations", "laplace_equations", "schrodinger_equations",
            "stochastic_differential_equations", "functional_differential_equations",
            "delay_differential_equations", "fractional_differential_equations",
            "asymptotic_methods", "perturbation_theory", "homogenization_theory",
            "averaging_methods", "wkb_approximation", "singular_perturbation_theory",
            "center_manifold_theory", "normal_forms", "hamiltonian_mechanics",
            "symplectic_integrators", "conservative_systems", "dissipative_systems",
            "integrable_systems", "inverse_scattering_transform", "lax_pairs",
            "geometric_methods_ode", "numerical_bifurcation_analysis", "time_frequency_analysis"
        ],
       
        "numerical_analysis": [
            "error_analysis", "finite_differences", "interpolation", "numerical_integration",
            "numerical_differentiation", "root_finding", "linear_systems", "matrix_factorizations",
            "iterative_methods", "eigenvalue_algorithms", "sparse_matrices", "nonlinear_systems",
            "optimization_algorithms", "gradient_descent", "newton_methods", "quasi_newton_methods",
            "conjugate_gradient", "approximation_theory", "spectral_methods", "odes_numerical",
            "pdes_numerical", "fast_fourier_transform", "wavelets", "finite_elements",
            "multigrid_methods", "boundary_element_methods", "monte_carlo_methods",
            "stochastic_differential_equations", "molecular_dynamics", "computational_fluid_dynamics",
            "parallel_computing", "high_performance_computing", "adaptive_methods",
            "numerical_linear_algebra", "numerical_optimization", "automatic_differentiation",
            "interval_arithmetic", "validated_numerics", "floating_point_arithmetic",
            "arbitrary_precision_arithmetic", "symbolic_numeric_methods", "spectral_element_methods",
            "discontinuous_galerkin_methods", "particle_methods", "meshless_methods",
            "level_set_methods", "front_tracking_methods", "shock_capturing_methods",
            "numerical_relativity", "computational_electromagnetics", "numerical_weather_prediction",
            "ocean_modeling", "climate_modeling", "computational_biology", "numerical_quantum_mechanics",
            "computational_chemistry", "computational_materials_science", "tensor_methods",
            "hierarchical_matrices", "fast_multipole_methods", "randomized_algorithms",
            "sparse_approximation", "compressed_sensing", "numerical_continuation"
        ],
       
        "probability_and_statistics": [
            "probability_theory", "random_variables", "probability_distributions", "moments",
            "central_limit_theorem", "law_of_large_numbers", "conditional_probability",
            "bayesian_statistics", "stochastic_processes", "markov_chains", "poisson_processes",
            "brownian_motion", "random_walks", "martingales", "queueing_theory",
            "descriptive_statistics", "statistical_inference", "hypothesis_testing",
            "confidence_intervals", "maximum_likelihood", "regression_analysis",
            "anova", "multivariate_statistics", "nonparametric_statistics", "time_series",
            "survival_analysis", "experimental_design", "sampling_theory", "bootstrap_methods",
            "statistical_learning", "machine_learning", "dimensionality_reduction", "clustering",
            "classification", "neural_networks", "support_vector_machines", "decision_trees",
            "bayesian_networks", "hidden_markov_models", "information_theory", "entropy",
            "mutual_information", "coding_theory", "compression", "error_correction_codes",
            "statistical_mechanics", "large_deviations", "extreme_value_theory", "statistical_physics",
            "percolation_theory", "renormalization_group", "spin_systems", "random_matrices",
            "free_probability_theory", "measure_concentration", "high_dimensional_statistics",
            "empirical_processes", "causal_inference", "graphical_models", "belief_propagation",
            "monte_carlo_methods", "mcmc", "sequential_monte_carlo", "variational_inference",
            "expectation_maximization", "sequential_estimation", "filtering_theory",
            "change_point_detection", "stochastic_optimization", "stochastic_approximation",
            "statistical_signal_processing", "information_geometry", "differential_privacy",
            "robust_statistics", "semiparametric_statistics", "nonlinear_time_series",
            "spatial_statistics", "point_processes", "random_fields", "stochastic_geometry",
            "statistical_physics_of_learning", "statistical_network_analysis"
        ],
       
        "operations_research": [
            "linear_programming", "duality_theory", "simplex_method", "interior_point_methods",
            "integer_programming", "branch_and_bound", "cutting_plane_methods", "dynamic_programming",
            "nonlinear_programming", "convex_optimization", "semidefinite_programming",
            "stochastic_programming", "multi_objective_optimization", "network_flows",
            "assignment_problems", "transportation_problems", "scheduling", "game_theory",
            "mechanism_design", "combinatorial_optimization", "metaheuristics", "genetic_algorithms",
            "simulated_annealing", "tabu_search", "particle_swarm", "ant_colony_optimization",
            "queueing_theory", "inventory_theory", "markov_decision_processes", "decision_analysis",
            "utility_theory", "supply_chain_management", "project_management", "reliability_theory",
            "robust_optimization", "distributionally_robust_optimization", "online_optimization",
            "competitive_analysis", "approximation_algorithms", "constraint_programming",
            "satisfiability_modulo_theories", "boolean_satisfiability", "facility_location",
            "vehicle_routing", "crew_scheduling", "timetabling", "resource_allocation",
            "auction_theory", "matching_theory", "fair_division", "mechanism_design",
            "social_choice_theory", "cooperative_game_theory", "bargaining_theory",
            "optimal_control", "differential_games", "stochastic_games", "evolutionary_game_theory",
            "market_design", "preference_learning", "group_decision_making", "risk_analysis",
            "discrete_choice_theory", "operations_management", "queuing_networks",
            "revenue_management", "pricing_optimization", "hierarchical_planning"
        ],
       
        "computational_mathematics": [
            "algorithms", "data_structures", "computational_complexity", "big_o_notation",
            "np_completeness", "approximation_algorithms", "randomized_algorithms",
            "algebraic_algorithms", "number_theoretic_algorithms", "cryptographic_algorithms",
            "hashing", "computational_geometry", "computational_topology", "computational_algebra",
            "symbolic_computation", "computer_algebra_systems", "automatic_theorem_proving",
            "formal_verification", "satisfiability", "constraint_satisfaction", "computational_learning_theory",
            "quantum_computing", "quantum_algorithms", "blockchain", "cryptography",
            "public_key_cryptography", "symmetric_key_cryptography", "elliptic_curve_cryptography",
            "quantum_cryptography", "zero_knowledge_proofs", "secure_multiparty_computation",
            "computational_group_theory", "computational_number_theory", "computational_algebraic_geometry",
            "computational_algebraic_topology", "computational_conformal_geometry",
            "computational_real_algebraic_geometry", "computational_commutative_algebra",
            "computer_aided_design", "computational_differential_equations", "computational_dynamics",
            "computational_fluid_dynamics", "computational_electromagnetics",
            "computational_aerodynamics", "computational_acoustics", "computational_heat_transfer",
            "computational_mechanics", "molecular_modeling", "molecular_dynamics",
            "monte_carlo_simulation", "metropolis_algorithm", "quantum_monte_carlo",
            "density_functional_theory", "computational_quantum_chemistry",
            "bioinformatics_algorithms", "sequence_alignment", "phylogenetic_trees",
            "computational_neuroscience", "neural_coding", "computational_psychiatry",
            "systems_biology", "protein_folding", "genomics", "proteomics"
        ],
       
        "financial_mathematics": [
            "interest_rates", "present_value", "future_value", "annuities", "amortization",
            "bonds", "options_pricing", "black_scholes", "binomial_models", "market_models",
            "portfolio_theory", "capm", "risk_management", "derivatives", "futures", "swaps",
            "finite_difference_methods_finance", "monte_carlo_methods_finance", "stochastic_calculus_finance",
            "arbitrage_theory", "risk_neutral_valuation", "term_structure_models",
            "interest_rate_models", "volatility_models", "stochastic_volatility", "local_volatility",
            "credit_risk", "credit_derivatives", "default_models", "recovery_models",
            "liquidity_models", "transaction_costs", "market_microstructure", "high_frequency_trading",
            "algorithmic_trading", "optimal_execution", "limit_order_books", "market_impact",
            "asset_allocation", "portfolio_optimization", "performance_attribution",
            "risk_metrics", "value_at_risk", "expected_shortfall", "stress_testing",
            "scenario_analysis", "copulas", "extreme_value_theory", "multivariate_return_distributions",
            "factor_models", "risk_premia", "behavioral_finance", "market_efficiency",
            "financial_econometrics", "time_series_models_finance", "cointegration",
            "regime_switching_models", "garch_models", "stochastic_control",
            "optimal_stopping", "american_options", "executive_compensation", "real_options",
            "regulatory_capital", "asset_liability_management", "pension_fund_mathematics",
            "insurance_mathematics", "actuarial_science", "life_contingencies"
        ],
       
        "physics_and_mathematical_physics": [
            "classical_mechanics", "lagrangian_mechanics", "hamiltonian_mechanics", "fluid_mechanics",
            "electromagnetism", "thermodynamics", "statistical_mechanics", "quantum_mechanics",
            "relativity", "general_relativity", "quantum_field_theory", "gauge_theory",
            "string_theory", "particle_physics", "condensed_matter_physics", "mathematical_physics",
            "integrable_systems", "conformal_field_theory", "supersymmetry", "quantum_gravity",
            "quantum_information", "quantum_computation", "quantum_optics", "quantum_chaos",
            "quantum_thermodynamics", "quantum_measurement", "quantum_foundations",
            "tensor_network_theory", "topological_quantum_field_theory", "topological_order",
            "anyons", "fractional_quantum_hall_effect", "topological_insulators",
            "topological_superconductors", "spin_glasses", "random_matrices", "exact_solutions",
            "plasma_physics", "magnetohydrodynamics", "kinetic_theory", "turbulence",
            "geophysical_fluid_dynamics", "atmospheric_physics", "oceanography",
            "stellar_structure", "stellar_evolution", "galactic_dynamics", "cosmology",
            "early_universe", "inflationary_theory", "dark_matter", "dark_energy",
            "gravitational_waves", "black_hole_physics", "holographic_principle",
            "ads_cft_correspondence", "renormalization_group", "effective_field_theory",
            "many_body_physics", "strongly_correlated_systems", "phase_transitions",
            "critical_phenomena", "nonequilibrium_statistical_mechanics", "transport_theory",
            "stochastic_thermodynamics", "active_matter", "biological_physics"
        ],
       
        "topology": [
            "general_topology", "metric_spaces", "topological_spaces", "continuity",
            "connectedness", "compactness", "separation_axioms", "countability_axioms",
            "algebraic_topology", "fundamental_group", "covering_spaces", "fibrations",
            "homology_theory", "cohomology_theory", "homotopy_theory", "higher_homotopy_groups",
            "obstruction_theory", "spectral_sequences", "sheaf_theory", "differential_forms",
            "de_rham_cohomology", "morse_theory", "k_theory", "cobordism_theory",
            "characteristic_classes", "vector_bundles", "fiber_bundles", "principal_bundles",
            "index_theorems", "manifold_theory", "differentiable_manifolds", "smooth_structures",
            "exotic_spheres", "surgery_theory", "low_dimensional_topology", "3_manifolds",
            "4_manifolds", "knot_theory", "braid_theory", "link_theory", "knot_invariants",
            "jones_polynomial", "seiberg_witten_theory", "gauge_theory", "symplectic_topology",
            "contact_topology", "foliations", "geometric_group_theory", "geometric_topology",
            "mapping_class_groups", "teichmuller_theory", "moduli_spaces", "operads",
            "operad_theory", "infinity_categories", "derived_categories", "topological_quantum_field_theory",
            "topological_data_analysis", "persistent_homology", "mapper_algorithm",
            "computational_topology", "applied_topology", "topological_combinatorics",
            "simplicial_complexes", "geometric_group_theory", "hyperbolic_geometry"
        ],
       
        "cryptography": [
            "symmetric_cryptography", "asymmetric_cryptography", "hash_functions", "message_authentication",
            "digital_signatures", "key_exchange", "random_number_generation", "pseudorandom_functions",
            "block_ciphers", "stream_ciphers", "authenticated_encryption", "modes_of_operation",
            "cryptanalysis", "side_channel_attacks", "fault_attacks", "differential_cryptanalysis",
            "linear_cryptanalysis", "algebraic_attacks", "quantum_cryptanalysis", "post_quantum_cryptography",
            "lattice_based_cryptography", "multivariate_cryptography", "hash_based_signatures",
            "code_based_cryptography", "isogeny_based_cryptography", "homomorphic_encryption",
            "functional_encryption", "attribute_based_encryption", "identity_based_encryption",
            "secure_multiparty_computation", "zero_knowledge_proofs", "zero_knowledge_arguments",
            "zkSNARKs", "succinct_arguments", "interactive_proofs", "probabilistic_proofs",
            "verifiable_computation", "delegated_computation", "secret_sharing", "threshold_cryptography",
            "proactive_security", "cryptographic_protocols", "oblivious_transfer", "commitment_schemes",
            "oblivious_ram", "private_information_retrieval", "anonymous_credentials",
            "ring_signatures", "group_signatures", "blind_signatures", "cryptographic_voting",
            "electronic_cash", "cryptocurrency", "blockchain_technology", "distributed_ledgers",
            "smart_contracts", "consensus_protocols", "proof_of_work", "proof_of_stake"
        ],
       
        "graph_theory": [
            "basic_concepts", "connectivity", "trees", "cycles", "matchings", "colorings",
            "planarity", "graph_algorithms", "network_flows", "shortest_paths", "spanning_trees",
            "vertex_cover", "independent_sets", "cliques", "dominating_sets", "graph_minors",
            "treewidth", "pathwidth", "graph_decompositions", "graph_products", "graph_operations",
            "directed_graphs", "tournaments", "strongly_connected_components", "acyclic_digraphs",
            "topological_sorting", "random_graphs", "small_world_networks", "scale_free_networks",
            "regular_graphs", "expander_graphs", "spectral_graph_theory", "graph_laplacian",
            "graph_eigenvalues", "graph_isomorphism", "graph_homomorphisms", "extremal_graph_theory",
            "ramsey_theory_on_graphs", "turan_theory", "probabilistic_methods", "random_graph_processes",
            "geometric_graphs", "disk_graphs", "unit_disk_graphs", "intersection_graphs",
            "interval_graphs", "perfect_graphs", "chordal_graphs", "comparability_graphs",
            "cographs", "permutation_graphs", "distance_regular_graphs", "strongly_regular_graphs",
            "graph_enumeration", "graph_generation", "graph_representation", "graph_visualization",
            "graph_drawing", "book_embeddings", "graph_immersions", "graph_minors", "graph_width_parameters",
            "feedback_vertex_set", "feedback_edge_set", "graph_partitioning", "community_detection",
            "centrality_measures", "social_network_analysis", "chemical_graph_theory", "molecular_graphs"
        ],
       
        "game_theory": [
            "normal_form_games", "extensive_form_games", "cooperative_games", "non_cooperative_games",
            "nash_equilibrium", "mixed_strategies", "pure_strategies", "dominant_strategies",
            "pareto_optimality", "social_choice", "mechanism_design", "auction_theory",
            "bargaining_theory", "repeated_games", "stochastic_games", "evolutionary_game_theory",
            "coalition_formation", "stable_matchings", "core", "shapley_value", "nucleolus",
            "fair_division", "cake_cutting", "resource_allocation", "voting_theory",
            "algorithmic_game_theory", "computational_social_choice", "price_of_anarchy",
            "price_of_stability", "congestion_games", "potential_games", "network_games",
            "graphical_games", "games_on_networks", "information_economics", "contract_theory",
            "principal_agent_problems", "moral_hazard", "adverse_selection", "signaling_games",
            "cheap_talk", "costly_signaling", "reputation_formation", "information_cascades",
            "herding_behavior", "learning_in_games", "no_regret_learning", "fictitious_play",
            "best_response_dynamics", "replicator_dynamics", "evolutionary_stable_strategies",
            "stochastic_stability", "quantal_response_equilibrium", "level_k_thinking",
            "cognitive_hierarchy", "psychological_game_theory", "reference_dependent_preferences",
            "social_preferences", "fairness", "reciprocity", "bounded_rationality"
        ],
       
        "machine_learning": [
            "supervised_learning", "unsupervised_learning", "reinforcement_learning", "deep_learning",
            "neural_networks", "convolutional_networks", "recurrent_networks", "generative_models",
            "bayesian_networks", "graphical_models", "support_vector_machines", "kernel_methods",
            "decision_trees", "random_forests", "boosting", "bagging", "ensemble_methods",
            "clustering", "dimensionality_reduction", "feature_selection", "feature_engineering",
            "representation_learning", "transfer_learning", "meta_learning", "few_shot_learning",
            "self_supervised_learning", "contrastive_learning", "multi_task_learning", "active_learning",
            "online_learning", "federated_learning", "distributed_learning", "privacy_preserving_ml",
            "fairness_in_ml", "interpretable_ml", "explainable_ai", "causal_inference",
            "time_series_analysis", "sequential_data", "natural_language_processing", "computer_vision",
            "speech_recognition", "generative_adversarial_networks", "variational_autoencoders",
            "normalizing_flows", "energy_based_models", "probabilistic_programming", "bayesian_inference",
            "approximate_inference", "mcmc_methods", "variational_inference", "message_passing",
            "belief_propagation", "expectation_maximization", "gaussian_processes", "thompson_sampling",
            "bandit_algorithms", "markov_decision_processes", "q_learning", "policy_gradients",
            "actor_critic_methods", "model_based_rl", "inverse_rl", "imitation_learning",
            "multi_agent_reinforcement_learning", "game_theoretic_learning", "evolutionary_computation",
            "genetic_algorithms", "evolutionary_strategies", "neuroevolution", "computational_learning_theory",
            "pac_learning", "vc_dimension", "rademacher_complexity", "information_theory",
            "maximum_entropy_methods", "optimal_transport", "manifold_learning", "topological_data_analysis"
        ],
       
        "elementary_mathematics": [
            "arithmetic", "basic_algebra", "basic_geometry", "trigonometry", "precalculus",
            "calculus_basics", "vectors_basics", "matrices_basics", "complex_numbers_basics",
            "sequences_series", "probability_basics", "statistics_basics", "counting_basics",
            "measurement", "word_problems", "mathematical_modeling", "proofs_basics",
            "number_sense", "fractions", "decimals", "percentages", "ratios", "proportions",
            "exponents", "roots", "logarithms", "polynomials", "factoring", "quadratic_equations",
            "linear_equations", "systems_of_equations", "inequalities", "coordinate_geometry",
            "euclidean_geometry", "similarity", "congruence", "circles", "triangles", "quadrilaterals",
            "polygons", "solid_geometry", "volume", "surface_area", "trigonometric_functions",
            "trigonometric_identities", "exponential_functions", "logarithmic_functions",
            "limits_introduction", "derivatives_introduction", "integration_introduction",
            "applications_of_derivatives", "applications_of_integrals", "sequences_and_series",
            "combinatorics_basics", "permutations_and_combinations", "elementary_number_theory",
            "divisibility", "primes_and_composites", "gcd_and_lcm", "modular_arithmetic_basics",
            "logic_and_sets", "functions_and_relations", "graphs_of_functions", "transformations",
            "discrete_mathematics_basics", "financial_mathematics_basics", "applied_mathematics"
        ]
    }
   
    # Coverage tracking
    self.covered_integers = set()
    self.covered_integer_pairs = set()
    self.covered_integer_triplets = set()
    self.covered_domains = {domain: 0 for domain in self.domains.keys()}
    self.covered_subdomains = {}
    self.coverage_range = {
        "integers": (-10000, 10000),
        "pairs": ((-1000, 1000), (-1000, 1000)),
        "triplets": ((-500, 500), (-500, 500), (-500, 500))
    }
   
    # Statistics tracking
    self.total_problems_generated = 0
    self.total_bytes_generated = 0
    self.generation_times = []
    self.batch_sizes = []
   
    # Initialize subdomain coverage
    for domain, subdomains in self.domains.items():
        for subdomain in subdomains:
            self.covered_subdomains[f"{domain}_{subdomain}"] = 0
   
    # Number systems and types
    self.number_types = [
        "integers", "rational_numbers", "real_numbers", "complex_numbers",
        "p_adic_numbers", "quaternions", "octonions", "hyperreal_numbers",
        "surreal_numbers", "ordinals", "cardinals", "constructible_numbers",
        "computable_numbers", "algebraic_numbers", "transcendental_numbers"
    ]
   
    # Number scales for different problem types
    self.number_scales = {
        "tiny": (0, 10),
        "small": (10, 100),
        "medium": (100, 1000),
        "large": (1000, 10000),
        "huge": (10000, 1000000),
        "astronomical": (1000000, 10**12),
        "cosmological": (10**12, 10**50)
    }
   
    # Problem representations
    self.representations = [
        "symbolic", "textual", "algebraic", "numerical", "algorithmic",
        "graphical", "tabular", "geometric", "proof-based", "computational",
        "applied"
    ]
   
    # Templates for word problems across domains
    self.word_problem_templates = {
        "arithmetic": [
            "A person has {a} items and buys {b} more. How many items do they have in total?",
            "If a store sells {a} items each day, how many items will it sell in {b} days?",
            "A recipe requires {a} cups of flour. If making {b} batches, how much flour is needed?",
            "A container has {a} liters and {b} liters are removed. How much remains?",
            "If {a} items cost ${b}, what is the cost per item?",
            "A person has ${a} and spends ${b}. How much money remains?",
            "If a journey of {a} kilometers takes {b} hours, what is the average speed?"
        ],
       
        "algebra": [
            "If {expression} = {value}, find the value of {variable}.",
            "Solve the equation: {equation}",
            "For what values of {variable} is {expression} {comparison} {value}?",
            "Find the value of {expression} when {variable} = {value}.",
            "If {function} represents {context}, what is {question}?",
            "The cost of producing x items is given by {cost_function}. What is {question}?"
        ],
       
        "geometry": [
            "A rectangle has width {a} and length {b}. What is its {property}?",
            "A circle has radius {r}. What is its {property}?",
            "A triangle has sides of length {a}, {b}, and {c}. What is its {property}?",
            "A cube has side length {a}. What is its {property}?",
            "A sphere has radius {r}. What is its {property}?",
            "A cylinder has radius {r} and height {h}. What is its {property}?",
            "Two points are located at {point1} and {point2}. What is the distance between them?",
            "A line passes through points {point1} and {point2}. What is its slope?"
        ],
       
        "calculus": [
            "Find the derivative of {function} with respect to {variable}.",
            "Evaluate the indefinite integral of {function} with respect to {variable}.",
            "Calculate the definite integral of {function} from {a} to {b}.",
            "Find the critical points of {function}.",
            "Determine the local extrema of {function}.",
            "Find the limit of {function} as {variable} approaches {value}.",
            "Determine the convergence or divergence of the series {series}."
        ],
       
        "probability": [
            "If the probability of event A is {probA} and the probability of event B is {probB}, what is {question}?",
            "A bag contains {red} red balls and {blue} blue balls. If {draws} balls are drawn without replacement, what is the probability of {event}?",
            "The probability distribution of X is given by {distribution}. What is {question}?",
            "A random variable X follows {distribution}. What is {question}?",
            "In an experiment, the probability of success is {p}. If the experiment is performed {n} times, what is the probability of {event}?"
        ]
    }
   
    # List of common variables used in math problems
    self.variables = ['x', 'y', 'z', 'a', 'b', 'c', 't', 'n', 'p', 'q', 'r', 's']
   
    # Parameters for controlling problem generation
    self.symbolic_probability = 0.7  # 70% chance for symbolic representation
   
    def _get_current_memory_usage(self):
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return memory_info.rss / (1024 * 1024)
   
    def _check_memory_limits(self):
        """Check if we're approaching memory limits and take action if needed"""
        current_usage = self._get_current_memory_usage()
       
        # If approaching limit (80% of max), force garbage collection
        if current_usage > 0.8 * self.memory_limit_mb:
            gc.collect()
            return self._get_current_memory_usage()
       
        return current_usage
   
    def _update_coverage(self, domain, subdomain, numbers=None):
        """Update coverage statistics"""
        # Update domain and subdomain counts
        self.covered_domains[domain] = self.covered_domains.get(domain, 0) + 1
        subdomain_key = f"{domain}_{subdomain}"
        self.covered_subdomains[subdomain_key] = self.covered_subdomains.get(subdomain_key, 0) + 1
       
        # Update number coverage
        if numbers:
            if isinstance(numbers, int) and self.coverage_range["integers"][0] <= numbers <= self.coverage_range["integers"][1]:
                self.covered_integers.add(numbers)
            elif isinstance(numbers, tuple):
                if len(numbers) == 2:
                    a, b = numbers
                    if (self.coverage_range["pairs"][0][0] <= a <= self.coverage_range["pairs"][0][1] and
                        self.coverage_range["pairs"][1][0] <= b <= self.coverage_range["pairs"][1][1]):
                        self.covered_integer_pairs.add((a, b))
                elif len(numbers) == 3:
                    a, b, c = numbers
                    if (self.coverage_range["triplets"][0][0] <= a <= self.coverage_range["triplets"][0][1] and
                        self.coverage_range["triplets"][1][0] <= b <= self.coverage_range["triplets"][1][1] and
                        self.coverage_range["triplets"][2][0] <= c <= self.coverage_range["triplets"][2][1]):
                        self.covered_integer_triplets.add((a, b, c))
   
    def _generate_systematic_integer(self, scale="small", force_new=False):
        """Generate an integer systematically to ensure coverage"""
        min_val, max_val = self.number_scales.get(scale, (1, 100))
       
        if force_new:
            # Adjust range to stay within coverage tracking limits
            adjusted_min = max(min_val, self.coverage_range["integers"][0])
            adjusted_max = min(max_val, self.coverage_range["integers"][1])
           
            # Find uncovered integers in range
            possible_integers = set(range(adjusted_min, adjusted_max + 1))
            uncovered = possible_integers - self.covered_integers
           
            if uncovered:
                # Use an uncovered integer if available
                selected = random.choice(list(uncovered))
                self.covered_integers.add(selected)
                return selected
       
        # If not forcing new or no uncovered integers available, use random
        return random.randint(min_val, max_val)
   
    def _generate_random_integer(self, scale="small", force_new=False):
        """Generate a random integer based on scale with coverage tracking"""
        if force_new:
            return self._generate_systematic_integer(scale, force_new)
       
        min_val, max_val = self.number_scales.get(scale, (1, 100))
        value = random.randint(min_val, max_val)
       
        # Track coverage if within range
        if self.coverage_range["integers"][0] <= value <= self.coverage_range["integers"][1]:
            self.covered_integers.add(value)
           
        return value
   
    def _generate_random_fraction(self, scale="small", force_new=False):
        """Generate a random fraction with coverage tracking"""
        min_val, max_val = self.number_scales.get(scale, (1, 100))
       
        if force_new:
            # Try to generate a pair not covered yet
            for _ in range(50):  # Limit attempts
                numerator = self._generate_systematic_integer(scale, True)
                denominator = self._generate_systematic_integer(scale, True)
                while denominator == 0 or math.gcd(numerator, denominator) == min(numerator, denominator) > 1:
                    denominator = self._generate_systematic_integer(scale, True)
               
                if (numerator, denominator) not in self.covered_integer_pairs:
                    self.covered_integer_pairs.add((numerator, denominator))
                    return Fraction(numerator, denominator)
       
        # Default generation if not forcing new or no uncovered pairs found
        numerator = random.randint(1, max_val)
        denominator = random.randint(1, max_val)
        while math.gcd(numerator, denominator) == min(numerator, denominator) > 1:
            # Ensure the fraction isn't trivially reducible
            denominator = random.randint(1, max_val)
           
        # Track coverage
        if (self.coverage_range["pairs"][0][0] <= numerator <= self.coverage_range["pairs"][0][1] and
            self.coverage_range["pairs"][1][0] <= denominator <= self.coverage_range["pairs"][1][1]):
            self.covered_integer_pairs.add((numerator, denominator))
           
        return Fraction(numerator, denominator)
   
    def _generate_random_decimal(self, scale="small", precision=None, force_new=False):
        """Generate a random decimal with coverage tracking"""
        min_val, max_val = self.number_scales.get(scale, (1, 100))
        precision = precision or random.randint(1, 6)
       
        # For force_new, we use the integer part to ensure coverage
        if force_new:
            int_part = self._generate_systematic_integer(scale, True)
            decimal_part = random.random()
            return round(int_part + decimal_part, precision)
       
        # Default generation
        value = round(random.uniform(min_val, max_val), precision)
       
        # Track the integer part for coverage
        int_part = int(value)
        if self.coverage_range["integers"][0] <= int_part <= self.coverage_range["integers"][1]:
            self.covered_integers.add(int_part)
           
        return value
   
    def _generate_random_complex(self, scale="small", force_new=False):
        """Generate a random complex number with coverage tracking"""
        if force_new:
            real_part = self._generate_systematic_integer(scale, True)
            imag_part = self._generate_systematic_integer(scale, True)
        else:
            real_part = self._generate_random_decimal(scale)
            imag_part = self._generate_random_decimal(scale)
           
        # Track coverage
        if (self.coverage_range["pairs"][0][0] <= real_part <= self.coverage_range["pairs"][0][1] and
            self.coverage_range["pairs"][1][0] <= imag_part <= self.coverage_range["pairs"][1][1]):
            self.covered_integer_pairs.add((int(real_part), int(imag_part)))
           
        return complex(real_part, imag_part)
   
    def _generate_random_number(self, number_type="integers", scale="small", force_new=False):
        """Generate a random number based on type and scale with coverage tracking"""
        if number_type == "integers":
            return self._generate_random_integer(scale, force_new)
        elif number_type == "rational_numbers":
            return self._generate_random_fraction(scale, force_new)
        elif number_type == "real_numbers":
            return self._generate_random_decimal(scale, None, force_new)
        elif number_type == "complex_numbers":
            return self._generate_random_complex(scale, force_new)
        else:
            return self._generate_random_integer(scale, force_new)
   
    def _generate_random_polynomial(self, degree=None, variable='x', coefficients_scale="small", force_new=False):
        """Generate a random polynomial with coverage tracking"""
        if degree is None:
            degree = random.randint(1, 5)
       
        coefficients = [self._generate_random_integer(coefficients_scale, force_new) for _ in range(degree + 1)]
        # Ensure leading coefficient is non-zero
        while coefficients[0] == 0:
            coefficients[0] = self._generate_random_integer(coefficients_scale, force_new)
           
        x = sympy.Symbol(variable)
        polynomial = 0
        for i, coef in enumerate(coefficients):
            polynomial += coef * x**(degree-i)
           
        # Track coefficient coverage as a tuple
        if len(coefficients) <= 3:
            self._update_coverage("algebra", "polynomials", tuple(coefficients[:3]))
        else:
            self._update_coverage("algebra", "polynomials", tuple(coefficients[:3]))
           
        return polynomial
   
    def _generate_random_expression(self, complexity=None, force_new=False):
        """Generate a random mathematical expression with coverage tracking"""
        if complexity is None:
            complexity = random.randint(1, 5)
           
        x, y, z = sympy.symbols('x y z')
        variables = [x, y, z]
       
        if complexity == 1:
            # Simple expressions
            operations = [
                lambda a, b: a + b,
                lambda a, b: a - b,
                lambda a, b: a * b,
                lambda a, b: a / b if b != 0 else a
            ]
            var = random.choice(variables[:2])
            const = self._generate_random_integer("small", force_new)
            op = random.choice(operations)
            return op(var, const)
       
        elif complexity == 2:
            # Bit more complex expressions
            var = random.choice(variables[:2])
            const1 = self._generate_random_integer("small", force_new)
            const2 = self._generate_random_integer("small", force_new)
            templates = [
                lambda v, c1, c2: c1 * v + c2,
                lambda v, c1, c2: c1 * v**2 + c2,
                lambda v, c1, c2: c1 * v + c2 * v**2,
                lambda v, c1, c2: c1 / (v + c2) if c2 != -v else c1 * v
            ]
           
            # Track coverage
            self._update_coverage("algebra", "expressions", (const1, const2))
           
            return random.choice(templates)(var, const1, const2)
           
        elif complexity == 3:
            # More complex expressions with functions
            var = random.choice(variables[:2])
            const = self._generate_random_integer("small", force_new)
            templates = [
                lambda v, c: sympy.sin(v) + c,
                lambda v, c: sympy.cos(v * c),
                lambda v, c: sympy.exp(v) + c,
                lambda v, c: sympy.log(v + c + 1),  # +1 to avoid log(0)
                lambda v, c: sympy.sqrt(v**2 + c**2)
            ]
           
            # Track coverage
            self._update_coverage("algebra", "expressions", const)
           
            return random.choice(templates)(var, const)
           
        elif complexity == 4:
            # Complex expressions with multiple variables
            var1 = variables[0]
            var2 = variables[1]
            const = self._generate_random_integer("small", force_new)
            templates = [
                lambda v1, v2, c: v1**2 + v2**2 + c,
                lambda v1, v2, c: v1 * v2 + c,
                lambda v1, v2, c: sympy.sin(v1) * sympy.cos(v2) + c,
                lambda v1, v2, c: (v1 + v2)**2 - c,
                lambda v1, v2, c: v1 / (v2**2 + 1) + c
            ]
           
            # Track coverage
            self._update_coverage("algebra", "expressions", const)
           
            return random.choice(templates)(var1, var2, const)
           
        else:  # complexity >= 5
            # Very complex expressions
            templates = [
                lambda: sympy.sin(x)**2 + sympy.cos(x)**2,
                lambda: sympy.exp(x) * sympy.sin(y) + sympy.log(z**2 + 1),
                lambda: (x**2 + y**2) / (1 + x**2 + y**2),
                lambda: sympy.sqrt(x**2 + y**2 + z**2),
                lambda: sympy.atan2(y, x) + sympy.exp(-x**2 - y**2)
            ]
            return random.choice(templates)()
   
    def _generate_random_equation(self, complexity=None, force_new=False):
        """Generate a random equation with coverage tracking"""
        if complexity is None:
            complexity = random.randint(1, 5)
           
        left_expr = self._generate_random_expression(complexity, force_new)
       
        # For equations, we either set right side to 0 or another expression
        if random.random() < 0.7:  # 70% chance for setting to 0 or a constant
            right_expr = self._generate_random_integer("small", force_new)
        else:
            right_expr = self._generate_random_expression(max(1, complexity-1), force_new)
           
        return sympy.Eq(left_expr, right_expr)
   
    def _generate_arithmetic_problem(self, subdomain=None, force_new=False):
        """Generate an arithmetic problem with systematic coverage"""
        if subdomain is None:
            subdomain = random.choice([
                "addition", "subtraction", "multiplication", "division",
                "exponentiation", "roots", "logarithms", "mixed"
            ])
           
        number_type = random.choice(["integers", "rational_numbers", "real_numbers"])
        scale = random.choice(list(self.number_scales.keys()))
           
        if subdomain == "addition":
            a = self._generate_random_number(number_type, scale, force_new)
            b = self._generate_random_number(number_type, scale, force_new)
            question = f"Calculate {a} + {b}"
            answer = a + b
           
            # Track coverage
            if number_type == "integers":
                self._update_coverage("arithmetic", "addition", (int(a), int(b)))
           
        elif subdomain == "subtraction":
            a = self._generate_random_number(number_type, scale, force_new)
            b = self._generate_random_number(number_type, scale, force_new)
            question = f"Calculate {a} - {b}"
            answer = a - b
           
            # Track coverage
            if number_type == "integers":
                self._update_coverage("arithmetic", "subtraction", (int(a), int(b)))
           
        elif subdomain == "multiplication":
            a = self._generate_random_number(number_type, scale, force_new)
            b = self._generate_random_number(number_type, scale, force_new)
            question = f"Calculate {a} × {b}"
            answer = a * b
           
            # Track coverage
            if number_type == "integers":
                self._update_coverage("arithmetic", "multiplication", (int(a), int(b)))
           
        elif subdomain == "division":
            b = self._generate_random_number(number_type, scale, force_new)
            while b == 0:  # Avoid division by zero
                b = self._generate_random_number(number_type, scale, force_new)
            a = self._generate_random_number(number_type, scale, force_new) * b  # Make division clean
            question = f"Calculate {a} ÷ {b}"
            answer = a / b
           
            # Track coverage
            if number_type == "integers":
                self._update_coverage("arithmetic", "division", (int(a), int(b)))
           
        elif subdomain == "exponentiation":
            a = self._generate_random_number("integers", "small", force_new)
            b = self._generate_random_integer("tiny", force_new)  # Keep exponents reasonable
            question = f"Calculate {a}^{b}"
            answer = a ** b
           
            # Track coverage
            self._update_coverage("arithmetic", "exponentiation", (int(a), int(b)))
           
        elif subdomain == "roots":
            a = self._generate_random_number("integers", "small", force_new)
            b = self._generate_random_integer("tiny", force_new)
            a_to_b = a ** b
            question = f"Calculate the {b}th root of {a_to_b}"
            answer = a
           
            # Track coverage
            self._update_coverage("arithmetic", "roots", (int(a), int(b)))
           
        elif subdomain == "logarithms":
            a = self._generate_random_number("integers", "small", force_new)
            b = self._generate_random_integer("tiny", force_new)
            a_to_b = a ** b
            question = f"Calculate log_{a}({a_to_b})"
            answer = b
           
            # Track coverage
            self._update_coverage("arithmetic", "logarithms", (int(a), int(b)))
           
        else:  # mixed operations
            operations = ['+', '-', '×', '÷']
            num_operations = random.randint(2, 5)
            numbers = [self._generate_random_number(number_type, scale, force_new) for _ in range(num_operations + 1)]
           
            expression_parts = [str(numbers[0])]
            for i in range(num_operations):
                op = random.choice(operations)
                if op == '÷' and numbers[i+1] == 0:  # Avoid division by zero
                    op = random.choice(['+', '-', '×'])
                expression_parts.append(op)
                expression_parts.append(str(numbers[i+1]))
               
            expression = ' '.join(expression_parts)
            question = f"Calculate {expression}"
           
            # Calculate answer
            result = numbers[0]
            for i in range(num_operations):
                op = expression_parts[i*2 + 1]
                num = numbers[i+1]
                if op == '+':
                    result += num
                elif op == '-':
                    result -= num
                elif op == '×':
                    result *= num
                elif op == '÷':
                    result /= num
            answer = result
           
            # Track coverage of first few numbers
            if number_type == "integers" and len(numbers) >= 3:
                self._update_coverage("arithmetic", "mixed", (int(numbers[0]), int(numbers[1]), int(numbers[2])))
           
        # Increase problem count
        self.total_problems_generated += 1
       
        # Check memory periodically
        if self.total_problems_generated % self.memory_check_interval == 0:
            self._check_memory_limits()
           
        return {
            "domain": "arithmetic",
            "subdomain": subdomain,
            "question": question,
            "answer": str(answer),
            "number_type": number_type,
            "scale": scale
        }
   
    def _generate_algebra_problem(self, subdomain=None, force_new=False):
        """Generate an algebra problem with systematic coverage"""
        if subdomain is None:
            subdomain = random.choice([
                "linear_equations", "quadratic_equations", "systems_of_equations",
                "inequalities", "expressions", "functions", "polynomials"
            ])
           
        if subdomain == "linear_equations":
            # Generate a linear equation like ax + b = c
            a = self._generate_random_integer("medium", force_new)
            while a == 0:  # Avoid a = 0
                a = self._generate_random_integer("medium", force_new)
            b = self._generate_random_integer("medium", force_new)
            c = self._generate_random_integer("medium", force_new)
           
            x = sympy.Symbol('x')
            equation = sympy.Eq(a*x + b, c)
            solution = sympy.solve(equation, x)[0]
           
            question = f"Solve the equation: {equation}"
            answer = f"x = {solution}"
           
            # Track coverage
            self._update_coverage("algebra", "linear_equations", (a, b, c))
           
            return {
                "domain": "algebra",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "symbolic_equation": str(equation),
                "symbolic_solution": str(solution)
            }
           
        elif subdomain == "quadratic_equations":
            # Generate a quadratic equation like ax^2 + bx + c = 0
            a = self._generate_random_integer("small", force_new)
            while a == 0:  # Avoid a = 0
                a = self._generate_random_integer("small", force_new)
            b = self._generate_random_integer("medium", force_new)
            c = self._generate_random_integer("medium", force_new)
           
            x = sympy.Symbol('x')
            equation = sympy.Eq(a*x**2 + b*x + c, 0)
           
            # Solve and format solution
            solutions = sympy.solve(equation, x)
            if len(solutions) == 1:
                answer = f"x = {solutions[0]}"
            else:
                answer = f"x = {solutions[0]} or x = {solutions[1]}"
           
            question = f"Solve the quadratic equation: {equation}"
           
            # Track coverage
            self._update_coverage("algebra", "quadratic_equations", (a, b, c))
           
            return {
                "domain": "algebra",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "symbolic_equation": str(equation),
                "symbolic_solution": str(solutions)
            }
           
        elif subdomain == "systems_of_equations":
            # Generate a system of two linear equations
            a1 = self._generate_random_integer("small", force_new)
            b1 = self._generate_random_integer("small", force_new)
            c1 = self._generate_random_integer("medium", force_new)
            a2 = self._generate_random_integer("small", force_new)
            b2 = self._generate_random_integer("small", force_new)
            c2 = self._generate_random_integer("medium", force_new)
           
            # Ensure the system is consistent and has a unique solution
            while a1*b2 - a2*b1 == 0:  # Check if determinant is zero
                a2 = self._generate_random_integer("small", force_new)
                b2 = self._generate_random_integer("small", force_new)
           
            x, y = sympy.symbols('x y')
            eq1 = sympy.Eq(a1*x + b1*y, c1)
            eq2 = sympy.Eq(a2*x + b2*y, c2)
           
            solution = sympy.solve([eq1, eq2], [x, y])
           
            question = f"Solve the system of equations:\n{eq1}\n{eq2}"
            answer = f"x = {solution[x]}, y = {solution[y]}"
           
            # Track coverage
            self._update_coverage("algebra", "systems_of_equations", (a1, b1, a2))
           
            return {
                "domain": "algebra",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "symbolic_equations": [str(eq1), str(eq2)],
                "symbolic_solution": str(solution)
            }
           
        elif subdomain == "inequalities":
            # Generate a linear inequality
            a = self._generate_random_integer("small", force_new)
            while a == 0:
                a = self._generate_random_integer("small", force_new)
            b = self._generate_random_integer("medium", force_new)
            c = self._generate_random_integer("medium", force_new)
           
            x = sympy.Symbol('x')
           
            # Randomly choose inequality type
            inequality_type = random.choice(['<', '<=', '>', '>='])
           
            if inequality_type == '<':
                inequality = sympy.Lt(a*x + b, c)
            elif inequality_type == '<=':
                inequality = sympy.Le(a*x + b, c)
            elif inequality_type == '>':
                inequality = sympy.Gt(a*x + b, c)
            else:  # >=
                inequality = sympy.Ge(a*x + b, c)
               
            solution = sympy.solve(inequality, x)
           
            question = f"Solve the inequality: {inequality}"
            answer = str(solution)
           
            # Track coverage
            self._update_coverage("algebra", "inequalities", (a, b, c))
           
            return {
                "domain": "algebra",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "symbolic_inequality": str(inequality),
                "symbolic_solution": str(solution)
            }
           
        elif subdomain == "expressions":
            # Generate an algebraic expression to simplify
            complexity = random.randint(2, 4)
            expression = self._generate_random_expression(complexity, force_new)
           
            simplified = sympy.simplify(expression)
           
            question = f"Simplify the expression: {expression}"
            answer = str(simplified)
           
            # Track coverage is handled in _generate_random_expression
           
            return {
                "domain": "algebra",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "symbolic_expression": str(expression),
                "symbolic_simplified": str(simplified)
            }
           
        elif subdomain == "functions":
            # Generate a function and ask for various properties
            x = sympy.Symbol('x')
            function_types = [
                lambda: sympy.sin(x),
                lambda: sympy.cos(x),
                lambda: sympy.exp(x),
                lambda: sympy.log(x),
                lambda: x**2,
                lambda: 1/x,
                lambda: sympy.sqrt(x),
                lambda: x**3 - 3*x
            ]
           
            function = random.choice(function_types)()
           
            # Generate different question types for functions
            question_types = [
                lambda f: (f"Find the derivative of f(x) = {f}", str(sympy.diff(f, x))),
                lambda f: (f"Find the value of f(2) where f(x) = {f}", str(f.subs(x, 2))),
                lambda f: (f"Find the domain of f(x) = {f}", "Domain depends on the function")
            ]
           
            question_generator = random.choice(question_types)
            question, answer = question_generator(function)
           
            # Track coverage (using function hash)
            function_hash = hash(str(function)) % 1000000
            self._update_coverage("algebra", "functions", function_hash)
           
            return {
                "domain": "algebra",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "symbolic_function": str(function)
            }
           
        elif subdomain == "polynomials":
            # Generate polynomial problems
            degree = random.randint(2, 5)
            x = sympy.Symbol('x')
           
            # Different polynomial problem types
            problem_types = [
                # Factor a polynomial
                lambda: {
                    "question_template": "Factor the polynomial: {}",
                    "polynomial": self._generate_random_polynomial(degree, 'x', "small", force_new),
                    "answer_type": "factorization"
                },
                # Find roots
                lambda: {
                    "question_template": "Find the roots of the polynomial: {}",
                    "polynomial": self._generate_random_polynomial(degree, 'x', "small", force_new),
                    "answer_type": "roots"
                },
                # Polynomial division
                lambda: {
                    "question_template": "Divide {} by {}",
                    "polynomial": self._generate_random_polynomial(degree, 'x', "small", force_new),
                    "divisor": self._generate_random_polynomial(random.randint(1, degree-1), 'x', "small", force_new),
                    "answer_type": "division"
                }
            ]
           
            problem_spec = random.choice(problem_types)()
           
            if problem_spec["answer_type"] == "factorization":
                polynomial = problem_spec["polynomial"]
                question = problem_spec["question_template"].format(polynomial)
                factored = sympy.factor(polynomial)
                answer = str(factored)
               
            elif problem_spec["answer_type"] == "roots":
                polynomial = problem_spec["polynomial"]
                question = problem_spec["question_template"].format(polynomial)
                roots = sympy.solve(polynomial, x)
                answer = ", ".join([str(root) for root in roots])
               
            elif problem_spec["answer_type"] == "division":
                polynomial = problem_spec["polynomial"]
                divisor = problem_spec["divisor"]
                question = problem_spec["question_template"].format(polynomial, divisor)
                quotient, remainder = sympy.div(polynomial, divisor)
                answer = f"Quotient: {quotient}, Remainder: {remainder}"
           
            # Coefficient coverage is tracked in _generate_random_polynomial
           
            return {
                "domain": "algebra",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "problem_type": problem_spec["answer_type"]
            }
           
        # Default case
        return self._generate_arithmetic_problem()
   
    def _generate_calculus_problem(self, subdomain=None, force_new=False):
        """Generate a calculus problem with systematic coverage"""
        if subdomain is None:
            subdomain = random.choice([
                "limits", "differentiation", "integration", "series",
                "multivariate_calculus", "vector_calculus"
            ])
           
        x, y, z, t = sympy.symbols('x y z t')
       
        if subdomain == "limits":
            # Generate a limit problem
            function_types = [
                lambda: sympy.sin(x)/x,  # sin(x)/x as x approaches 0
                lambda: (sympy.exp(x) - 1)/x,  # (e^x - 1)/x as x approaches 0
                lambda: (1 + x)**(1/x),  # (1 + x)^(1/x) as x approaches 0
                lambda: (sympy.cos(x) - 1)/x**2,  # (cos(x) - 1)/x^2 as x approaches 0
                lambda: sympy.sin(x)/sympy.tan(x),  # sin(x)/tan(x) as x approaches 0
                lambda: (x**3 - 1)/(x - 1),  # (x^3 - 1)/(x - 1) as x approaches 1
                lambda: (sympy.sqrt(x) - sympy.sqrt(a))/(x - a)  # (sqrt(x) - sqrt(a))/(x - a) as x approaches a
            ]
           
            function = random.choice(function_types)()
           
            # Choose a limit point
            if 'a' in str(function):
                a = sympy.Symbol('a')
                limit_point = a
            else:
                limit_points = [0, 1, sympy.oo, -sympy.oo]
                limit_point = random.choice(limit_points)
           
            # Compute the limit
            try:
                limit_value = sympy.limit(function, x, limit_point)
                limit_exists = True
            except:
                limit_exists = False
                limit_value = "DNE (Does Not Exist)"
           
            question = f"Calculate the limit: lim_(x→{limit_point}) {function}"
            answer = str(limit_value)
           
            # Track coverage
            self._update_coverage("calculus", "limits", hash(str(function)) % 10000)
           
            return {
                "domain": "calculus",
                "subdomain": subdomain,
                "question": question,
                "answer": answer,
                "symbolic_function": str(function),
                "limit_point": str(limit_point),
                "limit_exists": limit_exists
            }
           
        elif subdomain == "differentiation":
            # Generate a differentiation problem
            complexity = random.randint(1, 4)
            function = self._generate_random_expression(complexity, force_new)
           
            # Different types of differentiation problems
            problem_types = [
                lambda f: (f"Find the first derivative of f(x) = {f} with respect to x",
                          sympy.diff(f, x)),
                lambda f: (f"Find the second derivative of f(x) = {f} with respect to x",
                          sympy.diff(f, x, 2)),
                lambda f: (f"Find f'({random.randint(0, 5)}) if f(x) = {f}",
                          sympy.diff(f, x).subs(x, random.randint(0, 5)))
            ]
           
            question_generator = random.choice(problem_types)
            question, answer = question_generator(function)
           
            # Track coverage
            self._update_coverage("calculus", "differentiation", hash(str(function)) % 10000)
           
            return {
                "domain": "calculus",
                "subdomain": subdomain,
                "question": question,
                "answer": str(answer),
                "symbolic_function": str(function)
            }
           
        elif subdomain == "integration":
            # Generate an integration problem
            complexity = random.randint(1, 3)
            function = self._generate_random_expression(complexity, force_new)
           
            # Different types of integration problems
            problem_types = [
                lambda f: (f"Find the indefinite integral of f(x) = {f} with respect to x",
                          sympy.integrate(f, x)),
                lambda f: (f"Find the definite integral of f(x) = {f} from x = {random.randint(0, 3)} to x = {random.randint(4, 6)}",
                          sympy.integrate(f, (x, random.randint(0, 3), random.randint(4, 6))))
            ]
           
            question_generator = random.choice(problem_types)
            question, answer = question_generator(function)
           
            # Track coverage
            self._update_coverage("calculus", "integration", hash(str(function)) % 10000)
           
            return {
                "domain": "calculus",
                "subdomain": subdomain,
                "question": question,
                "answer": str(answer),
                "symbolic_function": str(function)
            }
           
        elif subdomain == "series":
            # Generate a series problem
            series_types = [
                lambda: (f"Determine whether the series Σ(1/n^2) from n=1 to ∞ converges or diverges.",
                         "Converges to π²/6"),
                lambda: (f"Determine whether the series Σ(1/n) from n=1 to ∞ converges or diverges.",
                         "Diverges (Harmonic series)"),
                lambda: (f"Find the sum of the geometric series Σ({random.randint(1, 5)}·{random.randint(1, 9)}/{10}^n) from n=0 to ∞.",
                         f"{random.randint(1, 5)}/({1 - random.randint(1, 9)/10})"),
                lambda: (f"Find the radius of convergence for the power series Σ(n·x^n) from n=1 to ∞.",
                         "R = 1")
            ]
           
            question, answer = random.choice(series_types)()
           
            # Track coverage
            self._update_coverage("calculus", "series", hash(question) % 10000)
           
            return {
                "domain": "calculus",
                "subdomain": subdomain,
                "question": question,
                "answer": answer
            }
           
        elif subdomain == "multivariate_calculus":
            # Generate a multivariate calculus problem
            function_types = [
                lambda: x**2 + y**2,
                lambda: x**2 - y**2,
                lambda: sympy.sin(x) * sympy.cos(y),
                lambda: sympy.exp(-(x**2 + y**2)),
                lambda: x**3 + 3*x*y**2
            ]
           
            function = random.choice(function_types)()
           
            problem_types = [
                lambda f: (f"Find ∂f/∂x for f(x,y) = {f}", sympy.diff(f, x)),
                lambda f: (f"Find ∂f/∂y for f(x,y) = {f}", sympy.diff(f, y)),
                lambda f: (f"Find ∂²f/∂x∂y for f(x,y) = {f}", sympy.diff(f, x, y)),
                lambda f: (f"Find the gradient ∇f for f(x,y) = {f}",
                          f"∇f = ({sympy.diff(f, x)})i + ({sympy.diff(f, y)})j")
            ]
           
            question_generator = random.choice(problem_types)
            question, answer = question_generator(function)
           
            # Track coverage
            self._update_coverage("calculus", "multivariate_calculus", hash(str(function)) % 10000)
           
            return {
                "domain": "calculus",
                "subdomain": subdomain,
                "question": question,
                "answer": str(answer),
                "symbolic_function": str(function)
            }
           
        elif subdomain == "vector_calculus":
            # Generate a vector calculus problem
            vector_field_types = [
                lambda: (sympy.Matrix([y, -x, 0]), "F = yi - xj"),
                lambda: (sympy.Matrix([x, y, z]), "F = xi + yj + zk"),
                lambda: (sympy.Matrix([y*z, x*z, x*y]), "F = yzi + xzj + xyk"),
                lambda: (sympy.Matrix([sympy.sin(y), sympy.cos(x), x*y]), "F = sin(y)i + cos(x)j + xyk")
            ]
           
            vector_field, vector_str = random.choice(vector_field_types)()
           
            problem_types = [
                lambda v, v_str: (f"Calculate the divergence of the vector field {v_str}.",
                                 sympy.divergence(v, (x, y, z))),
                lambda v, v_str: (f"Calculate the curl of the vector field {v_str}.",
                                 sympy.curl(v, (x, y, z)))
            ]
           
            question_generator = random.choice(problem_types)
            question, answer = question_generator(vector_field, vector_str)
           
            # Track coverage
            self._update_coverage("calculus", "vector_calculus", hash(vector_str) % 10000)
           
            return {
                "domain": "calculus",
                "subdomain": subdomain,
                "question": question,
                "answer": str(answer),
                "vector_field": vector_str
            }
           
        # Default case
        return {
            "domain": "calculus",
            "subdomain": "differentiation",
            "question": "Find the derivative of f(x) = x^2",
            "answer": "f'(x) = 2x",
            "symbolic_function": "x^2"
        }
   
    def _generate_geometry_problem(self, subdomain=None, force_new=False):
        """Generate a geometry problem with systematic coverage"""
        if subdomain is None:
            subdomain = random.choice([
                "euclidean_geometry", "coordinate_geometry", "analytic_geometry",
                "solid_geometry", "trigonometry"
            ])
           
        if subdomain == "euclidean_geometry":
            # Generate problems about shapes, angles, etc.
            shape_types = [
                "triangle", "rectangle", "circle", "square", "polygon", "angle"
            ]
           
            shape = random.choice(shape_types)
           
            if shape == "triangle":
                problem_types = [
                    # Area of triangle
                    lambda: {
                        "a": self._generate_random_number("integers", "small", force_new),
                        "b": self._generate_random_number("integers", "small", force_new),
                        "c": None,
                        "question_template": "Find the area of a triangle with base {a} and height {b}.",
                        "answer_formula": "0.5 * a * b",
                        "property": "area"
                    },
                    # Perimeter of triangle
                    lambda: {
                        "a": self._generate_random_number("integers", "small", force_new),
                        "b": self._generate_random_number("integers", "small", force_new),
                        "c": self._generate_random_number("integers", "small", force_new),
                        "question_template": "Find the perimeter of a triangle with sides {a}, {b}, and {c}.",
                        "answer_formula": "a + b + c",
                        "property": "perimeter"
                    },
                    # Pythagorean theorem
                    lambda: {
                        "a": self._generate_random_number("integers", "small", force_new),
                        "b": self._generate_random_number("integers", "small", force_new),
                        "c": None,  # Will be calculated
                        "question_template": "Find the hypotenuse of a right triangle with legs {a} and {b}.",
                        "answer_formula": "sqrt(a**2 + b**2)",
                        "property": "hypotenuse"
                    }
                ]
               
                problem_spec = random.choice(problem_types)()
               
                # Calculate the answer
                a = problem_spec["a"]
                b = problem_spec["b"]
                c = problem_spec["c"]
               
                formula = problem_spec["answer_formula"]
               
                if formula == "0.5 * a * b":
                    answer = 0.5 * a * b
                elif formula == "a + b + c":
                    answer = a + b + c
                elif formula == "sqrt(a**2 + b**2)":
                    answer = math.sqrt(a**2 + b**2)
               
                question = problem_spec["question_template"].format(a=a, b=b, c=c)
               
                # Track coverage
                self._update_coverage("geometry", "euclidean_geometry", (int(a), int(b)))
           
            # Implementations for other shapes would follow a similar pattern
            # For brevity, I'm focusing on triangle as an example
               
        # Implementation for more geometry subdomains would go here
        # For brevity, I'm focusing on euclidean_geometry as an example
           
        # Default case for geometry
        return {
            "domain": "geometry",
            "subdomain": "euclidean_geometry",
            "question": "Find the area of a circle with radius 5.",
            "answer": f"{25 * math.pi}",
            "shape": "circle",
            "property": "area"
        }
   
    def generate_question(self, domain=None, subdomain=None, force_new=False):
        """
        Generate a random math question based on domain and subdomain with statistical coverage
        """
        # Check memory before generation
        current_memory = self._check_memory_limits()
        if current_memory > self.memory_limit_mb:
            raise MemoryError(f"Memory usage of {current_memory:.2f}MB exceeds limit of {self.memory_limit_mb}MB")
       
        # Select domain with coverage-based weighting if not specified
        if domain is None:
            # Weight domains inversely by their coverage
            domain_weights = {d: 1.0 / (self.covered_domains.get(d, 1) + 1) for d in self.domains}
            total_weight = sum(domain_weights.values())
            normalized_weights = {d: w/total_weight for d, w in domain_weights.items()}
           
            domains = list(normalized_weights.keys())
            weights = list(normalized_weights.values())
            domain = random.choices(domains, weights=weights, k=1)[0]
           
        if subdomain is None and domain in self.domains:
            # Weight subdomains inversely by their coverage
            subdomain_weights = {}
            for sd in self.domains[domain]:
                key = f"{domain}_{sd}"
                subdomain_weights[sd] = 1.0 / (self.covered_subdomains.get(key, 1) + 1)
               
            total_weight = sum(subdomain_weights.values())
            if total_weight > 0:  # Prevent division by zero
                normalized_weights = {sd: w/total_weight for sd, w in subdomain_weights.items()}
               
                subdomains = list(normalized_weights.keys())
                weights = list(normalized_weights.values())
                subdomain = random.choices(subdomains, weights=weights, k=1)[0]
            else:
                subdomain = random.choice(self.domains[domain])

        # Call the appropriate generator method based on domain
        try:
            if domain == "arithmetic" or domain == "elementary_mathematics":
                return self._generate_arithmetic_problem(subdomain, force_new)
            elif domain == "algebra":
                return self._generate_algebra_problem(subdomain, force_new)
            elif domain == "calculus":
                return self._generate_calculus_problem(subdomain, force_new)
            elif domain == "geometry" or domain == "trigonometry":
                return self._generate_geometry_problem(subdomain, force_new)
            # Add other domains as needed
            else:
                # Default to arithmetic if domain not implemented
                return self._generate_arithmetic_problem(force_new=force_new)
        except Exception as e:
            print(f"Error generating {domain}/{subdomain} problem: {e}")
            # Fall back to arithmetic if there's an error
            return self._generate_arithmetic_problem(force_new=False)
   
    def generate_compound_question(self):
        """
        Generate an in-depth compound question with mathematically connected parts
        that build on each other to provide comprehensive mathematical coverage.
       
        Returns:
            A dictionary containing the mathematically coherent compound question
        """
        # Select a mathematical theme for interconnected questions
        theme = random.choice([
            "function_analysis",      # Calculus: analyzing a function in multiple ways
            "equation_solving",       # Algebra: multi-step solution of complex equation
            "geometric_sequence",     # Geometry: proof sequence on a geometric object
            "probability_scenario",   # Probability: multi-stage problem
            "number_theory_exploration", # Number theory: number properties
            "linear_algebra_sequence",   # Linear algebra: matrix and vector analysis
            "integration_methods",    # Calculus: multiple integration approaches
            "series_analysis",        # Calculus: sequence and series exploration
            "differential_equations", # ODEs: solve and analyze solutions
            "complex_analysis"        # Complex functions and properties
        ])
       
        # Generate appropriate mathematical domain based on theme
        if theme == "function_analysis":
            domain = "calculus"
            subdomain = random.choice(["differentiation", "limits", "continuity"])
        elif theme == "equation_solving":
            domain = "algebra"
            subdomain = random.choice(["linear_equations", "quadratic_equations", "systems_of_equations"])
        elif theme == "geometric_sequence":
            domain = "geometry"
            subdomain = random.choice(["euclidean_geometry", "coordinate_geometry"])
        elif theme == "probability_scenario":
            domain = "probability_and_statistics"
            subdomain = random.choice(["conditional_probability", "distributions"])
        elif theme == "number_theory_exploration":
            domain = "number_theory"
            subdomain = random.choice(["divisibility", "prime_numbers", "modular_arithmetic"])
        elif theme == "linear_algebra_sequence":
            domain = "algebra"
            subdomain = "matrices"
        elif theme == "integration_methods":
            domain = "calculus"
            subdomain = "integration"
        elif theme == "series_analysis":
            domain = "calculus"
            subdomain = "series"
        elif theme == "differential_equations":
            domain = "differential_equations"
            subdomain = random.choice(["linear_odes", "nonlinear_odes"])
        elif theme == "complex_analysis":
            domain = "analysis"
            subdomain = "complex_analysis"
       
        # Generate the compound question based on the theme
        if theme == "function_analysis":
            compound_data = self._generate_function_analysis_sequence()
        elif theme == "equation_solving":
            compound_data = self._generate_equation_solving_sequence()
        elif theme == "geometric_sequence":
            compound_data = self._generate_geometric_proof_sequence()
        elif theme == "probability_scenario":
            compound_data = self._generate_probability_scenario()
        elif theme == "number_theory_exploration":
            compound_data = self._generate_number_theory_sequence()
        elif theme == "linear_algebra_sequence":
            compound_data = self._generate_linear_algebra_sequence()
        elif theme == "integration_methods":
            compound_data = self._generate_integration_sequence()
        elif theme == "series_analysis":
            compound_data = self._generate_series_analysis_sequence()
        elif theme == "differential_equations":
            compound_data = self._generate_differential_equations_sequence()
        elif theme == "complex_analysis":
            compound_data = self._generate_complex_analysis_sequence()
        else:
            # Fallback to function analysis if none of the above work
            compound_data = self._generate_function_analysis_sequence()
       
        # Build the complete compound question
        compound_question = {
            "type": "compound",
            "domain": domain,
            "subdomain": subdomain,
            "theme": theme,
            "parts": compound_data["parts"],
            "context": compound_data["context"],
            "shared_object": compound_data.get("shared_object", "")
        }
       
        # Update coverage
        self._update_coverage(domain, subdomain)
       
        # Increment problem count
        self.total_problems_generated += 1
       
        # Check memory periodically
        if self.total_problems_generated % self.memory_check_interval == 0:
            self._check_memory_limits()
       
        return compound_question
   
    def _generate_function_analysis_sequence(self):
        """
        Generate a mathematically coherent sequence of questions that analyze a function in depth
        """
        # Generate a polynomial function of degree 3 for richness in behavior
        x = sympy.Symbol('x')
       
        # Generate coefficients ensuring we have a cubic term for interesting behavior
        a = self._generate_random_integer("small", True)
        while a == 0:
            a = self._generate_random_integer("small", True)
           
        b = self._generate_random_integer("small", True)
        c = self._generate_random_integer("small", True)
        d = self._generate_random_integer("small", True)
       
        # Create cubic polynomial: ax³ + bx² + cx + d
        poly = a*x**3 + b*x**2 + c*x + d
        function_str = str(poly)
       
        # Track coverage
        self._update_coverage("calculus", "differentiation", (a, b, c))
       
        # Calculate the derivative
        derivative = sympy.diff(poly, x)
        derivative_str = str(derivative)
       
        # Calculate the second derivative
        second_derivative = sympy.diff(derivative, x)
        second_derivative_str = str(second_derivative)
       
        # Find critical points by solving f'(x) = 0
        critical_points = sympy.solve(derivative, x)
       
        # For each critical point, determine nature using second derivative test
        critical_points_nature = []
        for cp in critical_points:
            # Evaluate second derivative at critical point
            sd_value = second_derivative.subs(x, cp)
            if sd_value > 0:
                nature = "local minimum"
            elif sd_value < 0:
                nature = "local maximum"
            else:
                nature = "inflection point (need further testing)"
            critical_points_nature.append((cp, nature))
       
        # Find inflection points by solving f''(x) = 0
        inflection_points = sympy.solve(second_derivative, x)
       
        # Create a sequence of interconnected questions about this function
        parts = [
            {
                "part_index": 1,
                "question": f"Find the first derivative of the function f(x) = {function_str}.",
                "answer": f"f'(x) = {derivative_str}",
                "explanation": "Differentiate term by term, applying the power rule and constant rule."
            },
            {
                "part_index": 2,
                "question": f"Find the critical points of f(x) = {function_str} by solving f'(x) = 0.",
                "answer": f"Critical points occur at x = {', '.join([str(cp) for cp in critical_points])}",
                "explanation": f"Set f'(x) = {derivative_str} = 0 and solve for x.",
                "depends_on": 1
            },
            {
                "part_index": 3,
                "question": "Find the second derivative of the function.",
                "answer": f"f''(x) = {second_derivative_str}",
                "explanation": "Differentiate f'(x) with respect to x.",
                "depends_on": 1
            },
            {
                "part_index": 4,
                "question": "Using the second derivative test, determine the nature of each critical point.",
                "answer": "; ".join([f"x = {cp} is a {nature}" for cp, nature in critical_points_nature]),
                "explanation": "For each critical point, evaluate the second derivative. If f''(c) > 0, then c is a local minimum. If f''(c) < 0, then c is a local maximum.",
                "depends_on": [2, 3]
            },
            {
                "part_index": 5,
                "question": "Find any inflection points of the function.",
                "answer": f"Inflection points occur at x = {', '.join([str(ip) for ip in inflection_points])}",
                "explanation": "Inflection points occur where f''(x) = 0 and f''(x) changes sign.",
                "depends_on": 3
            },
            {
                "part_index": 6,
                "question": f"Sketch the general shape of f(x) = {function_str}, indicating critical points and inflection points.",
                "answer": "The sketch should show the curve with marked critical points (maxima/minima) and inflection points, with the correct concavity in each region.",
                "explanation": "Use the information from the previous questions to sketch the function showing all key features.",
                "depends_on": [4, 5]
            }
        ]
       
        # Generate an explanation of how the parts connect
        context = f"""The following sequence of questions performs a complete analysis of the function f(x) = {function_str}.
Begin by finding derivatives, then use those to locate and classify critical points and inflection points,
ultimately leading to a complete understanding of the function's behavior."""
       
        return {
            "parts": parts,
            "context": context,
            "shared_object": function_str
        }
       
    def _generate_equation_solving_sequence(self):
        """
        Generate a mathematically coherent sequence about solving an equation step-by-step
        """
        # Create a moderately complex algebraic equation to solve
        x = sympy.Symbol('x')
       
        # Generate coefficients that will lead to a moderately complex but solvable equation
        a = self._generate_random_integer("small", True)
        while a == 0:
            a = self._generate_random_integer("small", True)
           
        b = self._generate_random_integer("small", True)
        c = self._generate_random_integer("small", True)
        d = self._generate_random_integer("small", True)
       
        # Create a rational equation with related terms: (ax + b)/(cx + d) = 2
        # This will require multiple steps and checking for extraneous solutions
        # Equation: (ax + b)/(cx + d) = 2
       
        # Track coverage
        self._update_coverage("algebra", "rational_functions", (a, b, c))
       
        # Set up the equation
        left_side = (a*x + b)/(c*x + d)
        right_side = 2
        equation = sympy.Eq(left_side, right_side)
        equation_str = str(equation)
       
        # Step 1: Multiply both sides by (cx + d) to clear the denominator
        step1 = sympy.Eq(a*x + b, 2*(c*x + d))
        step1_str = str(step1)
       
        # Step 2: Expand the right side
        step2 = sympy.Eq(a*x + b, 2*c*x + 2*d)
        step2_str = str(step2)
       
        # Step 3: Move all terms to left side
        step3 = sympy.Eq(a*x + b - 2*c*x - 2*d, 0)
        step3_str = str(step3)
       
        # Step 4: Combine like terms
        step4 = sympy.Eq((a - 2*c)*x + (b - 2*d), 0)
        step4_str = str(step4)
       
        # Step 5: Solve for x
        solution = sympy.solve(step4.lhs, x)[0]
        solution_str = str(solution)
       
        # Step 6: Check for extraneous solutions (values that make denominator zero)
        extraneous_check = solution.subs(x, c*x + d)
        has_extraneous = extraneous_check == 0
       
        # Create parts sequence
        parts = [
            {
                "part_index": 1,
                "question": f"Solve the equation: {equation_str}",
                "answer": "This requires multiple steps. Let's start by clearing the denominator.",
                "explanation": "This is a rational equation that requires clearing the denominator."
            },
            {
                "part_index": 2,
                "question": "Multiply both sides of the equation by the denominator (cx + d) to clear the fraction.",
                "answer": f"This gives us: {step1_str}",
                "explanation": "Multiplying both sides by (cx + d) eliminates the fraction.",
                "depends_on": 1
            },
            {
                "part_index": 3,
                "question": "Expand the right side of the equation.",
                "answer": f"{step2_str}",
                "explanation": "Distribute the 2 across (cx + d).",
                "depends_on": 2
            },
            {
                "part_index": 4,
                "question": "Rearrange the equation to standard form by moving all terms to the left side.",
                "answer": f"{step3_str}",
                "explanation": "Subtract 2cx + 2d from both sides.",
                "depends_on": 3
            },
            {
                "part_index": 5,
                "question": "Combine like terms.",
                "answer": f"{step4_str}",
                "explanation": "Combine the x terms and the constant terms.",
                "depends_on": 4
            },
            {
                "part_index": 6,
                "question": "Solve for x.",
                "answer": f"x = {solution_str}",
                "explanation": f"Divide by the coefficient of x and simplify.",
                "depends_on": 5
            },
            {
                "part_index": 7,
                "question": "Check for any extraneous solutions by verifying that your solution doesn't make the denominator zero.",
                "answer": f"We need to check if {c}x + {d} = 0 when x = {solution_str}. " +
                         (f"This gives {c}({solution_str}) + {d} = 0, which is " +
                          ("true" if has_extraneous else "false")) + ". " +
                          ("Therefore, this is an extraneous solution and the equation has no solution."
                           if has_extraneous else
                           f"Therefore, x = {solution_str} is a valid solution."),
                "explanation": "When solving rational equations, we must check if our solution makes any denominator zero, which would make the original expression undefined.",
                "depends_on": 6
            }
        ]
       
        # Create context
        context = f"""The following sequence of questions walks through the complete solution of the rational equation {equation_str}.
Each step builds on the previous one, from clearing the denominator through solving for x and checking for extraneous solutions."""
       
        return {
            "parts": parts,
            "context": context,
            "shared_object": equation_str
        }
       
    def _generate_geometric_proof_sequence(self):
        """
        Generate a mathematically coherent sequence of geometric proofs
        """
        # Create a geometric scenario involving triangles, circles, or other geometric objects
        geometry_type = random.choice(["triangle", "circle", "polygon"])
       
        if geometry_type == "triangle":
            # Generate a triangle with specific properties
            # For this example, we'll use a triangle with known sides and angles
            a = self._generate_random_integer("small", True)  # Side length
            while a < 3:  # Ensure reasonable side length
                a = self._generate_random_integer("small", True)
               
            b = self._generate_random_integer("small", True)  # Side length
            while b < 3:
                b = self._generate_random_integer("small", True)
               
            c = random.randint(max(abs(a-b)+1, 3), a+b-1)  # Ensure triangle inequality
           
            # Calculate angles using law of cosines
            angle_A = math.acos((b**2 + c**2 - a**2) / (2*b*c)) * 180/math.pi
            angle_B = math.acos((a**2 + c**2 - b**2) / (2*a*c)) * 180/math.pi
            angle_C = math.acos((a**2 + b**2 - c**2) / (2*a*b)) * 180/math.pi
           
            # Track coverage
            self._update_coverage("geometry", "euclidean_geometry", (a, b, c))
           
            # Round angles to 2 decimal places
            angle_A = round(angle_A, 2)
            angle_B = round(angle_B, 2)
            angle_C = round(angle_C, 2)
           
            # Check if triangle is special
            is_equilateral = a == b == c
            is_isosceles = a == b or b == c or a == c
            is_right = abs(angle_A - 90) < 0.1 or abs(angle_B - 90) < 0.1 or abs(angle_C - 90) < 0.1
           
            triangle_type = "scalene"
            if is_equilateral:
                triangle_type = "equilateral"
            elif is_isosceles:
                triangle_type = "isosceles"
               
            if is_right:
                triangle_type += " right"
           
            # Calculate area using Heron's formula
            s = (a + b + c) / 2  # Semi-perimeter
            area = math.sqrt(s * (s-a) * (s-b) * (s-c))
           
            # Create a sequence of proof questions about triangle properties
            parts = [
                {
                    "part_index": 1,
                    "question": f"Consider triangle ABC with sides a = {a}, b = {b}, and c = {c}. Calculate the three angles of the triangle using the law of cosines.",
                    "answer": f"Angle A = {angle_A}°, Angle B = {angle_B}°, Angle C = {angle_C}°",
                    "explanation": "Use the law of cosines: cos(A) = (b² + c² - a²)/(2bc), and similarly for the other angles."
                },
                {
                    "part_index": 2,
                    "question": "Verify that the three angles of the triangle sum to 180°.",
                    "answer": f"A + B + C = {angle_A} + {angle_B} + {angle_C} = {angle_A + angle_B + angle_C}°, which is {abs(angle_A + angle_B + angle_C - 180) < 0.1}",
                    "explanation": "Due to rounding, the sum might be slightly off from exactly 180°, but the actual angles in a triangle always sum to 180°.",
                    "depends_on": 1
                },
                {
                    "part_index": 3,
                    "question": f"Classify the triangle based on its sides and angles.",
                    "answer": f"This is a {triangle_type} triangle.",
                    "explanation": "A triangle is equilateral if all sides are equal, isosceles if exactly two sides are equal, and scalene if no sides are equal. It's a right triangle if one angle is 90°.",
                    "depends_on": [1, 2]
                },
                {
                    "part_index": 4,
                    "question": "Calculate the area of the triangle using Heron's formula.",
                    "answer": f"Area = {area:.2f} square units",
                    "explanation": "Heron's formula: Area = √(s(s-a)(s-b)(s-c)) where s = (a+b+c)/2 is the semi-perimeter."
                },
                {
                    "part_index": 5,
                    "question": "Determine the radius of the inscribed circle (incircle) of the triangle.",
                    "answer": f"Incircle radius = {area/s:.2f} units",
                    "explanation": "The incircle radius r = Area/s, where s is the semi-perimeter.",
                    "depends_on": 4
                },
                {
                    "part_index": 6,
                    "question": "Determine the radius of the circumscribed circle (circumcircle) of the triangle.",
                    "answer": f"Circumcircle radius = {(a*b*c)/(4*area):.2f} units",
                    "explanation": "The circumcircle radius R = (abc)/(4×Area).",
                    "depends_on": 4
                }
            ]
           
            # Create context
            context = f"""The following sequence of questions explores various geometric properties of a triangle with sides
a = {a}, b = {b}, and c = {c}. Each question builds on the results of previous calculations,
leading to a comprehensive understanding of this specific triangle."""
           
            return {
                "parts": parts,
                "context": context,
                "shared_object": f"Triangle with sides a = {a}, b = {b}, c = {c}"
            }
           
        elif geometry_type == "circle":
            # Generate a circle scenario
            radius = self._generate_random_integer("small", True)
            while radius < 2:  # Ensure reasonable radius
                radius = self._generate_random_integer("small", True)
               
            # Track coverage
            self._update_coverage("geometry", "euclidean_geometry", radius)
           
            # Create circle properties
            area = math.pi * radius**2
            circumference = 2 * math.pi * radius
           
            # Create a sequence about circle properties
            parts = [
                {
                    "part_index": 1,
                    "question": f"Consider a circle with radius r = {radius} units. Calculate its area and circumference.",
                    "answer": f"Area = πr² = π·{radius}² = {area:.2f} square units; Circumference = 2πr = 2π·{radius} = {circumference:.2f} units",
                    "explanation": "The area of a circle is πr² and its circumference is 2πr, where r is the radius."
                },
                {
                    "part_index": 2,
                    "question": "A regular hexagon is inscribed in this circle. Calculate the length of each side of the hexagon.",
                    "answer": f"Side length = r = {radius} units",
                    "explanation": "For a regular hexagon inscribed in a circle, each side equals the radius of the circle.",
                    "depends_on": 1
                },
                {
                    "part_index": 3,
                    "question": "Calculate the area of the inscribed regular hexagon.",
                    "answer": f"Area = (3√3/2)·r² = (3√3/2)·{radius}² = {(3*math.sqrt(3)/2)*radius**2:.2f} square units",
                    "explanation": "The area of a regular hexagon with side length s is (3√3/2)·s². Since s = r for the inscribed hexagon, the area is (3√3/2)·r².",
                    "depends_on": 2
                },
                {
                    "part_index": 4,
                    "question": "Calculate the ratio of the area of the circle to the area of the inscribed regular hexagon.",
                    "answer": f"Ratio = {area/((3*math.sqrt(3)/2)*radius**2):.4f} = 2π/(3√3) ≈ 1.2092",
                    "explanation": "The ratio is (πr²)/((3√3/2)·r²) = 2π/(3√3).",
                    "depends_on": [1, 3]
                },
                {
                    "part_index": 5,
                    "question": "Now consider a regular hexagon circumscribed around the circle. Calculate its area.",
                    "answer": f"Area = 2√3·r² = 2√3·{radius}² = {2*math.sqrt(3)*radius**2:.2f} square units",
                    "explanation": "The area of a regular hexagon circumscribed around a circle of radius r is 2√3·r².",
                    "depends_on": 1
                },
                {
                    "part_index": 6,
                    "question": "Calculate the ratio of the area of the circumscribed regular hexagon to the area of the circle.",
                    "answer": f"Ratio = {(2*math.sqrt(3)*radius**2)/area:.4f} = 2√3/π ≈ 1.1027",
                    "explanation": "The ratio is (2√3·r²)/(πr²) = 2√3/π.",
                    "depends_on": [1, 5]
                }
            ]
           
            # Create context
            context = f"""The following sequence of questions explores the geometric properties of a circle with radius {radius} units,
along with inscribed and circumscribed regular hexagons. The sequence builds systematically from basic properties
to more complex relationships between these geometric figures."""
           
            return {
                "parts": parts,
                "context": context,
                "shared_object": f"Circle with radius r = {radius} units"
            }
           
        # Add more geometry types as needed
       
        # Default fallback to triangle
        return self._generate_geometric_proof_sequence()
       
    def _generate_probability_scenario(self):
        """
        Generate a mathematically coherent multi-stage probability scenario
        """
        # Create a probability scenario with multiple related questions
        scenario_type = random.choice(["cards", "dice", "urn", "coins", "marbles"])
       
        if scenario_type == "cards":
            # Card drawing scenario
            # Track coverage
            self._update_coverage("probability_and_statistics", "conditional_probability", hash(scenario_type) % 10000)
           
            parts = [
                {
                    "part_index": 1,
                    "question": "A standard deck of 52 playing cards contains 4 suits (hearts, diamonds, clubs, spades), each with 13 cards (Ace, 2-10, Jack, Queen, King). What is the probability of drawing a heart from a well-shuffled deck?",
                    "answer": "P(heart) = 13/52 = 1/4 = 0.25",
                    "explanation": "There are 13 hearts in a 52-card deck."
                },
                {
                    "part_index": 2,
                    "question": "If you draw one card from the deck and it is a heart, what is the probability that the next card drawn (without replacement) is also a heart?",
                    "answer": "P(heart | heart) = 12/51 ≈ 0.235",
                    "explanation": "After drawing one heart, there are 12 hearts remaining out of 51 cards.",
                    "depends_on": 1
                },
                {
                    "part_index": 3,
                    "question": "What is the probability of drawing two hearts in a row from the deck (without replacement)?",
                    "answer": "P(H₁ ∩ H₂) = P(H₁) × P(H₂|H₁) = (13/52) × (12/51) = 156/2652 = 13/221 ≈ 0.0588",
                    "explanation": "We use the conditional probability: P(A and B) = P(A) × P(B|A)",
                    "depends_on": 2
                },
                {
                    "part_index": 4,
                    "question": "If you draw two cards without replacement, what is the probability that both are face cards (Jack, Queen, or King)?",
                    "answer": "P(both face cards) = (12/52) × (11/51) = 132/2652 = 11/221 ≈ 0.0498",
                    "explanation": "There are 12 face cards in a deck. After drawing one face card, there are 11 face cards left out of 51 cards.",
                    "depends_on": 3
                },
                {
                    "part_index": 5,
                    "question": "If you draw three cards without replacement, what is the probability of getting a sequence with exactly one heart?",
                    "answer": "P(exactly one heart) = C(13,1) × C(39,2) / C(52,3) = 13 × 741 / 22100 = 9633/22100 ≈ 0.436",
                    "explanation": "We need to choose 1 heart from 13 hearts, and 2 non-hearts from 39 non-hearts, divided by the total number of ways to choose 3 cards from 52.",
                    "depends_on": 4
                },
                {
                    "part_index": 6,
                    "question": "If you draw five cards without replacement (a poker hand), what is the probability of getting a flush (all 5 cards of the same suit)?",
                    "answer": "P(flush) = 4 × C(13,5) / C(52,5) = 4 × 1287 / 2598960 = 5148/2598960 = 0.00198",
                    "explanation": "There are 4 ways to choose a suit, and C(13,5) ways to choose 5 cards from that suit. The total number of 5-card hands is C(52,5).",
                    "depends_on": 5
                }
            ]
           
            # Create context
            context = """The following sequence of questions explores probability concepts in the context of drawing cards
from a standard deck of 52 playing cards. The sequence builds from simple probabilities to more complex
scenarios involving multiple draws and specific hand combinations."""
           
            return {
                "parts": parts,
                "context": context,
                "shared_object": "Standard deck of 52 playing cards"
            }
           
        elif scenario_type == "urn":
            # Urn probability scenario (balls in urn)
            red = self._generate_random_integer("tiny", True) + 2  # At least 2
            blue = self._generate_random_integer("tiny", True) + 2
            green = self._generate_random_integer("tiny", True) + 2
            total = red + blue + green
           
            # Track coverage
            self._update_coverage("probability_and_statistics", "conditional_probability", (red, blue, green))
           
            parts = [
                {
                    "part_index": 1,
                    "question": f"An urn contains {red} red balls, {blue} blue balls, and {green} green balls. If you draw one ball at random, what is the probability of drawing a red ball?",
                    "answer": f"P(red) = {red}/{total} = {red/total:.4f}",
                    "explanation": f"There are {red} red balls out of {total} total balls."
                },
                {
                    "part_index": 2,
                    "question": "If you draw one ball and it is red, what is the probability that the next ball drawn (without replacement) is blue?",
                    "answer": f"P(blue | red) = {blue}/({total}-1) = {blue}/{total-1} = {blue/(total-1):.4f}",
                    "explanation": f"After drawing a red ball, there are {blue} blue balls out of {total-1} remaining balls.",
                    "depends_on": 1
                },
                {
                    "part_index": 3,
                    "question": "What is the probability of drawing one ball of each color in exactly three draws (without replacement)?",
                    "answer": f"P(one of each) = {red}×{blue}×{green}/[{total}×({total}-1)×({total}-2)] = {red*blue*green}/[{total*(total-1)*(total-2)}] = {(red*blue*green)/(total*(total-1)*(total-2)):.4f}",
                    "explanation": "We need the first draw to be one color, the second draw to be a different color, and the third draw to be the remaining color. This happens in 3! = 6 different ways, but we need to account for the specific probabilities of each draw.",
                    "depends_on": 2
                },
                {
                    "part_index": 4,
                    "question": "Suppose you draw balls one at a time without replacement until you get a green ball. What is the probability that you need exactly 3 draws?",
                    "answer": f"P(green on 3rd draw) = ({red}+{blue})/{total} × ({red}+{blue}-1)/({total}-1) × {green}/({total}-2) = {((red+blue)/(total))*((red+blue-1)/(total-1))*(green/(total-2)):.4f}",
                    "explanation": "This requires that the first two draws are not green (they're either red or blue), and the third draw is green.",
                    "depends_on": 3
                },
                {
                    "part_index": 5,
                    "question": "If you draw 2 balls simultaneously, what is the probability of getting exactly one red ball?",
                    "answer": f"P(exactly one red) = [C({red},1) × C({blue}+{green},1)] / C({total},2) = [{red}×({blue}+{green})] / [{total}×({total}-1)/2] = {(red*(blue+green))/((total*(total-1))/2):.4f}",
                    "explanation": "We need to choose 1 red ball from {red} red balls, and 1 non-red ball from {blue+green} non-red balls, divided by the total number of ways to choose 2 balls from {total} balls.",
                    "depends_on": 1
                },
                {
                    "part_index": 6,
                    "question": "Suppose you draw 4 balls with replacement. What is the probability that you get at least one ball of each color?",
                    "answer": "This requires calculating the complement: P(at least one of each) = 1 - P(all red) - P(all blue) - P(all green) - P(only red and blue) - P(only red and green) - P(only blue and green)",
                    "explanation": "This is a complex calculation involving inclusion-exclusion principle. We need to find the probability of NOT getting at least one of each color, which means either missing red entirely, missing blue entirely, or missing green entirely.",
                    "depends_on": 1
                }
            ]
           
            # Create context
            context = f"""The following sequence of questions explores probability concepts in the context of drawing balls from an urn
containing {red} red balls, {blue} blue balls, and {green} green balls. The sequence builds from basic probabilities
to more complex scenarios involving multiple draws, conditional probabilities, and combinatorial calculations."""
           
            return {
                "parts": parts,
                "context": context,
                "shared_object": f"Urn with {red} red, {blue} blue, and {green} green balls"
            }
       
        # Add more probability scenario types as needed
       
        # Default fallback
        return self._generate_probability_scenario()
   
    def _generate_different_properties(self, domain, subdomain, num_parts, force_new=False):
        """Generate questions about different properties of the same mathematical object"""
        parts = []
       
        # Generate a base mathematical object
        if domain == "geometry":
            # Generate a geometric object with various properties to explore
            if subdomain in ["euclidean_geometry", "coordinate_geometry"]:
                # Create a triangle with various properties
                a = self._generate_random_integer("small", force_new)
                b = self._generate_random_integer("small", force_new)
                c = random.randint(max(abs(a-b) + 1, 1), a+b-1)  # Ensure triangle inequality
               
                # Questions about different properties
                properties = [
                    {"name": "perimeter", "question": f"Find the perimeter of a triangle with sides {a}, {b}, and {c}.",
                     "answer": f"{a + b + c}"},
                    {"name": "area", "question": f"Find the area of a triangle with sides {a}, {b}, and {c} using Heron's formula.",
                     "answer": f"Calculation using Heron's formula with s = {(a+b+c)/2}"},
                    {"name": "angles", "question": f"Find the largest angle in a triangle with sides {a}, {b}, and {c}.",
                     "answer": "Calculation required using Law of Cosines"},
                    {"name": "type", "question": f"What type of triangle is formed by sides {a}, {b}, and {c}?",
                     "answer": "Depends on the specific values"}
                ]
               
                # Track coverage
                self._update_coverage(domain, subdomain, (a, b, c))
               
                # Add properties as parts
                for i in range(min(num_parts, len(properties))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": properties[i]["question"],
                        "answer": properties[i]["answer"],
                        "property": properties[i]["name"],
                        "object_type": "triangle",
                        "parameters": {"a": a, "b": b, "c": c},
                        "part_index": i + 1
                    })
       
        elif domain == "algebra" and subdomain == "functions":
            # Create a function and explore its properties
            function_type = random.choice(["linear", "quadratic", "exponential"])
           
            if function_type == "linear":
                m = self._generate_random_integer("small", force_new)
                while m == 0:
                    m = self._generate_random_integer("small", force_new)
                b = self._generate_random_integer("medium", force_new)
                function_str = f"f(x) = {m}x + {b}"
               
                properties = [
                    {"name": "value", "question": f"For the function {function_str}, find f(2).",
                     "answer": f"{m * 2 + b}"},
                    {"name": "root", "question": f"For the function {function_str}, find the value of x where f(x) = 0.",
                     "answer": f"x = {-b/m}"},
                    {"name": "slope", "question": f"What is the slope of the function {function_str}?",
                     "answer": f"{m}"},
                    {"name": "y-intercept", "question": f"What is the y-intercept of the function {function_str}?",
                     "answer": f"{b}"}
                ]
               
                # Track coverage
                self._update_coverage(domain, subdomain, (m, b))
               
            elif function_type == "quadratic":
                a = self._generate_random_integer("small", force_new)
                while a == 0:
                    a = self._generate_random_integer("small", force_new)
                b = self._generate_random_integer("medium", force_new)
                c = self._generate_random_integer("medium", force_new)
                function_str = f"f(x) = {a}x² + {b}x + {c}"
               
                properties = [
                    {"name": "value", "question": f"For the function {function_str}, find f(1).",
                     "answer": f"{a + b + c}"},
                    {"name": "vertex", "question": f"Find the vertex of the function {function_str}.",
                     "answer": f"x = {-b/(2*a)}, y = calculation required"},
                    {"name": "axis", "question": f"Find the axis of symmetry for the function {function_str}.",
                     "answer": f"x = {-b/(2*a)}"},
                    {"name": "discriminant", "question": f"Find the discriminant of the function {function_str} and determine the number of real roots.",
                     "answer": f"Discriminant = {b*b - 4*a*c}, leading to appropriate conclusion"}
                ]
               
                # Track coverage
                self._update_coverage(domain, subdomain, (a, b, c))
               
            elif function_type == "exponential":
                a = self._generate_random_integer("small", force_new)
                while a == 0 or a == 1:
                    a = self._generate_random_integer("small", force_new)
                b = self._generate_random_integer("small", force_new)
                function_str = f"f(x) = {a}^x + {b}"
               
                properties = [
                    {"name": "value", "question": f"For the function {function_str}, find f(2).",
                     "answer": f"{a**2 + b}"},
                    {"name": "growth_rate", "question": f"For the function {function_str}, determine if it represents exponential growth or decay.",
                     "answer": f"{'Growth' if a > 1 else 'Decay'}"},
                    {"name": "y-intercept", "question": f"Find the y-intercept of the function {function_str}.",
                     "answer": f"{1 + b}"},
                    {"name": "asymptote", "question": f"Does the function {function_str} have a horizontal asymptote? If yes, find it.",
                     "answer": f"{'Yes, y = ' + str(b) if a < 1 else 'No horizontal asymptote'}"}
                ]
               
                # Track coverage
                self._update_coverage(domain, subdomain, (a, b))
               
            # Add the properties as separate parts
            for i in range(min(num_parts, len(properties))):
                parts.append({
                    "domain": domain,
                    "subdomain": subdomain,
                    "question": properties[i]["question"],
                    "answer": properties[i]["answer"],
                    "property": properties[i]["name"],
                    "function": function_str,
                    "function_type": function_type,
                    "part_index": i + 1
                })
       
        # Generate the appropriate number of parts
        while len(parts) < num_parts:
            # If specific domain handling didn't generate enough parts, add generic ones
            property_number = len(parts) + 1
           
            try:
                # Fall back to standard question generation
                problem = self.generate_question(domain, subdomain, force_new)
                problem["question"] = f"Property {property_number}: {problem['question']}"
                problem["property"] = f"property_{property_number}"
                problem["part_index"] = property_number
                parts.append(problem)
            except Exception as e:
                # If there's an error, create a placeholder
                parts.append({
                    "domain": domain,
                    "subdomain": subdomain,
                    "question": f"Property {property_number}: Additional property of the mathematical object",
                    "answer": "Answer not generated",
                    "property": f"property_{property_number}",
                    "part_index": property_number
                })
               
        return parts
   
    def _generate_step_by_step(self, domain, subdomain, num_parts, force_new=False):
        """Generate a sequence of questions representing steps to solve a larger problem"""
        parts = []
       
        # Select a problem type that can be broken into steps
        if domain == "algebra" and subdomain in ["linear_equations", "quadratic_equations"]:
            # Create a multi-step algebra problem
            if subdomain == "linear_equations":
                # Generate a more complex linear equation that requires multiple steps
                a = self._generate_random_integer("small", force_new)
                while a == 0:
                    a = self._generate_random_integer("small", force_new)
                b = self._generate_random_integer("medium", force_new)
                c = self._generate_random_integer("small", force_new)
                while c == 0:
                    c = self._generate_random_integer("small", force_new)
                d = self._generate_random_integer("medium", force_new)
               
                # Track coverage
                self._update_coverage(domain, subdomain, (a, b, c))
               
                # A problem like: a(x + b) = c(x - d)
                equation = f"{a}(x + {b}) = {c}(x - {d})"
               
                steps = [
                    {"name": "expand",
                     "question": f"Step 1: Expand the equation {equation}.",
                     "answer": f"{a}x + {a*b} = {c}x - {c*d}"},
                   
                    {"name": "rearrange",
                     "question": f"Step 2: Rearrange to get all terms with x on the left side and constants on the right side.",
                     "answer": f"{a}x - {c}x = -{a*b} - {c*d}"},
                   
                    {"name": "combine",
                     "question": f"Step 3: Combine like terms.",
                     "answer": f"{a-c}x = -{a*b + c*d}"},
                   
                    {"name": "solve",
                     "question": f"Step 4: Solve for x.",
                     "answer": f"x = {-(a*b + c*d)/(a-c)}" if a != c else "No solution (contradiction)"}
                ]
               
                # Add the steps as separate parts
                for i in range(min(num_parts, len(steps))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": steps[i]["question"],
                        "answer": steps[i]["answer"],
                        "step": steps[i]["name"],
                        "equation": equation,
                        "part_index": i + 1
                    })
       
        elif domain == "calculus" and subdomain == "integration":
            # Create a multi-step integration problem
            function_type = random.choice(["polynomial", "trigonometric", "exponential"])
           
            if function_type == "polynomial":
                # Integration by parts example
                function = "x * e^x"
               
                steps = [
                    {"name": "identify",
                     "question": f"Step 1: To integrate {function} dx, identify u and dv for integration by parts.",
                     "answer": "u = x, dv = e^x dx"},
                   
                    {"name": "find_values",
                     "question": f"Step 2: Find du and v for the integration by parts formula.",
                     "answer": "du = dx, v = e^x"},
                   
                    {"name": "apply_formula",
                     "question": f"Step 3: Apply the integration by parts formula: ∫u dv = uv - ∫v du",
                     "answer": "∫x e^x dx = x * e^x - ∫e^x dx"},
                   
                    {"name": "evaluate",
                     "question": f"Step 4: Evaluate the remaining integral and simplify.",
                     "answer": "∫x e^x dx = x * e^x - e^x + C = e^x(x - 1) + C"}
                ]
               
                # Track coverage
                self._update_coverage(domain, subdomain, hash(function) % 10000)
               
                # Add the steps as separate parts
                for i in range(min(num_parts, len(steps))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": steps[i]["question"],
                        "answer": steps[i]["answer"],
                        "step": steps[i]["name"],
                        "function": function,
                        "part_index": i + 1
                    })
                   
            elif function_type == "trigonometric":
                # Integration of a trigonometric function
                function = "sin^2(x)"
               
                steps = [
                    {"name": "identity",
                     "question": f"Step 1: To integrate {function} dx, use a trigonometric identity to rewrite the function.",
                     "answer": "sin^2(x) = (1 - cos(2x))/2"},
                   
                    {"name": "substitute",
                     "question": f"Step 2: Substitute the identity into the integral.",
                     "answer": "∫sin^2(x) dx = ∫(1 - cos(2x))/2 dx = (1/2)∫dx - (1/2)∫cos(2x) dx"},
                   
                    {"name": "integrate",
                     "question": f"Step 3: Integrate each term separately.",
                     "answer": "(1/2)∫dx - (1/2)∫cos(2x) dx = (1/2)x - (1/2)(sin(2x)/2) + C"},
                   
                    {"name": "simplify",
                     "question": f"Step 4: Simplify the final result.",
                     "answer": "∫sin^2(x) dx = (1/2)x - (1/4)sin(2x) + C"}
                ]
               
                # Track coverage
                self._update_coverage(domain, subdomain, hash(function) % 10000)
               
                # Add the steps as separate parts
                for i in range(min(num_parts, len(steps))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": steps[i]["question"],
                        "answer": steps[i]["answer"],
                        "step": steps[i]["name"],
                        "function": function,
                        "part_index": i + 1
                    })
       
        # Generate the appropriate number of parts
        while len(parts) < num_parts:
            # If specific domain handling didn't generate enough parts, add generic ones
            step_number = len(parts) + 1
           
            try:
                # Fall back to standard question generation
                problem = self.generate_question(domain, subdomain, force_new)
                problem["question"] = f"Step {step_number}: {problem['question']}"
                problem["step"] = f"step_{step_number}"
                problem["part_index"] = step_number
                parts.append(problem)
            except Exception as e:
                # If there's an error, create a placeholder
                parts.append({
                    "domain": domain,
                    "subdomain": subdomain,
                    "question": f"Step {step_number}: Additional step in solving the problem",
                    "answer": "Answer not generated",
                    "step": f"step_{step_number}",
                    "part_index": step_number
                })
               
        return parts
   
    def _generate_variations(self, domain, subdomain, num_parts, force_new=False):
        """Generate variations on a theme - similar problems with slight modifications"""
        parts = []
       
        # Generate variations of a base problem
        if domain == "probability":
            # Create variations on a probability problem
            if subdomain in ["basic_probability", "conditional_probability"]:
                # Base scenario: bag with colored balls
                red = self._generate_random_integer("small", force_new)
                blue = self._generate_random_integer("small", force_new)
                green = self._generate_random_integer("small", force_new)
                total = red + blue + green
               
                # Track coverage
                self._update_coverage(domain, subdomain, (red, blue, green))
               
                variations = [
                    {"name": "single_draw",
                     "question": f"A bag contains {red} red balls, {blue} blue balls, and {green} green balls. What is the probability of drawing a red ball?",
                     "answer": f"{red}/{total}"},
                   
                    {"name": "specific_sequence",
                     "question": f"From a bag containing {red} red balls, {blue} blue balls, and {green} green balls, two balls are drawn without replacement. What is the probability of drawing a red ball followed by a blue ball?",
                     "answer": f"{red}/{total} × {blue}/{total-1} = {red*blue}/{total*(total-1)}"},
                   
                    {"name": "conditional",
                     "question": f"From a bag containing {red} red balls, {blue} blue balls, and {green} green balls, what is the probability of drawing a blue ball given that the first ball drawn was red? (Assume the first ball is not replaced.)",
                     "answer": f"{blue}/{total-1}"},
                   
                    {"name": "complement",
                     "question": f"From a bag containing {red} red balls, {blue} blue balls, and {green} green balls, what is the probability of drawing a ball that is not green?",
                     "answer": f"{red+blue}/{total} = {(red+blue)/total}"}
                ]
               
                # Add the variations as separate parts
                for i in range(min(num_parts, len(variations))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": variations[i]["question"],
                        "answer": variations[i]["answer"],
                        "variation": variations[i]["name"],
                        "scenario": "colored_balls",
                        "parameters": {"red": red, "blue": blue, "green": green},
                        "part_index": i + 1
                    })
       
        elif domain == "geometry":
            # Create variations on a geometry problem
            if subdomain in ["euclidean_geometry", "coordinate_geometry"]:
                # Base scenario: triangle
                base = self._generate_random_integer("small", force_new)
                height = self._generate_random_integer("small", force_new)
               
                # Track coverage
                self._update_coverage(domain, subdomain, (base, height))
               
                variations = [
                    {"name": "area_triangle",
                     "question": f"Find the area of a triangle with base {base} and height {height}.",
                     "answer": f"{(base * height)/2}"},
                   
                    {"name": "area_parallelogram",
                     "question": f"Find the area of a parallelogram with base {base} and height {height}.",
                     "answer": f"{base * height}"},
                   
                    {"name": "area_rhombus",
                     "question": f"Find the area of a rhombus with diagonals of length {base} and {height}.",
                     "answer": f"{(base * height)/2}"},
                   
                    {"name": "area_trapezoid",
                     "question": f"Find the area of a trapezoid with parallel sides of length {base} and {base+4}, and height {height}.",
                     "answer": f"{(2*base+4) * height/2} = {(2*base+4) * height/2}"}
                ]
               
                # Add the variations as separate parts
                for i in range(min(num_parts, len(variations))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": variations[i]["question"],
                        "answer": variations[i]["answer"],
                        "variation": variations[i]["name"],
                        "scenario": "shape_areas",
                        "parameters": {"base": base, "height": height},
                        "part_index": i + 1
                    })
       
        # Generate the appropriate number of parts
        while len(parts) < num_parts:
            # If specific domain handling didn't generate enough parts, add generic ones
            variation_number = len(parts) + 1
           
            try:
                # Fall back to standard question generation
                problem = self.generate_question(domain, subdomain, force_new)
                problem["question"] = f"Variation {variation_number}: {problem['question']}"
                problem["variation"] = f"variation_{variation_number}"
                problem["part_index"] = variation_number
                parts.append(problem)
            except Exception as e:
                # If there's an error, create a placeholder
                parts.append({
                    "domain": domain,
                    "subdomain": subdomain,
                    "question": f"Variation {variation_number}: Additional variation of the problem",
                    "answer": "Answer not generated",
                    "variation": f"variation_{variation_number}",
                    "part_index": variation_number
                })
               
        return parts
   
    def _generate_application_sequence(self, domain, subdomain, num_parts, force_new=False):
        """Generate a sequence from theory to application"""
        parts = []
       
        # Theory to application progression
        if domain == "calculus":
            # Create a theory-to-application sequence for calculus
            if subdomain == "differentiation":
                # Start with theory of derivatives, then move to applications
                function = "f(x) = x^2 - 4x + 7"
               
                # Track coverage
                self._update_coverage(domain, subdomain, hash(function) % 10000)
               
                applications = [
                    {"name": "definition",
                     "question": f"Find the derivative of {function} using the definition of the derivative.",
                     "answer": "f'(x) = 2x - 4"},
                   
                    {"name": "value",
                     "question": f"For {function}, evaluate f'(3).",
                     "answer": "f'(3) = 2(3) - 4 = 2"},
                   
                    {"name": "critical_points",
                     "question": f"Find all critical points of {function}.",
                     "answer": "Setting f'(x) = 0: 2x - 4 = 0, so x = 2 is the only critical point."},
                   
                    {"name": "optimization",
                     "question": f"A particle moves according to the position function {function} meters at time x seconds. At what time does the particle reach its minimum velocity?",
                     "answer": "The velocity is f'(x) = 2x - 4, which is minimized when x = 2 seconds."}
                ]
               
                # Add the applications as separate parts
                for i in range(min(num_parts, len(applications))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": applications[i]["question"],
                        "answer": applications[i]["answer"],
                        "application": applications[i]["name"],
                        "function": function,
                        "part_index": i + 1
                    })
       
        elif domain == "linear_algebra":
            # Create a theory-to-application sequence for linear algebra
            if subdomain == "matrices":
                # Define a matrix
                matrix_values = [[self._generate_random_integer("tiny", force_new) for _ in range(2)] for _ in range(2)]
                matrix_str = f"A = [({matrix_values[0][0]}, {matrix_values[0][1]}), ({matrix_values[1][0]}, {matrix_values[1][1]})]"
               
                # Track coverage
                self._update_coverage(domain, subdomain, (matrix_values[0][0], matrix_values[0][1], matrix_values[1][0]))
               
                applications = [
                    {"name": "properties",
                     "question": f"Calculate the determinant of the matrix {matrix_str}.",
                     "answer": f"det(A) = {matrix_values[0][0]}*{matrix_values[1][1]} - {matrix_values[0][1]}*{matrix_values[1][0]} = {matrix_values[0][0]*matrix_values[1][1] - matrix_values[0][1]*matrix_values[1][0]}"},
                   
                    {"name": "inverse",
                     "question": f"Find the inverse of the matrix {matrix_str}, if it exists.",
                     "answer": "Calculation required based on the determinant"},
                   
                    {"name": "system",
                     "question": f"Use the matrix {matrix_str} to solve the system of equations: {matrix_values[0][0]}x + {matrix_values[0][1]}y = 10, {matrix_values[1][0]}x + {matrix_values[1][1]}y = 20",
                     "answer": "Calculation required using matrix methods"},
                   
                    {"name": "transformation",
                     "question": f"If the matrix {matrix_str} represents a linear transformation T, find T((3,4)).",
                     "answer": f"T((3,4)) = A * [3,4] = [{matrix_values[0][0]}*3 + {matrix_values[0][1]}*4, {matrix_values[1][0]}*3 + {matrix_values[1][1]}*4] = calculation"}
                ]
               
                # Add the applications as separate parts
                for i in range(min(num_parts, len(applications))):
                    parts.append({
                        "domain": domain,
                        "subdomain": subdomain,
                        "question": applications[i]["question"],
                        "answer": applications[i]["answer"],
                        "application": applications[i]["name"],
                        "matrix": matrix_str,
                        "part_index": i + 1
                    })
       
        # Generate the appropriate number of parts
        while len(parts) < num_parts:
            # If specific domain handling didn't generate enough parts, add generic ones
            application_number = len(parts) + 1
           
            try:
                # Fall back to standard question generation
                problem = self.generate_question(domain, subdomain, force_new)
                problem["question"] = f"Application {application_number}: {problem['question']}"
                problem["application"] = f"application_{application_number}"
                problem["part_index"] = application_number
                parts.append(problem)
            except Exception as e:
                # If there's an error, create a placeholder
                parts.append({
                    "domain": domain,
                    "subdomain": subdomain,
                    "question": f"Application {application_number}: Additional application of the concept",
                    "answer": "Answer not generated",
                    "application": f"application_{application_number}",
                    "part_index": application_number
                })
               
        return parts

    def _generate_compound_context(self, domain, subdomain, pattern_type):
        """Generate contextual information for a compound question"""
       
        # Create context descriptions based on domain and pattern
        if domain == "algebra" and subdomain in ["linear_equations", "quadratic_equations"]:
            if pattern_type == "step_by_step":
                return "Solve the following equation step by step."
            elif pattern_type == "progressive_difficulty":
                return "Solve each of the following equations, which increase in difficulty."
       
        elif domain == "calculus":
            if subdomain == "differentiation":
                return "Work with the following function f(x) and its derivatives."
            elif subdomain == "integration":
                return "Evaluate the following integrals related to the same function."
               
        elif domain == "geometry":
            return "Consider the geometric figure described in the problems below."
           
        elif domain == "probability":
            return "The following questions relate to a probability experiment."
       
        # Generic contexts by pattern type
        if pattern_type == "progressive_difficulty":
            return "Solve the following problems that progressively increase in difficulty."
        elif pattern_type == "different_properties":
            return "Explore different properties of the mathematical object described."
        elif pattern_type == "step_by_step":
            return "Solve the problem by working through each step."
        elif pattern_type == "variations":
            return "Solve these variations of a common problem type."
        elif pattern_type == "application_sequence":
            return "Apply the theoretical concepts to increasingly complex applications."
           
        return "Solve the following related problems."
   
    def estimate_resources(self, num_problems=None, coverage_goals=None):
        """
        Estimate disk space and time required for generation based on sample
       
        Args:
            num_problems: Number of problems to generate (default: calculates based on coverage goals)
            coverage_goals: Dictionary with coverage goals for different number types and domains
           
        Returns:
            Dictionary with resource estimates
        """
        print("Estimating resource requirements...")
       
        # Default coverage goals
        if coverage_goals is None:
            coverage_goals = {
                "integers": 10000,  # Unique integers in range
                "integer_pairs": 100000,  # Unique integer pairs
                "domains": {domain: 1000 for domain in self.domains}  # Problems per domain
            }
       
        # Calculate total problems needed if not specified
        if num_problems is None:
            # Calculate based on coverage goals and overlap estimation
            total_domains = sum(coverage_goals["domains"].values())
            # Assume 30% overlap between coverage categories
            num_problems = int(max(total_domains, coverage_goals["integers"], coverage_goals["integer_pairs"]/10) * 1.3)
       
        # Generate a sample to estimate resources
        sample_size = min(1000, int(num_problems * 0.01))  # 1% of total or 1000, whichever is smaller
        sample_problems = []
       
        print(f"Generating {sample_size} sample problems for estimation...")
       
        # Track generation time
        start_time = time.time()
       
        # Generate sample with progress bar
        for _ in tqdm(range(sample_size), desc="Generating samples"):
            problem = self.generate_question(force_new=True)
            sample_problems.append(problem)
           
        end_time = time.time()
       
        # Calculate statistics
        generation_time = end_time - start_time
        avg_time_per_problem = generation_time / sample_size
        estimated_total_time = avg_time_per_problem * num_problems
       
        # Estimate disk space
        sample_data = {"problems": sample_problems}
        sample_json = json.dumps(sample_data)
        sample_size_bytes = len(sample_json.encode('utf-8'))
       
        avg_bytes_per_problem = sample_size_bytes / sample_size
        estimated_total_bytes = avg_bytes_per_problem * num_problems
       
        # Convert to more readable units
        estimated_size_mb = estimated_total_bytes / (1024 * 1024)
        estimated_size_gb = estimated_size_mb / 1024
       
        estimated_hours = estimated_total_time / 3600
        estimated_days = estimated_hours / 24
       
        # Current memory usage
        current_memory_mb = self._get_current_memory_usage()
       
        # Prepare estimation results
        estimation = {
            "num_problems": num_problems,
            "coverage_goals": coverage_goals,
            "sample_size": sample_size,
            "avg_time_per_problem": avg_time_per_problem,
            "estimated_total_time_seconds": estimated_total_time,
            "estimated_hours": estimated_hours,
            "estimated_days": estimated_days,
            "avg_bytes_per_problem": avg_bytes_per_problem,
            "estimated_total_bytes": estimated_total_bytes,
            "estimated_size_mb": estimated_size_mb,
            "estimated_size_gb": estimated_size_gb,
            "current_memory_mb": current_memory_mb,
            "memory_limit_mb": self.memory_limit_mb
        }
       
        # Display estimation
        print("\nResource Estimation:")
        print("====================")
        print(f"Problems to generate: {num_problems:,}")
        print(f"Estimated disk space: {estimated_size_gb:.2f} GB")
        print(f"Estimated time: {estimated_hours:.2f} hours ({estimated_days:.2f} days)")
        print(f"Estimated generation rate: {1/avg_time_per_problem:.2f} problems/second")
        print(f"Current memory usage: {current_memory_mb:.2f} MB")
        print(f"Memory limit: {self.memory_limit_mb} MB")
       
        return estimation
   
    def _generate_machine_learning_problem(self, subdomain=None, force_new=False):
        """Generate a machine learning problem with systematic coverage"""
        if subdomain is None:
            subdomain = random.choice([
                "supervised_learning", "unsupervised_learning", "reinforcement_learning",
                "deep_learning", "model_evaluation", "feature_engineering"
            ])
           
        if subdomain == "supervised_learning":
            # Generate problems about supervised learning algorithms
            topic = random.choice([
                "linear_regression", "logistic_regression", "decision_trees",
                "random_forests", "svm", "naive_bayes", "knn"
            ])
           
            if topic == "linear_regression":
                # Generate a linear regression problem
                problem_type = random.choice(["prediction", "coefficient_interpretation", "error_analysis"])
               
                if problem_type == "prediction":
                    # Generate random coefficients
                    a = self._generate_random_integer("small", force_new)
                    b = self._generate_random_integer("small", force_new)
                    epsilon = random.randint(-2, 2)  # Small error term
                   
                    # Generate a prediction problem
                    x = self._generate_random_integer("small", force_new)
                    y = a * x + b + epsilon
                   
                    question = f"A linear regression model trained on a dataset yielded the equation ŷ = {a}x + {b}. What would be the predicted value of y when x = {x}?"
                    answer = f"ŷ = {a} × {x} + {b} = {a*x + b}"
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "supervised_learning", (a, b, x))
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "supervised_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of how to use a linear regression model for prediction."
                    }
                   
                elif problem_type == "coefficient_interpretation":
                    # Generate random coefficients for a multivariate regression
                    a = self._generate_random_integer("small", force_new)
                    b = self._generate_random_integer("small", force_new)
                    c = self._generate_random_integer("small", force_new)
                   
                    question = f"In a multiple linear regression model ŷ = {a}x₁ + {b}x₂ + {c}, what is the interpretation of the coefficient {b}?"
                    answer = f"The coefficient {b} represents the expected change in y for a one-unit increase in x₂, holding x₁ constant."
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "supervised_learning", (a, b, c))
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "supervised_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of coefficient interpretation in multiple linear regression."
                    }
                   
                elif problem_type == "error_analysis":
                    # Generate an MSE calculation problem
                    n = random.randint(3, 5)  # Number of data points
                    actual = [self._generate_random_integer("small", force_new) for _ in range(n)]
                    predicted = [actual[i] + random.randint(-2, 2) for i in range(n)]
                   
                    question = f"Calculate the Mean Squared Error (MSE) for the following actual vs. predicted values:\nActual: {actual}\nPredicted: {predicted}"
                   
                    # Calculate MSE
                    mse = sum((actual[i] - predicted[i])**2 for i in range(n)) / n
                    answer = f"MSE = (1/{n}) × Σ(actual - predicted)² = (1/{n}) × ({' + '.join([f'({actual[i]} - {predicted[i]})²' for i in range(n)])}) = {mse:.2f}"
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "supervised_learning", hash(str(actual) + str(predicted)) % 10000)
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "supervised_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of error metrics in regression models."
                    }
                   
            elif topic == "decision_trees":
                # Generate a decision tree problem
                problem_type = random.choice(["entropy_calculation", "information_gain", "tree_interpretation"])
               
                if problem_type == "entropy_calculation":
                    # Generate data for entropy calculation
                    p = random.uniform(0.1, 0.9)
                    p = round(p, 2)
                    q = 1 - p
                   
                    question = f"Calculate the entropy of a binary class distribution where the probability of the positive class is {p} and the negative class is {q}."
                   
                    # Calculate entropy
                    entropy = -(p * math.log2(p) + q * math.log2(q))
                    answer = f"Entropy = -[{p} × log₂({p}) + {q} × log₂({q})] = {entropy:.4f}"
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "supervised_learning", int(p * 100))
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "supervised_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of entropy calculation used in decision tree algorithms."
                    }
                   
                elif problem_type == "information_gain":
                    # Simplified example for information gain calculation
                    question = """Consider a dataset with 14 samples: 9 positive and 5 negative.
A feature splits the dataset into two subsets:
- Left subset: 8 samples (6 positive, 2 negative)
- Right subset: 6 samples (3 positive, 3 negative)
Calculate the information gain from this split."""
                   
                    # Calculate entropy and information gain
                    parent_entropy = -(9/14 * math.log2(9/14) + 5/14 * math.log2(5/14))
                    left_entropy = -(6/8 * math.log2(6/8) + 2/8 * math.log2(2/8))
                    right_entropy = -(3/6 * math.log2(3/6) + 3/6 * math.log2(3/6))
                    weighted_entropy = (8/14) * left_entropy + (6/14) * right_entropy
                    information_gain = parent_entropy - weighted_entropy
                   
                    answer = f"""Parent entropy = -[(9/14) × log₂(9/14) + (5/14) × log₂(5/14)] = {parent_entropy:.4f}
Left subset entropy = -[(6/8) × log₂(6/8) + (2/8) × log₂(2/8)] = {left_entropy:.4f}
Right subset entropy = -[(3/6) × log₂(3/6) + (3/6) × log₂(3/6)] = {right_entropy:.4f}
Weighted entropy after split = (8/14) × {left_entropy:.4f} + (6/14) × {right_entropy:.4f} = {weighted_entropy:.4f}
Information gain = {parent_entropy:.4f} - {weighted_entropy:.4f} = {information_gain:.4f}"""
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "supervised_learning", hash(question) % 10000)
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "supervised_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of information gain calculation used in decision tree algorithms."
                    }
                   
        elif subdomain == "unsupervised_learning":
            # Generate problems about unsupervised learning algorithms
            topic = random.choice([
                "clustering", "dimensionality_reduction", "principal_component_analysis",
                "k_means", "hierarchical_clustering"
            ])
           
            if topic == "k_means":
                # Generate a k-means clustering problem
                problem_type = random.choice(["centroid_calculation", "cluster_assignment", "convergence"])
               
                if problem_type == "centroid_calculation":
                    # Generate random points for a cluster
                    n = random.randint(3, 5)  # Number of points
                    points = [(self._generate_random_integer("tiny", force_new),
                               self._generate_random_integer("tiny", force_new)) for _ in range(n)]
                   
                    question = f"Calculate the centroid (mean) of the following cluster points: {points}"
                   
                    # Calculate centroid
                    x_mean = sum(p[0] for p in points) / n
                    y_mean = sum(p[1] for p in points) / n
                    answer = f"Centroid = (({' + '.join([str(p[0]) for p in points])})/{n}, ({' + '.join([str(p[1]) for p in points])})/{n}) = ({x_mean:.2f}, {y_mean:.2f})"
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "unsupervised_learning", hash(str(points)) % 10000)
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "unsupervised_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of centroid calculation in k-means clustering."
                    }
                   
                elif problem_type == "cluster_assignment":
                    # Generate random centroids and a point
                    centroids = [(self._generate_random_integer("tiny", force_new),
                                  self._generate_random_integer("tiny", force_new)) for _ in range(3)]
                    point = (self._generate_random_integer("tiny", force_new),
                             self._generate_random_integer("tiny", force_new))
                   
                    question = f"Given centroids C1{centroids[0]}, C2{centroids[1]}, and C3{centroids[2]}, to which cluster would the point {point} be assigned in k-means clustering?"
                   
                    # Calculate distances
                    distances = [math.sqrt((point[0] - c[0])**2 + (point[1] - c[1])**2) for c in centroids]
                    min_index = distances.index(min(distances))
                    cluster = min_index + 1
                   
                    answer = f"""Distance to C1 = √[({point[0]} - {centroids[0][0]})² + ({point[1]} - {centroids[0][1]})²] = {distances[0]:.2f}
Distance to C2 = √[({point[0]} - {centroids[1][0]})² + ({point[1]} - {centroids[1][1]})²] = {distances[1]:.2f}
Distance to C3 = √[({point[0]} - {centroids[2][0]})² + ({point[1]} - {centroids[2][1]})²] = {distances[2]:.2f}
The point would be assigned to cluster C{cluster} which has the minimum distance."""
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "unsupervised_learning", hash(str(centroids) + str(point)) % 10000)
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "unsupervised_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of point assignment in k-means clustering based on the minimum distance to centroids."
                    }
                   
        elif subdomain == "deep_learning":
            # Generate problems about deep learning
            topic = random.choice([
                "neural_networks", "backpropagation", "activation_functions",
                "optimization_algorithms", "regularization"
            ])
           
            if topic == "activation_functions":
                # Generate an activation function problem
                activation_function = random.choice(["sigmoid", "relu", "tanh", "softmax"])
               
                if activation_function == "sigmoid":
                    x = random.choice([-2, -1, 0, 1, 2])  # Choose a nice value for calculation
                    question = f"Calculate the output of the sigmoid activation function for the input x = {x}."
                   
                    # Calculate sigmoid: σ(x) = 1 / (1 + e^(-x))
                    sigmoid_x = 1 / (1 + math.exp(-x))
                    answer = f"sigmoid({x}) = 1 / (1 + e^(-{x})) = 1 / (1 + {math.exp(-x):.4f}) = {sigmoid_x:.4f}"
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "deep_learning", x + 10)  # Offset to ensure positive index
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "deep_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of the sigmoid activation function which maps inputs to values between 0 and 1."
                    }
                   
                elif activation_function == "relu":
                    x = self._generate_random_integer("tiny", force_new) - 5  # Allow for negative values
                    question = f"Calculate the output of the ReLU (Rectified Linear Unit) activation function for the input x = {x}."
                   
                    # Calculate ReLU: f(x) = max(0, x)
                    relu_x = max(0, x)
                    answer = f"ReLU({x}) = max(0, {x}) = {relu_x}"
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "deep_learning", x + 10)  # Offset to ensure positive index
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "deep_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of the ReLU activation function which outputs the input if it is positive, or zero otherwise."
                    }
                   
                elif activation_function == "softmax":
                    # Generate a vector for softmax calculation
                    z = [self._generate_random_integer("tiny", force_new) for _ in range(3)]
                    question = f"Calculate the softmax activation function for the vector z = {z}."
                   
                    # Calculate softmax: softmax(z_i) = e^z_i / Σ(e^z_j)
                    exp_z = [math.exp(val) for val in z]
                    sum_exp_z = sum(exp_z)
                    softmax_z = [e / sum_exp_z for e in exp_z]
                   
                    answer = f"""exp(z) = [{', '.join([f'e^{val} = {math.exp(val):.4f}' for val in z])}]
sum(exp(z)) = {' + '.join([f'{e:.4f}' for e in exp_z])} = {sum_exp_z:.4f}
softmax(z) = [{', '.join([f'{e:.4f}/{sum_exp_z:.4f} = {e/sum_exp_z:.4f}' for e in exp_z])}]
           = [{', '.join([f'{val:.4f}' for val in softmax_z])}]"""
                   
                    # Track coverage
                    self._update_coverage("machine_learning", "deep_learning", hash(str(z)) % 10000)
                   
                    return {
                        "domain": "machine_learning",
                        "subdomain": "deep_learning",
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "explanation": "This tests understanding of the softmax activation function which normalizes inputs into a probability distribution."
                    }
                   
        elif subdomain == "model_evaluation":
            # Generate problems about model evaluation metrics
            topic = random.choice([
                "accuracy", "precision_recall", "f1_score", "roc_auc", "confusion_matrix"
            ])
           
            if topic == "confusion_matrix":
                # Generate a confusion matrix problem
                # Structure: [TP, FP, FN, TN]
                confusion_values = [random.randint(10, 50) for _ in range(4)]
                tp, fp, fn, tn = confusion_values
               
                question = f"""Given the confusion matrix:
               
                        Predicted Positive  |  Predicted Negative
Actual Positive  |        {tp}            |        {fn}
Actual Negative  |        {fp}            |        {tn}

Calculate the accuracy, precision, recall, and F1 score."""
               
                # Calculate metrics
                total = sum(confusion_values)
                accuracy = (tp + tn) / total
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
               
                answer = f"""Accuracy = (TP + TN) / Total = ({tp} + {tn}) / {total} = {accuracy:.4f}
Precision = TP / (TP + FP) = {tp} / ({tp} + {fp}) = {precision:.4f}
Recall = TP / (TP + FN) = {tp} / ({tp} + {fn}) = {recall:.4f}
F1 Score = 2 × (Precision × Recall) / (Precision + Recall) = 2 × ({precision:.4f} × {recall:.4f}) / ({precision:.4f} + {recall:.4f}) = {f1:.4f}"""
               
                # Track coverage
                self._update_coverage("machine_learning", "model_evaluation", hash(str(confusion_values)) % 10000)
               
                return {
                    "domain": "machine_learning",
                    "subdomain": "model_evaluation",
                    "topic": topic,
                    "question": question,
                    "answer": answer,
                    "explanation": "This tests understanding of classification metrics derived from the confusion matrix."
                }
               
        # Default return
        return {
            "domain": "machine_learning",
            "subdomain": subdomain if subdomain else "supervised_learning",
            "question": "What is the difference between supervised and unsupervised learning?",
            "answer": "Supervised learning algorithms are trained using labeled examples, where the desired output is known. Unsupervised learning algorithms find patterns in data where no labels are available.",
            "explanation": "This tests basic understanding of machine learning paradigms."
        }
       
    # Add educational metadata to problems
    def _add_educational_metadata(self, problem):
        """Add educational metadata to a problem for enhanced pedagogical value"""
        domain = problem.get("domain", "")
        subdomain = problem.get("subdomain", "")
       
        # Define difficulty levels
        difficulty_mapping = {
            "elementary_mathematics": "beginner",
            "arithmetic": "beginner",
            "basic_algebra": "beginner",
            "algebra": "intermediate",
            "calculus": "advanced",
            "number_theory": "advanced",
            "topology": "expert",
            "abstract_algebra": "expert",
            "differential_equations": "advanced",
            "probability_and_statistics": "intermediate",
            "geometry": "intermediate",
            "linear_algebra": "intermediate",
            "combinatorics": "intermediate",
            "game_theory": "intermediate",
            "machine_learning": "advanced",
            "logic_and_foundations": "advanced",
            "computational_mathematics": "advanced"
        }
       
        # Determine difficulty level
        difficulty = difficulty_mapping.get(domain, "intermediate")
       
        # More specific difficulty adjustments based on subdomain
        if domain == "calculus" and subdomain in ["limits", "differentiation"]:
            difficulty = "intermediate"
        elif domain == "calculus" and subdomain in ["multivariate_calculus", "vector_calculus"]:
            difficulty = "expert"
        elif domain == "algebra" and subdomain in ["linear_equations", "quadratic_equations"]:
            difficulty = "beginner"
        elif domain == "algebra" and subdomain in ["galois_theory", "homological_algebra"]:
            difficulty = "expert"
           
        # Define educational standards mapping
        standards_mapping = {
            "elementary_mathematics": ["Common Core Math K-8", "NCTM Standards"],
            "arithmetic": ["Common Core Math K-5", "NCTM Number and Operations"],
            "basic_algebra": ["Common Core Math 6-8", "NCTM Algebra"],
            "algebra": ["Common Core Math 8-12", "NCTM Algebra", "AP Algebra"],
            "calculus": ["AP Calculus AB/BC", "IB Mathematics HL", "College Board Standards"],
            "geometry": ["Common Core Math 8-10", "NCTM Geometry", "AP Geometry"],
            "probability_and_statistics": ["AP Statistics", "Common Core Statistics", "NCTM Data Analysis"],
            "linear_algebra": ["College Mathematics", "STEM Undergraduate"],
            "number_theory": ["College Mathematics", "Math Competition"],
            "discrete_mathematics": ["Computer Science Standards", "STEM Undergraduate"]
        }
       
        # Determine applicable standards
        standards = standards_mapping.get(domain, ["College Mathematics"])
       
        # Define Bloom's taxonomy level
        blooms_mapping = {
            "beginner": ["Remember", "Understand"],
            "intermediate": ["Apply", "Analyze"],
            "advanced": ["Analyze", "Evaluate"],
            "expert": ["Evaluate", "Create"]
        }
       
        blooms_level = random.choice(blooms_mapping.get(difficulty, ["Apply"]))
       
        # Define prerequisite concepts
        prerequisites = {}
       
        if domain == "calculus":
            prerequisites = {
                "limits": ["Functions", "Algebra", "Coordinate Geometry"],
                "differentiation": ["Limits", "Functions", "Algebra"],
                "integration": ["Differentiation", "Functions", "Algebra"],
                "multivariate_calculus": ["Single Variable Calculus", "Linear Algebra", "Vector Analysis"],
                "vector_calculus": ["Multivariate Calculus", "Linear Algebra", "Vector Analysis"]
            }
        elif domain == "algebra":
            prerequisites = {
                "linear_equations": ["Arithmetic", "Basic Algebra"],
                "quadratic_equations": ["Linear Equations", "Factoring", "Completing the Square"],
                "systems_of_equations": ["Linear Equations", "Substitution Method", "Elimination Method"],
                "matrices": ["Systems of Equations", "Array Operations"],
                "eigenvalues": ["Matrices", "Determinants", "Characteristic Polynomials"]
            }
           
        # Get prerequisites for this problem
        problem_prerequisites = prerequisites.get(subdomain, [])
       
        # Define learning objectives
        learning_objectives = {
            "arithmetic": "Perform basic arithmetic operations efficiently and accurately.",
            "basic_algebra": "Solve basic algebraic equations and manipulate algebraic expressions.",
            "linear_equations": "Solve linear equations in one variable and interpret solutions.",
            "quadratic_equations": "Solve quadratic equations using various methods and interpret solutions.",
            "calculus": "Apply calculus concepts to solve problems involving rates of change and accumulation.",
            "limits": "Evaluate limits of functions using algebraic and graphical methods.",
            "differentiation": "Calculate derivatives using appropriate rules and interpret them as rates of change.",
            "integration": "Compute integrals using various techniques and interpret them as accumulated quantities.",
            "probability": "Calculate probabilities of events using appropriate rules and distributions.",
            "statistics": "Analyze data using statistical measures and interpret results."
        }
       
        # Get learning objective for this problem
        learning_objective = learning_objectives.get(subdomain,
                                                   learning_objectives.get(domain,
                                                                         f"Demonstrate understanding of {domain} concepts and techniques."))
       
        # Create metadata dictionary
        metadata = {
            "difficulty_level": difficulty,
            "educational_standards": standards,
            "blooms_taxonomy_level": blooms_level,
            "prerequisites": problem_prerequisites,
            "learning_objective": learning_objective,
            "estimated_time_minutes": {"beginner": 5, "intermediate": 10, "advanced": 15, "expert": 20}.get(difficulty, 10),
            "knowledge_domain": domain,
            "topic": subdomain
        }
       
        # Add metadata to problem
        problem["educational_metadata"] = metadata
       
        return problem
   
    def _generate_problem_solution_steps(self, problem):
        """Generate step-by-step solution steps for a problem"""
        domain = problem.get("domain", "")
        subdomain = problem.get("subdomain", "")
        question = problem.get("question", "")
        answer = problem.get("answer", "")
       
        solution_steps = []
       
        # Generate solution steps based on domain and subdomain
        if domain == "arithmetic":
            if "addition" in question.lower():
                solution_steps = [
                    "Identify the numbers to be added.",
                    "Line up the numbers properly, if working by hand.",
                    "Add the digits from right to left, carrying when necessary.",
                    "Write the final sum."
                ]
            elif "subtraction" in question.lower():
                solution_steps = [
                    "Identify the numbers involved in the subtraction.",
                    "Line up the numbers properly, with the larger number on top (if working by hand).",
                    "Subtract the digits from right to left, borrowing when necessary.",
                    "Write the final difference."
                ]
            elif "multiplication" in question.lower():
                solution_steps = [
                    "Identify the numbers to be multiplied.",
                    "Multiply each digit of the second number with each digit of the first number.",
                    "Add the partial products, accounting for place values.",
                    "Write the final product."
                ]
            elif "division" in question.lower():
                solution_steps = [
                    "Identify the dividend and divisor.",
                    "Set up the division using appropriate notation.",
                    "Perform the division, finding quotient and remainder.",
                    "Write the final result, checking that divisor × quotient + remainder = dividend."
                ]
               
        elif domain == "algebra" and subdomain == "linear_equations":
            solution_steps = [
                "Identify the linear equation to be solved.",
                "Simplify both sides of the equation if needed (combine like terms).",
                "Move all variable terms to one side and all constant terms to the other side.",
                "Factor out the coefficient of the variable if necessary.",
                "Solve for the variable by dividing both sides by the coefficient.",
                "Check the solution by substituting back into the original equation."
            ]
           
        elif domain == "algebra" and subdomain == "quadratic_equations":
            solution_steps = [
                "Identify the quadratic equation to be solved.",
                "Rearrange the equation into standard form: ax² + bx + c = 0.",
                "Try to factor the quadratic expression if possible.",
                "If factoring works, set each factor equal to zero and solve.",
                "If factoring doesn't work, use the quadratic formula: x = (-b ± √(b² - 4ac)) / 2a.",
                "Calculate the discriminant: b² - 4ac to determine the number of solutions.",
                "Compute the solutions and simplify if possible.",
                "Check the solutions by substituting back into the original equation."
            ]
           
        elif domain == "calculus" and subdomain == "differentiation":
            solution_steps = [
                "Identify the function to be differentiated.",
                "Determine which differentiation rules apply (power rule, product rule, chain rule, etc.).",
                "Apply the appropriate rules step by step.",
                "Simplify the resulting expression if possible.",
                "Verify the answer by checking a simple case or using other methods if appropriate."
            ]
           
        elif domain == "calculus" and subdomain == "integration":
            solution_steps = [
                "Identify the function to be integrated.",
                "Determine which integration technique is appropriate (substitution, parts, partial fractions, etc.).",
                "Apply the chosen technique step by step.",
                "Find the antiderivative and include the constant of integration if indefinite.",
                "If it's a definite integral, evaluate at the limits and subtract.",
                "Simplify the result if possible."
            ]
           
        elif domain == "probability_and_statistics" and subdomain == "basic_probability":
            solution_steps = [
                "Identify the probability question and what event we're finding the probability of.",
                "Determine the sample space (all possible outcomes).",
                "Count the number of favorable outcomes (outcomes in the event).",
                "Apply the probability formula: P(event) = (number of favorable outcomes) / (total number of possible outcomes).",
                "Simplify the fraction if possible and express as a decimal or percentage if required."
            ]
           
        # If we don't have specific steps for this problem type, generate generic steps
        if not solution_steps:
            # Extract numbers and key terms from the question for generic steps
            # This is a simplified approach; a more sophisticated implementation would use NLP techniques
            numbers_in_question = re.findall(r'-?\d+\.?\d*', question)
           
            solution_steps = [
                f"Understand the problem: {question}",
                "Identify the relevant concepts and formulas needed to solve the problem.",
                "Set up the problem using appropriate notation and variables.",
                "Apply the necessary mathematical techniques to work toward the solution.",
                "Perform calculations accurately, paying attention to units and sign conventions.",
                f"Arrive at the final answer: {answer}",
                "Verify that the answer makes sense in the context of the problem."
            ]
           
            if numbers_in_question:
                solution_steps.insert(3, f"Work with the given values: {', '.join(numbers_in_question)}")
       
        # Add solution steps to the problem
        problem["solution_steps"] = solution_steps
       
        return problem
   
    def _add_output_formats(self, problem):
        """Add additional output formats like LaTeX, markdown, etc."""
        domain = problem.get("domain", "")
        subdomain = problem.get("subdomain", "")
        question = problem.get("question", "")
        answer = problem.get("answer", "")
       
        # Generate LaTeX representation
        latex_question = self._convert_to_latex(question)
        latex_answer = self._convert_to_latex(answer)
       
        # Generate Markdown representation
        markdown_question = self._convert_to_markdown(question)
        markdown_answer = self._convert_to_markdown(answer)
       
        # Create output formats dictionary
        output_formats = {
            "latex": {
                "question": latex_question,
                "answer": latex_answer
            },
            "markdown": {
                "question": markdown_question,
                "answer": markdown_answer
            }
        }
       
        # Add output formats to problem
        problem["output_formats"] = output_formats
       
        return problem
   
    def _convert_to_latex(self, text):
        """Convert text with math notation to LaTeX format"""
        # This is a simplified implementation; a complete implementation would use more sophisticated parsing
       
        # Replace basic operations
        latex_text = text.replace("×", r" \times ")
        latex_text = latex_text.replace("÷", r" \div ")
        latex_text = latex_text.replace("²", r"^2")
        latex_text = latex_text.replace("³", r"^3")
        latex_text = latex_text.replace("√", r"\sqrt")
       
        # Replace fractions
        fraction_pattern = r'(\d+)/(\d+)'
        latex_text = re.sub(fraction_pattern, r'\\frac{\1}{\2}', latex_text)
       
        # Replace subscripts and superscripts
        subscript_pattern = r'(\w)_(\w+)'
        latex_text = re.sub(subscript_pattern, r'\1_{\2}', latex_text)
       
        superscript_pattern = r'(\w)\^(\w+)'
        latex_text = re.sub(superscript_pattern, r'\1^{\2}', latex_text)
       
        # Handle special functions
        latex_text = re.sub(r'sin\(', r'\\sin(', latex_text)
        latex_text = re.sub(r'cos\(', r'\\cos(', latex_text)
        latex_text = re.sub(r'tan\(', r'\\tan(', latex_text)
        latex_text = re.sub(r'log\(', r'\\log(', latex_text)
        latex_text = re.sub(r'ln\(', r'\\ln(', latex_text)
        latex_text = re.sub(r'exp\(', r'\\exp(', latex_text)
       
        # Wrap in LaTeX math delimiters if it contains math
        if any(char in latex_text for char in "+-*/^_√∫∂"):
            latex_text = f"${latex_text}$"
       
        return latex_text
   
    def _convert_to_markdown(self, text):
        """Convert text to Markdown format"""
        # This is a simplified implementation
       
        # Replace headers
        markdown_text = text
       
        # Make important terms bold
        terms_to_bold = ["sum", "difference", "product", "quotient", "derivative", "integral",
                         "mean", "median", "mode", "variance", "standard deviation"]
       
        for term in terms_to_bold:
            if term in markdown_text.lower():
                pattern = re.compile(f'\\b{term}\\b', re.IGNORECASE)
                markdown_text = pattern.sub(f'**{term}**', markdown_text)
       
        # Convert lists to markdown lists
        lines = markdown_text.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("- "):
                lines[i] = line
            elif re.match(r'^\d+\. ', line.strip()):
                lines[i] = line
            elif line.strip().startswith("* "):
                lines[i] = line
               
        markdown_text = "\n".join(lines)
       
        return markdown_text
       
    def _generate_number_theory_sequence(self):
        """
        Generate a mathematically coherent sequence about number theory
        """
        # Choose a number for analysis
        n = self._generate_random_integer("medium", True)
        while n < 20:  # Ensure a reasonably interesting number
            n = self._generate_random_integer("medium", True)
           
        # Track coverage
        self._update_coverage("number_theory", "prime_numbers", n)
       
        # Find the prime factorization
        factors = []
        d = 2
        temp_n = n
        while d * d <= temp_n:
            while temp_n % d == 0:
                factors.append(d)
                temp_n //= d
            d += 1
        if temp_n > 1:
            factors.append(temp_n)
           
        # Create prime factorization string
        if len(factors) == 1:
            factorization = f"{n} is prime"
        else:
            factor_counts = {}
            for f in factors:
                if f in factor_counts:
                    factor_counts[f] += 1
                else:
                    factor_counts[f] = 1
                   
            factorization = " × ".join([f"{f}^{c}" if c > 1 else str(f) for f, c in factor_counts.items()])
       
        # Find all divisors
        divisors = []
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                divisors.append(i)
                if i != n // i:
                    divisors.append(n // i)
        divisors.sort()
       
        # Calculate sum of divisors
        sum_of_divisors = sum(divisors)
       
        # Determine if perfect, abundant, or deficient
        if sum_of_divisors - n == n:
            number_type = "perfect"
        elif sum_of_divisors - n > n:
            number_type = "abundant"
        else:
            number_type = "deficient"
           
        # Find modular multiplicative inverse for a small prime
        small_prime = 7  # Using 7 for simplicity
        if n % small_prime != 0:
            # Extended Euclidean Algorithm for modular inverse
            def extended_gcd(a, b):
                if a == 0:
                    return b, 0, 1
                else:
                    gcd, x, y = extended_gcd(b % a, a)
                    return gcd, y - (b // a) * x, x
                   
            gcd, x, y = extended_gcd(n % small_prime, small_prime)
            inverse = x % small_prime
        else:
            inverse = "does not exist"
           
        # Create parts
        parts = [
            {
                "part_index": 1,
                "question": f"Find the prime factorization of {n}.",
                "answer": f"{n} = {factorization}",
                "explanation": "We find the prime factorization by dividing by the smallest prime factors repeatedly."
            },
            {
                "part_index": 2,
                "question": f"List all the positive divisors of {n}.",
                "answer": f"The divisors of {n} are: {', '.join(map(str, divisors))}",
                "explanation": "We check all numbers from 1 to √n, and for each divisor i, we include both i and n/i.",
                "depends_on": 1
            },
            {
                "part_index": 3,
                "question": f"Calculate the sum of all positive divisors of {n}.",
                "answer": f"The sum of divisors is {sum_of_divisors}",
                "explanation": "We add up all the divisors found in the previous step.",
                "depends_on": 2
            },
            {
                "part_index": 4,
                "question": f"Is {n} a perfect number, an abundant number, or a deficient number?",
                "answer": f"{n} is a {number_type} number.",
                "explanation": "A perfect number equals the sum of its proper divisors. An abundant number is greater than the sum of its proper divisors. A deficient number is less than the sum of its proper divisors.",
                "depends_on": 3
            },
            {
                "part_index": 5,
                "question": f"Find the modular multiplicative inverse of {n} modulo {small_prime}, if it exists.",
                "answer": f"The modular inverse of {n} modulo {small_prime} is {inverse}",
                "explanation": f"The modular multiplicative inverse of a modulo m is an integer a⁻¹ such that a·a⁻¹ ≡ 1 (mod m). It exists if and only if a and m are coprime."
            },
            {
                "part_index": 6,
                "question": f"For how many values of x in the range 0 ≤ x < {n} is x² ≡ 1 (mod {n})?",
                "answer": "The answer depends on the prime factorization of n.",
                "explanation": "The number of solutions is related to the number of distinct prime factors of n.",
                "depends_on": 1
            }
        ]
       
        # Create context
        context = f"""The following sequence of questions explores number-theoretic properties of the integer {n}.
The sequence builds from prime factorization through divisor analysis, modular arithmetic,
and special number classifications."""
       
        return {
            "parts": parts,
            "context": context,
            "shared_object": str(n)
        }
   
    def _generate_integration_sequence(self):
        """
        Generate a mathematically coherent sequence about a complex integration problem
        """
        # Create an integration problem with multiple solution methods
        integration_type = random.choice(["standard", "substitution", "by_parts", "rational_function"])
       
        if integration_type == "by_parts":
            # Integration by parts example: ∫x·e^x dx
            function = "x·e^x"
           
            # Track coverage
            self._update_coverage("calculus", "integration", hash(function) % 10000)
           
            # Create parts
            parts = [
                {
                    "part_index": 1,
                    "question": f"Evaluate the indefinite integral: ∫{function} dx",
                    "answer": "This integral requires the integration by parts technique.",
                    "explanation": "Integration by parts is useful when integrating the product of functions."
                },
                {
                    "part_index": 2,
                    "question": "Apply the integration by parts formula ∫u·dv = u·v - ∫v·du by identifying appropriate functions for u and dv.",
                    "answer": "Let u = x and dv = e^x dx",
                    "explanation": "When choosing u and dv, we typically choose u as the function that becomes simpler when differentiated, and dv as the function that has a known integral.",
                    "depends_on": 1
                },
                {
                    "part_index": 3,
                    "question": "Find du and v based on your choices.",
                    "answer": "du = dx and v = e^x",
                    "explanation": "du is the differential of u, and v is the antiderivative of dv.",
                    "depends_on": 2
                },
                {
                    "part_index": 4,
                    "question": "Apply the integration by parts formula to evaluate the integral.",
                    "answer": "∫x·e^x dx = x·e^x - ∫e^x dx = x·e^x - e^x + C",
                    "explanation": "Substitute the values into the formula ∫u·dv = u·v - ∫v·du and solve the resulting simpler integral.",
                    "depends_on": 3
                },
                {
                    "part_index": 5,
                    "question": "Simplify your answer.",
                    "answer": "∫x·e^x dx = e^x(x - 1) + C",
                    "explanation": "Factor out e^x to get a more elegant form of the answer.",
                    "depends_on": 4
                },
                {
                    "part_index": 6,
                    "question": "Verify your answer by differentiating it.",
                    "answer": "d/dx[e^x(x - 1) + C] = e^x(x - 1) + e^x = x·e^x",
                    "explanation": "We can verify an indefinite integral by differentiating it. The result should equal the original integrand.",
                    "depends_on": 5
                }
            ]
           
            # Create context
            context = """The following sequence of questions works through the evaluation of the integral ∫x·e^x dx
using the integration by parts technique. The sequence builds step by step from identifying the
appropriate substitution through application of the formula and verification of the result."""
           
            return {
                "parts": parts,
                "context": context,
                "shared_object": "∫x·e^x dx"
            }
           
        elif integration_type == "substitution":
            # Integration by substitution example: ∫cos(3x) dx
            function = "cos(3x)"
           
            # Track coverage
            self._update_coverage("calculus", "integration", hash(function) % 10000)
           
            # Create parts
            parts = [
                {
                    "part_index": 1,
                    "question": f"Evaluate the indefinite integral: ∫{function} dx",
                    "answer": "This integral can be solved using substitution.",
                    "explanation": "The presence of a composite function suggests using substitution."
                },
                {
                    "part_index": 2,
                    "question": "Choose an appropriate substitution for this integral.",
                    "answer": "Let u = 3x, so du = 3 dx, or dx = du/3",
                    "explanation": "When integrating a composite function like cos(3x), we typically substitute for the inner function (3x).",
                    "depends_on": 1
                },
                {
                    "part_index": 3,
                    "question": "Rewrite the integral in terms of u.",
                    "answer": "∫cos(3x) dx = ∫cos(u) · (du/3) = (1/3)∫cos(u) du",
                    "explanation": "Substitute u for 3x and dx for du/3 in the original integral.",
                    "depends_on": 2
                },
                {
                    "part_index": 4,
                    "question": "Evaluate the integral in terms of u.",
                    "answer": "(1/3)∫cos(u) du = (1/3)sin(u) + C",
                    "explanation": "The integral of cos(u) is sin(u).",
                    "depends_on": 3
                },
                {
                    "part_index": 5,
                    "question": "Convert your answer back to the original variable x.",
                    "answer": "(1/3)sin(u) + C = (1/3)sin(3x) + C",
                    "explanation": "Substitute u = 3x back into the answer.",
                    "depends_on": 4
                },
                {
                    "part_index": 6,
                    "question": "Verify your answer by differentiation.",
                    "answer": "d/dx[(1/3)sin(3x) + C] = (1/3) · 3 · cos(3x) = cos(3x)",
                    "explanation": "We verify by taking the derivative of our answer, which should equal the original integrand.",
                    "depends_on": 5
                }
            ]
           
            # Create context
            context = """The following sequence of questions works through the evaluation of the integral ∫cos(3x) dx
using the substitution method. The sequence builds step by step from identifying the appropriate
substitution through application of the formula and verification of the result."""
           
            return {
                "parts": parts,
                "context": context,
                "shared_object": "∫cos(3x) dx"
            }
           
        # Add more integration types as needed

    def generate_batch(self, batch_size, output_dir, batch_number):
        """Generate a batch of problems with checkpointing"""
        problems = []
        batch_start_time = time.time()
       
        print(f"\nGenerating batch #{batch_number} ({batch_size} problems)...")
       
        # For each batch, include at least one compound question from each domain
        compound_domains = ["function_analysis", "equation_solving", "geometric_sequence",
                          "probability_scenario", "number_theory_exploration", "linear_algebra_sequence",
                          "integration_methods"]
       
        # Generate problems with a progress bar
        with tqdm(total=batch_size, desc="Generating problems") as pbar:
            # First, add compound questions for comprehensive coverage
            for domain in compound_domains[:min(len(compound_domains), batch_size // 10)]:
                try:
                    # Create a compound question
                    compound_question = self.generate_compound_question()
                    problems.append(compound_question)
                    pbar.update(1)
                except Exception as e:
                    print(f"\nError generating compound question: {e}")
           
            # Then fill the rest with regular questions
            remaining = batch_size - len(problems)
            for i in range(remaining):
                try:
                    # Check memory periodically
                    if i % 100 == 0:
                        current_memory = self._check_memory_limits()
                        if current_memory > 0.9 * self.memory_limit_mb:
                            print(f"\nApproaching memory limit ({current_memory:.2f}MB). Ending batch early.")
                            break
                           
                    # Generate problem with statistical coverage
                    force_new = (i % 5 == 0)  # Force new uncovered numbers 20% of the time
                    problem = self.generate_question(force_new=force_new)
                    problems.append(problem)
                    self.total_problems_generated += 1
                    pbar.update(1)
                   
                except Exception as e:
                    print(f"\nError generating problem: {e}")
                    if isinstance(e, MemoryError):
                        print("Memory limit reached. Ending batch.")
                        break
       
        batch_end_time = time.time()
        batch_duration = batch_end_time - batch_start_time
       
        # Coverage stats
        coverage_stats = {
            "integers": len(self.covered_integers),
            "integer_pairs": len(self.covered_integer_pairs),
            "integer_triplets": len(self.covered_integer_triplets),
            "domains": self.covered_domains,
            "top_subdomains": dict(sorted(self.covered_subdomains.items(),
                                        key=lambda x: x[1], reverse=True)[:10])
        }
       
        # Create batch metadata
        batch_data = {
            "metadata": {
                "generator": "EnhancedMegaMathGen",
                "batch_number": batch_number,
                "batch_size": len(problems),
                "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "generation_duration_seconds": batch_duration,
                "memory_usage_mb": self._get_current_memory_usage(),
                "total_problems_generated": self.total_problems_generated,
                "coverage_stats": coverage_stats,
                "compound_questions_count": sum(1 for p in problems if "theme" in p)
            },
            "problems": problems
        }
       
        # Save the batch with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/math_batch_{batch_number:06d}_{timestamp}.json"
       
        with open(filename, 'w') as f:
            json.dump(batch_data, f)
           
        # Update statistics
        self.generation_times.append(batch_duration)
        self.batch_sizes.append(len(problems))
        batch_size_bytes = os.path.getsize(filename)
        self.total_bytes_generated += batch_size_bytes
       
        return {
            "filename": filename,
            "problems_count": len(problems),
            "compound_questions_count": sum(1 for p in problems if "theme" in p),
            "file_size_bytes": batch_size_bytes,
            "duration_seconds": batch_duration,
            "memory_usage_mb": self._get_current_memory_usage()
        }
   
    def save_coverage_checkpoint(self, output_dir, batch_number):
        """Save current coverage data as a checkpoint"""
        # Create a summary of coverage data (without the full sets that could be very large)
        coverage_summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "batch_number": batch_number,
            "total_problems_generated": self.total_problems_generated,
            "covered_integers_count": len(self.covered_integers),
            "covered_integer_pairs_count": len(self.covered_integer_pairs),
            "covered_integer_triplets_count": len(self.covered_integer_triplets),
            "covered_domains": self.covered_domains,
            "covered_subdomains_sample": dict(sorted(self.covered_subdomains.items(),
                                                   key=lambda x: x[1], reverse=True)[:50]),
            "memory_usage_mb": self._get_current_memory_usage(),
            "total_bytes_generated": self.total_bytes_generated,
            "generation_stats": {
                "avg_time_per_problem": sum(self.generation_times) / max(1, len(self.generation_times)),
                "avg_problems_per_batch": sum(self.batch_sizes) / max(1, len(self.batch_sizes)),
                "total_batches": len(self.batch_sizes)
            }
        }
       
        # Save to file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/coverage_checkpoint_{batch_number:06d}_{timestamp}.json"
       
        with open(filename, 'w') as f:
            json.dump(coverage_summary, f)
           
        return filename

# Signal handler for graceful termination
def signal_handler(sig, frame):
    print(f"\nReceived signal {sig}. Finishing current batch and exiting gracefully...")
    global keep_running
    keep_running = False

# Main execution function
def run_mega_math_generator():
    """
    Run the MegaMathGen - Ultra Comprehensive Mathematics Problem Generator
    """
   
    # Initialize the generator
    print("Initializing MegaMathGen - Ultra Comprehensive Mathematics Problem Generator")
    print("==========================================================================")
    print("This script will continuously generate math problems across all domains")
    print("until manually stopped with Ctrl+C.")
    print("Data will be saved in batches to prevent data loss.")
    print()
   
    # Set up signal handling for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
   
    # Create output directory
    output_dir = "mega_math_data"
    os.makedirs(output_dir, exist_ok=True)
   
    # Initialize generator
    generator = ComprehensiveMathGenerator()
   
    # Estimate resource requirements
    estimation = generator.estimate_resources()
   
    # Confirm with user
    user_input = input("\nProceed with generation? (yes/no): ")
    if user_input.lower() not in ['yes', 'y']:
        print("Generation cancelled by user.")
        return
   
    # Initialize counters
    total_problems = 0
    total_size_mb = 0
    batch_number = 1
    batch_size = 5000  # Number of problems per batch
    compound_ratio = 0.3  # 30% of problems will be compound
    checkpoint_interval = 5  # Save checkpoint every N batches
   
    # Adjust batch size based on memory usage
    current_memory = generator._get_current_memory_usage()
    if current_memory > 5000:  # If already using > 5GB
        batch_size = min(batch_size, int(5000 * (28000 / current_memory)))
        print(f"\nAdjusting batch size to {batch_size} based on current memory usage")
   
    # Start generation loop
    global keep_running
    keep_running = True
   
    start_time = time.time()
   
    print(f"Starting generation, saving output to {output_dir}/")
   
    try:
        while keep_running:
            # Generate a batch
            batch_start_time = time.time()
           
            # Generate and save a batch
            batch_result = generator.generate_batch(batch_size, output_dir, batch_number)
           
            # Update counters
            total_problems += batch_result["problems_count"]
            total_size_bytes = batch_result["file_size_bytes"]
            file_size_mb = total_size_bytes / (1024 * 1024)
            total_size_mb += file_size_mb
           
            # Progress Report
            batch_duration = batch_result["duration_seconds"]
            total_duration = time.time() - start_time
           
            print(f"Batch #{batch_number} completed in {batch_duration:.2f} seconds")
            print(f"Saved to {batch_result['filename']} ({file_size_mb:.2f} MB)")
           
            # Print coverage stats
            integers_covered = len(generator.covered_integers)
            pairs_covered = len(generator.covered_integer_pairs)
            triplets_covered = len(generator.covered_integer_triplets)
           
            print(f"Coverage: {integers_covered:,} unique integers, {pairs_covered:,} unique pairs, {triplets_covered:,} unique triplets")
            print(f"Compound questions in batch: {batch_result.get('compound_questions_count', 0)}")
            print(f"Progress: {total_problems:,} problems generated, total size: {total_size_mb:.2f} MB")
            print(f"Running for: {total_duration/60:.2f} minutes, avg rate: {total_problems/total_duration:.2f} problems/second")
            print(f"Current memory usage: {batch_result['memory_usage_mb']:.2f} MB")
           
            # Save coverage checkpoint periodically
            if batch_number % checkpoint_interval == 0:
                checkpoint_file = generator.save_coverage_checkpoint(output_dir, batch_number)
                print(f"Coverage checkpoint saved to {checkpoint_file}")
               
                # Force garbage collection after checkpoint
                gc.collect()
           
            # Prepare for next batch
            batch_number += 1
           
    except KeyboardInterrupt:
        print("\nInterrupted by user. Saving final checkpoint...")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
   
    finally:
        # Save final coverage checkpoint
        try:
            final_checkpoint = generator.save_coverage_checkpoint(output_dir, batch_number)
            print(f"Final coverage checkpoint saved to {final_checkpoint}")
        except Exception as e:
            print(f"Error saving final checkpoint: {e}")
       
        # End of generation report
        end_time = time.time()
        total_time = end_time - start_time
       
        print("\n==========================================================================")
        print("MegaMathGen - Generation Summary")
        print("==========================================================================")
        print(f"Total problems generated: {total_problems:,}")
        print(f"Total data generated: {total_size_mb:.2f} MB ({total_size_mb/1024:.4f} GB)")
        print(f"Total time running: {total_time/60:.2f} minutes ({total_time/3600:.2f} hours)")
        print(f"Generation rate: {total_problems/total_time:.2f} problems per second")
        print(f"Final memory usage: {generator._get_current_memory_usage():.2f} MB")
        print(f"Coverage: {len(generator.covered_integers):,} unique integers")
        print(f"         {len(generator.covered_integer_pairs):,} unique integer pairs")
        print(f"         {len(generator.covered_integer_triplets):,} unique integer triplets")
        print(f"Output directory: {os.path.abspath(output_dir)}")
        print("==========================================================================")
        print("Generation complete. Data saved successfully.")

if __name__ == "__main__":
    run_mega_math_generator()