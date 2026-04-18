"""
Code-Dataset-Processor

This script generates a comprehensive dataset of code samples with multiple representations
for training AI models on software code. It produces a rich set of features including:

- Source code (multiple variants)
- Abstract Syntax Trees (ASTs)
- Control Flow Graphs (CFGs)
- Data Flow Graphs (DFGs)
- Program Dependence Graphs (PDGs)
- Dependency Graphs
- Bytecode compilation
- Execution traces
- Version history
- Code metrics and quality labels
- Algorithm and pattern detection
- Security vulnerability analysis
- Performance estimates
- Natural language descriptions

Usage:
    python Code-Dataset-Processor.py --target-size 1.0 --include-bugs
    python Code-Dataset-Processor.py --mode count --num-samples 500
"""

import os
import ast
import json
import random
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import logging
import argparse
import gzip
from collections import defaultdict
import py_compile
import marshal
import importlib.util
import dis
import base64
import tempfile
import sys
import traceback
import re
import math
import subprocess
from datetime import datetime

# Optional dependencies - will use if available
try:
    import radon.metrics
    import radon.complexity

    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False

try:
    import pylint.lint
    from pylint.reporters.text import TextReporter

    PYLINT_AVAILABLE = True
except ImportError:
    PYLINT_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CodeGenerator:
    """Generator for synthetic code samples in multiple languages and representations"""

    def __init__(self, seed=42):
        """Initialize the code generator with a random seed for reproducibility"""
        self.seed = seed
        random.seed(seed)
        self.operators = [
            "+",
            "-",
            "*",
            "/",
            "%",
            "==",
            "!=",
            "<",
            ">",
            "<=",
            ">=",
            "and",
            "or",
        ]
        self.variable_types = ["int", "float", "string", "bool", "list", "dict"]

        # Algorithm templates for recognition
        self.algorithm_templates = {
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
        }

        # Design pattern templates
        self.design_pattern_templates = {
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
            "insecure_random": {"pattern": r"random\.\w+\(\)", "severity": "low"},
        }

    def generate_variable_name(self, prefix="var"):
        """Generate a random variable name"""
        return f"{prefix}_{random.randint(1, 1000)}"

    def _process_expression(self, expr, parent_id, graph, variables):
        """Process expressions to connect variable uses to their definitions"""
        if isinstance(expr, ast.Name) and isinstance(expr.ctx, ast.Load):
            var_name = expr.id
            if var_name in variables and variables[var_name]:
                graph.add_edge(variables[var_name][-1], parent_id)
        elif isinstance(expr, ast.BinOp):
            self._process_expression(expr.left, parent_id, graph, variables)
            self._process_expression(expr.right, parent_id, graph, variables)
        elif isinstance(expr, ast.Call):
            for arg in expr.args:
                self._process_expression(arg, parent_id, graph, variables)

    def generate_sample(
        self, complexity=2, include_bugs=True, add_special_samples=True
    ):
        """Generate a complete code sample with all representations and advanced metrics"""
        # Decide if this should be a normal sample or include special patterns
        if add_special_samples and random.random() < 0.3:
            # Choose a special pattern to include
            pattern_type = random.choice(
                ["algorithm", "design_pattern", "vulnerability", "normal"]
            )

            if pattern_type == "algorithm":
                algo_type = random.choice(list(self.algorithm_templates.keys()))
                code = self.generate_algorithm_code(algo_type)
            elif pattern_type == "design_pattern":
                design_pattern = random.choice(list(self.design_pattern_templates.keys()))
                code = self.generate_design_pattern_code(design_pattern)
            elif pattern_type == "vulnerability":
                vuln_type = random.choice(list(self.security_vulnerabilities.keys()))
                code = self.generate_vulnerable_code(vuln_type)
            else:
                code = self.generate_script(complexity)
        else:
            code = self.generate_script(complexity)

        # Generate buggy version if requested
        buggy_code = self.generate_buggy_version(code) if include_bugs else None

        # Get AST
        ast_tree = self.generate_ast(code)
        if ast_tree is None:
            # Fall back to a simpler script if we had syntax issues
            code = self.generate_function(complexity)
            ast_tree = self.generate_ast(code)
            if ast_tree is None:
                logging.error("Failed to generate valid AST for both script and function")
                return None

        # Generate all representations
        ast_dict = self.ast_to_dict(ast_tree)

        # Generate graphs
        cfg = self.serialize_graph(self.generate_cfg(code))
        dfg = self.serialize_graph(self.generate_dfg(code))
        pdg = self.serialize_graph(self.generate_pdg(code))
        dep_graph = self.serialize_graph(self.generate_dependency_graph(code))

        # Generate version history
        version_history = self.generate_version_history(code, num_versions=3)

        # Generate compiled representations
        bytecode = self.generate_bytecode(code)
        execution_trace = self.generate_execution_trace(code)

        # Advanced analysis
        complexity_metrics = self.analyze_code_complexity(code)
        complexity_labels = self.analyze_complexity_labels(complexity_metrics)
        identified_algorithms = self.identify_algorithms(code)
        identified_patterns = self.identify_design_patterns(code)
        security_vulnerabilities = self.identify_security_vulnerabilities(code)
        performance_estimate = self.estimate_performance(code)

        # Generate natural language description
        nl_description = self.generate_natural_language_description(
            code,
            complexity_labels,
            identified_algorithms,
            identified_patterns,
            security_vulnerabilities,
        )

        # Build the complete sample with all metrics and labels
        sample = {
            "code": code,
            "buggy_code": buggy_code,
            "ast": ast_dict,
            "cfg": cfg,
            "dfg": dfg,
            "pdg": pdg,
            "dependency_graph": dep_graph,
            "version_history": version_history,
            "bytecode": bytecode,
            "execution_trace": execution_trace,
            "metrics": complexity_metrics,
            "labels": complexity_labels,
            "algorithms": identified_algorithms,
            "design_patterns": identified_patterns,
            "security_vulnerabilities": security_vulnerabilities,
            "performance": performance_estimate,
            "natural_language_description": nl_description,
            "language": "python",
            "generation_timestamp": datetime.now().isoformat(),
        }

        return sample

    def generate_value(self, var_type):
        """Generate a random value based on the variable type"""
        if var_type == "int":
            return random.randint(-100, 100)
        elif var_type == "float":
            return round(random.uniform(-100.0, 100.0), 2)
        elif var_type == "string":
            words = [
                "hello",
                "world",
                "python",
                "code",
                "data",
                "model",
                "train",
                "test",
            ]
            return f'"{random.choice(words)}"'
        elif var_type == "bool":
            return random.choice(["True", "False"])
        elif var_type == "list":
            size = random.randint(1, 5)
            elements = [str(random.randint(1, 10)) for _ in range(size)]
            return f"[{', '.join(elements)}]"
        elif var_type == "dict":
            size = random.randint(1, 3)
            keys = [f'"{self.generate_variable_name("key")}"' for _ in range(size)]
            values = [str(random.randint(1, 10)) for _ in range(size)]
            items = [f"{k}: {v}" for k, v in zip(keys, values)]
            return f"{{{', '.join(items)}}}"

    def generate_expression(self, depth=0, max_depth=3, variables=None):
        """Generate a random expression with controlled complexity"""
        if variables is None:
            variables = []

        # Base case: return a variable or literal
        if depth >= max_depth or random.random() < 0.3:
            if variables and random.random() < 0.7:
                return random.choice(variables)
            else:
                var_type = random.choice(["int", "float", "bool"])
                return str(self.generate_value(var_type))

        # Recursive case: create a binary operation
        operator = random.choice(self.operators)
        left = self.generate_expression(depth + 1, max_depth, variables)
        right = self.generate_expression(depth + 1, max_depth, variables)

        # Add parentheses for clarity
        return f"({left} {operator} {right})"

    def generate_statement(self, indent=0, variables=None, nesting_level=0):
        """Generate a random Python statement"""
        if variables is None:
            variables = []
            
        # Python has a limit of 20 statically nested blocks
        # Avoid deep nesting to prevent "too many statically nested blocks" error
        if nesting_level >= 18:  # Leave some margin
            statement_types = ["assignment"]  # Only generate simple statements at deep nesting
        else:
            statement_types = ["assignment", "conditional", "loop"]
            
        statement_type = random.choice(statement_types)

        indentation = "    " * indent

        if statement_type == "assignment":
            var_name = self.generate_variable_name()
            var_type = random.choice(self.variable_types)

            # Simple assignment
            if random.random() < 0.7 or not variables:
                value = self.generate_value(var_type)
                variables.append(var_name)
                return f"{indentation}{var_name} = {value}", variables
            # Expression assignment
            else:
                expr = self.generate_expression(variables=variables)
                variables.append(var_name)
                return f"{indentation}{var_name} = {expr}", variables

        elif statement_type == "conditional" and variables:
            condition = self.generate_expression(variables=variables)
            result = f"{indentation}if {condition}:\n"
            inner_stmt, variables = self.generate_statement(indent + 1, variables, nesting_level + 1)
            result += inner_stmt

            if random.random() < 0.5:
                result += f"\n{indentation}else:\n"
                inner_stmt, variables = self.generate_statement(indent + 1, variables, nesting_level + 1)
                result += inner_stmt

            return result, variables

        elif statement_type == "loop" and variables:
            loop_var = self.generate_variable_name("i")
            loop_range = random.randint(2, 5)
            result = f"{indentation}for {loop_var} in range({loop_range}):\n"
            inner_stmt, variables = self.generate_statement(
                indent + 1, variables + [loop_var], nesting_level + 1
            )
            result += inner_stmt
            return result, variables

        else:
            # Default to assignment if we can't do other types
            var_name = self.generate_variable_name()
            var_type = random.choice(self.variable_types)
            value = self.generate_value(var_type)
            variables.append(var_name)
            return f"{indentation}{var_name} = {value}", variables

    def generate_function(self, complexity=1):
        """Generate a random Python function with controlled complexity"""
        # Generate function name and parameters
        func_name = f"function_{random.randint(1, 1000)}"
        num_params = random.randint(0, 3)
        # Ensure unique parameter names
        params = []
        for _ in range(num_params):
            param_name = self.generate_variable_name("param")
            while param_name in params:
                param_name = self.generate_variable_name("param")
            params.append(param_name)

        # Start function definition
        function_def = f"def {func_name}({', '.join(params)}):\n"

        # Add docstring
        function_def += '    """A randomly generated function"""\n'

        # Generate function body
        variables = params.copy()
        body = ""

        # Generate statements based on complexity
        num_statements = random.randint(1, 3 * complexity)

        for _ in range(num_statements):
            stmt, variables = self.generate_statement(indent=1, variables=variables, nesting_level=1)
            body += stmt + "\n"

        # Add return statement if we have variables
        if variables:
            return_var = random.choice(variables)
            body += f"    return {return_var}\n"
        else:
            body += "    return None\n"

        function_def += body
        return function_def

    def generate_class(self, complexity=1):
        """Generate a random Python class with methods"""
        class_name = f"Class{random.randint(1, 100)}"

        # Start class definition
        class_def = f"class {class_name}:\n"

        # Add docstring
        class_def += '    """A randomly generated class"""\n\n'

        # Add constructor
        class_def += "    def __init__(self):\n"
        num_attributes = random.randint(1, 3)

        for _ in range(num_attributes):
            attr_name = self.generate_variable_name("self")
            attr_type = random.choice(self.variable_types)
            attr_value = self.generate_value(attr_type)
            class_def += f"        self.{attr_name} = {attr_value}\n"

        class_def += "\n"

        # Add methods
        num_methods = random.randint(1, 2 * complexity)

        for _ in range(num_methods):
            method_name = f"method_{random.randint(1, 100)}"
            class_def += f"    def {method_name}(self"

            # Add parameters
            num_params = random.randint(0, 2)
            params = [self.generate_variable_name("param") for _ in range(num_params)]
            if params:
                class_def += ", " + ", ".join(params)

            class_def += "):\n"

            # Add method docstring
            class_def += '        """A randomly generated method"""\n'

            # Generate method body
            variables = ["self"] + params
            body = ""

            num_statements = random.randint(1, 2 * complexity)
            for _ in range(num_statements):
                stmt, variables = self.generate_statement(indent=2, variables=variables, nesting_level=2)
                body += stmt + "\n"

            # Add return statement
            if random.random() < 0.7 and variables:
                # Choose a variable that's not 'self'
                return_vars = [v for v in variables if v != "self"]
                if return_vars:
                    return_var = random.choice(return_vars)
                    body += f"        return {return_var}\n"
                else:
                    body += "        return None\n"
            else:
                body += "        return None\n"

            class_def += body + "\n"

        return class_def

    def generate_script(self, complexity=1):
        """Generate a complete Python script with imports, functions, and a main section"""
        script = "# Randomly generated Python script\n\n"

        # Add imports
        imports = [
            "import random",
            "import os",
            "import sys",
            "import math",
            "import json",
        ]
        selected_imports = random.sample(imports, random.randint(1, len(imports)))
        script += "\n".join(selected_imports) + "\n\n"

        # Add functions
        num_functions = random.randint(1, 2 * complexity)
        for _ in range(num_functions):
            script += self.generate_function(complexity) + "\n\n"

        # Add classes
        num_classes = random.randint(0, complexity)
        for _ in range(num_classes):
            script += self.generate_class(complexity) + "\n\n"

        # Add main section
        script += 'if __name__ == "__main__":\n'
        variables = []

        num_statements = random.randint(2, 3 * complexity)
        for _ in range(num_statements):
            stmt, variables = self.generate_statement(indent=1, variables=variables, nesting_level=1)
            script += stmt + "\n"

        # Add a function call if we generated any
        if num_functions > 0:
            func_call = f"    function_{random.randint(1, 1000)}("
            num_args = random.randint(0, 2)

            if num_args > 0 and variables:
                args = [
                    random.choice(variables)
                    for _ in range(min(num_args, len(variables)))
                ]
                func_call += ", ".join(args)

            func_call += ")\n"
            script += func_call

        return script

    def generate_algorithm_code(self, algorithm_type):
        """Generate code implementing a specific algorithm"""
        if algorithm_type == "linear_search":
            return """def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
"""
        elif algorithm_type == "binary_search":
            return """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
"""
        elif algorithm_type == "bubble_sort":
            return """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""
        elif algorithm_type == "factorial":
            return """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
        else:
            return self.generate_function(complexity=2)

    def generate_design_pattern_code(self, pattern_type):
        """Generate code implementing a specific design pattern"""
        if pattern_type == "singleton":
            return """class Singleton:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if self.__class__._instance is not None:
            raise Exception("This class is a singleton!")
        self.value = random.randint(1, 100)
"""
        elif pattern_type == "factory":
            return """class ShapeFactory:
    @staticmethod
    def create_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        elif shape_type == "triangle":
            return Triangle()
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
"""
        elif pattern_type == "observer":
            return """class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def add_observer(self, observer):
        self._observers.append(observer)
    
    def remove_observer(self, observer):
        self._observers.remove(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._state)
    
    def set_state(self, state):
        self._state = state
        self.notify_observers()
"""
        elif pattern_type == "decorator":
            return """class Component:
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        return "ConcreteComponent"

class Decorator(Component):
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()

class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"ConcreteDecoratorA({self._component.operation()})"
"""
        else:
            return self.generate_class(complexity=2)

    def generate_vulnerable_code(self, vulnerability_type):
        """Generate code with a specific vulnerability type"""
        if vulnerability_type == "sql_injection":
            return """def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return db.execute(query)
"""
        elif vulnerability_type == "command_injection":
            return """def ping_host(hostname):
    result = os.system("ping -c 1 " + hostname)
    return result == 0
"""
        elif vulnerability_type == "path_traversal":
            return """def read_file(filename):
    with open("data/" + filename, "r") as f:
        return f.read()
"""
        elif vulnerability_type == "hardcoded_credentials":
            return """def connect_to_database():
    username = "admin"
    password = "super_secret_password"
    return db.connect(username, password)
"""
        elif vulnerability_type == "insecure_random":
            return """def generate_token():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(16))
"""
        else:
            return self.generate_function(complexity=1)

    def generate_ast(self, code):
        """Generate AST for given code"""
        try:
            return ast.parse(code)
        except SyntaxError as e:
            logging.error(f"Syntax error in generated code: {e}")
            return None

    def ast_to_dict(self, node):
        """Convert AST to a dictionary representation"""
        if isinstance(node, ast.AST):
            fields = {}
            for name, value in ast.iter_fields(node):
                fields[name] = self.ast_to_dict(value)
            return {"node_type": type(node).__name__, "fields": fields}
        elif isinstance(node, list):
            return [self.ast_to_dict(item) for item in node]
        else:
            return node

    def generate_cfg(self, code):
        """Generate a simplified Control Flow Graph from code"""
        try:
            tree = ast.parse(code)
            graph = nx.DiGraph()

            # Simple implementation just to demonstrate the concept
            # In a real system, this would be much more sophisticated
            node_id = 0

            def visit_node(node, parent_id=None):
                nonlocal node_id
                current_id = node_id
                node_id += 1

                # Add node
                node_label = f"{type(node).__name__}"
                if isinstance(node, ast.FunctionDef):
                    node_label += f": {node.name}"
                elif isinstance(node, ast.ClassDef):
                    node_label += f": {node.name}"

                graph.add_node(current_id, label=node_label)

                # Add edge from parent if exists
                if parent_id is not None:
                    graph.add_edge(parent_id, current_id)

                # Visit children
                for child in ast.iter_child_nodes(node):
                    visit_node(child, current_id)

                return current_id

            visit_node(tree)
            return graph
        except Exception as e:
            logging.error(f"Error generating CFG: {e}")
            return nx.DiGraph()

    def generate_dfg(self, code):
        """Generate a simplified Data Flow Graph from code"""
        try:
            tree = ast.parse(code)
            graph = nx.DiGraph()

            variables = {}
            node_id = 0

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
                            self._process_expression(
                                node.value, def_id, graph, variables
                            )

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

    def generate_pdg(self, code):
        """Generate a Program Dependence Graph (PDG) combining control and data dependencies"""
        try:
            # PDG combines control and data flow graphs
            cfg = self.generate_cfg(code)
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

    def generate_dependency_graph(self, code):
        """Generate a dependency graph showing module/import dependencies"""
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

    def generate_version_history(self, code, num_versions=3):
        """Simulate version control history for the generated code"""
        history = []
        current_code = code

        # Initial commit
        history.append(
            {
                "version": 1,
                "timestamp": "2023-01-01T00:00:00Z",
                "author": "developer1@example.com",
                "message": "Initial commit",
                "code": current_code,
                "changes": {
                    "additions": len(current_code.splitlines()),
                    "deletions": 0,
                    "files_changed": 1,
                },
            }
        )

        # Generate additional versions with modifications
        for i in range(2, num_versions + 1):
            # Choose a modification type
            mod_type = random.choice(["feature", "bugfix", "refactor"])

            if mod_type == "feature":
                # Add a new function
                new_func = self.generate_function(complexity=random.randint(1, 2))
                lines = current_code.splitlines()
                insert_pos = random.randint(0, len(lines) - 1)
                lines.insert(insert_pos, "\n" + new_func)
                new_code = "\n".join(lines)
                message = f"Add new functionality: {new_func.splitlines()[0]}"
                additions = len(new_func.splitlines())
                deletions = 0

            elif mod_type == "bugfix":
                # Fix a bug by modifying a line
                lines = current_code.splitlines()
                mod_line = random.randint(0, len(lines) - 1)
                old_line = lines[mod_line]

                # Ensure it's a line with code not just whitespace or comments
                attempts = 0
                while (
                    not old_line.strip() or old_line.strip().startswith("#")
                ) and attempts < 10:
                    mod_line = random.randint(0, len(lines) - 1)
                    old_line = lines[mod_line]
                    attempts += 1

                # Simple modification: change an operator or value
                if "=" in old_line:
                    parts = old_line.split("=")
                    parts[-1] = " " + str(random.randint(1, 100))
                    new_line = "=".join(parts)
                elif "+" in old_line:
                    new_line = old_line.replace("+", "-")
                else:
                    new_line = old_line + " # Modified in bugfix"

                lines[mod_line] = new_line
                new_code = "\n".join(lines)
                message = f"Fix bug in line {mod_line + 1}"
                additions = 1
                deletions = 1

            else:  # refactor
                # Rename a variable
                lines = current_code.splitlines()
                variables = set()

                # Find variables
                for line in lines:
                    if "=" in line and not line.strip().startswith("#"):
                        parts = line.split("=")
                        if len(parts) > 1:
                            var_name = parts[0].strip()
                            if var_name and var_name.isidentifier():
                                variables.add(var_name)

                if variables:
                    var_to_rename = random.choice(list(variables))
                    new_var_name = var_to_rename + "_renamed"

                    new_lines = []
                    for line in lines:
                        if var_to_rename in line:
                            # Ensure it's actually the variable, not part of another word
                            new_line = []
                            for part in line.split(" "):
                                if part == var_to_rename:
                                    new_line.append(new_var_name)
                                elif part.startswith(var_to_rename + "."):
                                    new_line.append(
                                        new_var_name + part[len(var_to_rename) :]
                                    )
                                else:
                                    new_line.append(part)
                            new_lines.append(" ".join(new_line))
                        else:
                            new_lines.append(line)

                    new_code = "\n".join(new_lines)
                    message = (
                        f"Refactor: rename variable {var_to_rename} to {new_var_name}"
                    )
                    # Count the occurrences
                    additions = sum(1 for line in new_lines if new_var_name in line)
                    deletions = sum(1 for line in lines if var_to_rename in line)
                else:
                    # If no variables to rename, add a comment
                    new_code = current_code + "\n# Code refactored for clarity"
                    message = "Minor refactoring"
                    additions = 1
                    deletions = 0

            # Add to history
            history.append(
                {
                    "version": i,
                    "timestamp": f"2023-{i:02d}-01T00:00:00Z",
                    "author": f"developer{random.randint(1, 3)}@example.com",
                    "message": message,
                    "code": new_code,
                    "changes": {
                        "additions": additions,
                        "deletions": deletions,
                        "files_changed": 1,
                    },
                }
            )

            current_code = new_code

        return history

    def generate_bytecode(self, code):
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

    def generate_execution_trace(self, code):
        """Generate execution trace for the code"""
        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                tmp_filename = tmp.name

                # Add tracing code to the original code
                trace_code = """


import sys
import traceback

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

                # Add a code block to print the trace at the end
                trace_epilogue = """

# Print execution trace at the end
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
        import json
        print(json.dumps(_execution_trace))
"""

                # Strip the original __main__ block if it exists
                main_code = "\n"
                code_lines = code.splitlines()
                in_main_block = False
                main_indentation = ""

                for line in code_lines:
                    if line.strip().startswith('if __name__ == "__main__":'):
                        in_main_block = True
                        main_indentation = line[: line.find("if")]
                        main_code += line + "\n"
                    elif in_main_block:
                        if line.strip() and not line.startswith(main_indentation + " "):
                            in_main_block = False
                            main_code += line + "\n"
                        else:
                            main_code += line + "\n"
                    else:
                        main_code += line + "\n"

                # Write the complete instrumented code
                tmp.write((trace_code + main_code + trace_epilogue).encode("utf-8"))

            # Run the instrumented code and capture the output
            import subprocess

            result = subprocess.run(
                [sys.executable, tmp_filename], capture_output=True, text=True
            )

            # Clean up the temporary file
            os.unlink(tmp_filename)

            # Try to parse the execution trace from the output
            trace = []
            if result.stdout:
                try:
                    trace = json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    logging.error(
                        f"Failed to parse execution trace JSON: {result.stdout}"
                    )

            return {
                "trace": trace,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        except Exception as e:
            logging.error(f"Error generating execution trace: {e}")
            return {
                "error": str(e),
                "trace": [],
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
            }

    def analyze_code_complexity(self, code):
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
            ast_tree = self.generate_ast(code)
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

                # Advanced metrics if available
                if RADON_AVAILABLE:
                    try:
                        mi = radon.metrics.mi_visit(code, multi=True)
                        metrics["maintainability_index"] = mi

                        cc = radon.complexity.cc_visit(code)
                        metrics["radon_complexity"] = {c.name: c.complexity for c in cc}
                    except Exception as e:
                        logging.warning(f"Error calculating radon metrics: {e}")

                # Pylint score if available
                if PYLINT_AVAILABLE:
                    try:
                        with tempfile.NamedTemporaryFile(
                            suffix=".py", delete=False
                        ) as tmp:
                            tmp_filename = tmp.name
                            tmp.write(code.encode("utf-8"))

                        from io import StringIO

                        pylint_output = StringIO()
                        reporter = TextReporter(pylint_output)
                        pylint.lint.Run([tmp_filename], reporter=reporter, exit=False)

                        # Extract score from output
                        output_str = pylint_output.getvalue()
                        score_match = re.search(
                            r"Your code has been rated at ([-\d.]+)/10", output_str
                        )
                        if score_match:
                            metrics["pylint_score"] = float(score_match.group(1))

                        os.unlink(tmp_filename)
                    except Exception as e:
                        logging.warning(f"Error calculating pylint score: {e}")
        except Exception as e:
            logging.error(f"Error analyzing code complexity: {e}")

        return metrics

    def analyze_complexity_labels(self, metrics):
        """Generate labels for complexity based on metrics"""
        labels = {}

        # Cyclomatic complexity labels
        cc = metrics.get("cyclomatic_complexity", 0)
        if cc <= 5:
            labels["complexity_level"] = "simple"
        elif cc <= 10:
            labels["complexity_level"] = "moderate"
        elif cc <= 20:
            labels["complexity_level"] = "complex"
        else:
            labels["complexity_level"] = "very_complex"

        # Maintainability labels
        mi = metrics.get("maintainability_index", 0)
        if mi >= 80:
            labels["maintainability"] = "high"
        elif mi >= 60:
            labels["maintainability"] = "moderate"
        elif mi >= 40:
            labels["maintainability"] = "low"
        else:
            labels["maintainability"] = "very_low"

        # Function size labels
        avg_func_len = metrics.get("avg_function_length", 0)
        if avg_func_len <= 10:
            labels["function_size"] = "small"
        elif avg_func_len <= 20:
            labels["function_size"] = "medium"
        elif avg_func_len <= 50:
            labels["function_size"] = "large"
        else:
            labels["function_size"] = "very_large"

        return labels

    def identify_algorithms(self, code):
        """Identify algorithms in the code"""
        algorithms = []

        for algo_name, algo_info in self.algorithm_templates.items():
            if re.search(algo_info["pattern"], code, re.MULTILINE):
                algorithms.append(
                    {"name": algo_name, "complexity": algo_info["complexity"]}
                )

        return algorithms

    def identify_design_patterns(self, code):
        """Identify design patterns in the code"""
        patterns = []

        for pattern_name, pattern_info in self.design_pattern_templates.items():
            if re.search(pattern_info["pattern"], code, re.MULTILINE):
                patterns.append({"name": pattern_name})

        return patterns

    def identify_security_vulnerabilities(self, code):
        """Identify potential security vulnerabilities in the code"""
        vulnerabilities = []

        for vuln_name, vuln_info in self.security_vulnerabilities.items():
            if re.search(vuln_info["pattern"], code, re.MULTILINE):
                vulnerabilities.append(
                    {"type": vuln_name, "severity": vuln_info["severity"]}
                )

        return vulnerabilities

    def estimate_performance(self, code):
        """Estimate performance characteristics of the code"""
        performance = {"estimation_method": "static_analysis"}

        # Try to identify time complexity from loops and recursion
        tree = self.generate_ast(code)
        if tree:
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
            loop_visitor.visit(tree)
            max_loop_depth = loop_visitor.max_depth

            # Check for recursion
            has_recursion = False
            function_names = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.add(node.name)

            for node in ast.walk(tree):
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
            for node in ast.walk(tree):
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

    def generate_natural_language_description(
        self, code, metrics, algorithms, patterns, vulnerabilities
    ):
        """Generate a natural language description of the code"""
        lines = code.splitlines()

        # Extract basic structural information
        imports = [
            line
            for line in lines
            if line.strip().startswith("import ") or line.strip().startswith("from ")
        ]
        functions = [line for line in lines if line.strip().startswith("def ")]
        classes = [line for line in lines if line.strip().startswith("class ")]

        # Build description
        description = "This Python code "

        if imports:
            description += f"imports {len(imports)} module(s) including " + ", ".join(
                [imp.split()[1].split(".")[0] for imp in imports[:3]]
            )
            if len(imports) > 3:
                description += f" and {len(imports) - 3} more"
            description += ". "

        if classes:
            description += f"It defines {len(classes)} class(es)"
            if classes:
                description += " named " + ", ".join(
                    [cls.split()[1].split("(")[0] for cls in classes[:3]]
                )
                if len(classes) > 3:
                    description += f" and {len(classes) - 3} more"
            description += ". "

        if functions:
            description += f"It contains {len(functions)} function(s)"
            if functions:
                description += " including " + ", ".join(
                    [func.split()[1].split("(")[0] for func in functions[:3]]
                )
                if len(functions) > 3:
                    description += f" and {len(functions) - 3} more"
            description += ". "

        # Add complexity information
        if "complexity_level" in metrics:
            description += f"The code has {metrics['complexity_level']} complexity. "

        # Add algorithm information
        if algorithms:
            description += (
                "It appears to implement "
                + ", ".join([algo["name"].replace("_", " ") for algo in algorithms])
                + ". "
            )

        # Add design pattern information
        if patterns:
            description += (
                "The code uses the "
                + ", ".join([pattern["name"] for pattern in patterns])
                + " design pattern(s). "
            )

        # Add performance information
        if "time_complexity" in metrics:
            description += f"The estimated time complexity is {metrics.get('time_complexity', 'unknown')}. "

        # Add security information
        if vulnerabilities:
            description += (
                f"Warning: The code contains {len(vulnerabilities)} potential security issue(s) including "
                + ", ".join(
                    [vuln["type"].replace("_", " ") for vuln in vulnerabilities]
                )
                + ". "
            )

        return description.strip()

    def compute_metrics(self, code, ast_tree):
        """Compute code metrics"""
        metrics = {}

        # Simple metrics
        metrics["loc"] = len(code.splitlines())

        # Count functions
        functions = [
            node for node in ast.walk(ast_tree) if isinstance(node, ast.FunctionDef)
        ]
        metrics["function_count"] = len(functions)

        # Average function complexity (lines per function)
        if metrics["function_count"] > 0:
            function_lines = []
            for func in functions:
                start_line = func.lineno
                end_line = (
                    func.end_lineno if hasattr(func, "end_lineno") else start_line
                )
                for node in ast.walk(func):
                    if hasattr(node, "end_lineno"):
                        end_line = max(end_line, node.end_lineno)
                function_lines.append(end_line - start_line + 1)

            metrics["avg_function_length"] = sum(function_lines) / len(function_lines)
        else:
            metrics["avg_function_length"] = 0

        # Count classes
        metrics["class_count"] = len(
            [node for node in ast.walk(ast_tree) if isinstance(node, ast.ClassDef)]
        )

        # Complexity metrics - simplified versions
        metrics["cyclomatic_complexity"] = (
            len(
                [
                    node
                    for node in ast.walk(ast_tree)
                    if isinstance(node, (ast.If, ast.For, ast.While))
                ]
            )
            + 1
        )

        return metrics

    def generate_buggy_version(self, code):
        """Introduce a random bug into the code"""
        lines = code.splitlines()
        if not lines:
            return code

        bug_type = random.choice(["syntax", "variable", "logic"])

        if bug_type == "syntax":
            # Remove a character from a random line
            line_idx = random.randint(0, len(lines) - 1)
            line = lines[line_idx]

            if line.strip() and not line.strip().startswith("#"):
                char_idx = random.randint(0, len(line) - 1)
                lines[line_idx] = line[:char_idx] + line[char_idx + 1 :]

        elif bug_type == "variable":
            # Change a variable name
            var_pattern = r"[a-zA-Z_][a-zA-Z0-9_]*"
            variables = set()

            for line in lines:
                if "=" in line and not line.strip().startswith("#"):
                    parts = line.split("=")
                    if len(parts) > 1:
                        var_name = parts[0].strip()
                        if var_name and var_name.isidentifier():
                            variables.add(var_name)

            if variables:
                var_to_change = random.choice(list(variables))
                new_var = var_to_change + "_x"

                # Replace one occurrence
                for i, line in enumerate(lines):
                    if var_to_change in line and random.random() < 0.3:
                        # Make sure it's actually a variable and not part of another word
                        parts = []
                        in_var = False
                        for part in line.replace(
                            var_to_change, f"<SPLIT>{var_to_change}<SPLIT>"
                        ).split("<SPLIT>"):
                            if part == var_to_change and not in_var:
                                parts.append(new_var)
                                in_var = True
                            elif part.startswith(var_to_change + "."):
                                parts.append(
                                    new_var + part[len(var_to_change) :]
                                )
                            else:
                                parts.append(part)

                        lines[i] = "".join(parts)
                        break

        elif bug_type == "logic":
            # Flip a comparison operator
            operators = {
                "==": "!=",
                "!=": "==",
                "<": ">=",
                ">": "<=",
                "<=": ">",
                ">=": "<",
            }

            for i, line in enumerate(lines):
                for op in operators:
                    if op in line and "if " in line and random.random() < 0.5:
                        lines[i] = line.replace(op, operators[op], 1)
                        return "\n".join(lines)

        return "\n".join(lines)

    def serialize_graph(self, graph):
        """Serialize a NetworkX graph to a JSON-compatible format"""
        return {
            "nodes": [
                {"id": n, "label": graph.nodes[n].get("label", str(n))}
                for n in graph.nodes
            ],
            "edges": [{"source": u, "target": v} for u, v in graph.edges],
        }


class EnhancedDatasetGenerator:
    """Generate an enhanced dataset of code samples with extensive metrics and labels"""

    def __init__(self, output_dir="./enhanced_code_dataset", seed=42):
        self.output_dir = output_dir
        self.generator = CodeGenerator(seed=seed)
        os.makedirs(output_dir, exist_ok=True)

    def generate_dataset(
        self,
        num_samples=100,
        complexity_range=(1, 3),
        include_bugs=True,
        add_special_samples=True,
    ):
        """Generate a dataset with specified number of samples"""
        samples = []
        logging.info(f"Generating {num_samples} enhanced code samples...")

        with tqdm(total=num_samples) as pbar:
            valid_samples = 0
            attempts = 0

            while valid_samples < num_samples and attempts < num_samples * 2:
                attempts += 1
                complexity = random.randint(complexity_range[0], complexity_range[1])

                sample = self.generator.generate_sample(
                    complexity,
                    include_bugs=include_bugs,
                    add_special_samples=add_special_samples,
                )

                if sample is not None:
                    samples.append(sample)
                    valid_samples += 1
                    pbar.update(1)

        logging.info(
            f"Successfully generated {len(samples)} samples out of {attempts} attempts"
        )
        return samples

    def save_dataset(self, samples, output_file="enhanced_code_dataset.jsonl.gz"):
        """Save the dataset to a compressed JSONL file"""
        output_path = os.path.join(self.output_dir, output_file)

        logging.info(f"Saving dataset to {output_path}")
        with gzip.open(output_path, "wt", encoding="utf-8") as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")

        # Also save a small sample as uncompressed for easy inspection
        sample_path = os.path.join(self.output_dir, "sample.json")
        with open(sample_path, "w", encoding="utf-8") as f:
            json.dump(samples[:5], f, indent=2)

        # Generate dataset statistics
        self.generate_dataset_stats(
            samples, os.path.join(self.output_dir, "dataset_stats.json")
        )

        return output_path

    def generate_dataset_stats(self, samples, output_file):
        """Generate statistics about the dataset"""
        stats = {
            "total_samples": len(samples),
            "avg_loc": sum(s["metrics"].get("loc", 0) for s in samples)
            / max(1, len(samples)),
            "complexity_distribution": {},
            "algorithm_distribution": {},
            "vulnerability_count": sum(
                len(s.get("security_vulnerabilities", [])) for s in samples
            ),
            "pattern_distribution": {},
            "performance_distribution": {},
        }

        # Collect distributions
        for sample in samples:
            # Complexity
            complexity_level = sample.get("labels", {}).get(
                "complexity_level", "unknown"
            )
            stats["complexity_distribution"][complexity_level] = (
                stats["complexity_distribution"].get(complexity_level, 0) + 1
            )

            # Algorithms
            for algo in sample.get("algorithms", []):
                algo_name = algo.get("name", "unknown")
                stats["algorithm_distribution"][algo_name] = (
                    stats["algorithm_distribution"].get(algo_name, 0) + 1
                )

            # Design patterns
            for pattern in sample.get("design_patterns", []):
                pattern_name = pattern.get("name", "unknown")
                stats["pattern_distribution"][pattern_name] = (
                    stats["pattern_distribution"].get(pattern_name, 0) + 1
                )

            # Performance
            time_complexity = sample.get("performance", {}).get(
                "time_complexity", "unknown"
            )
            stats["performance_distribution"][time_complexity] = (
                stats["performance_distribution"].get(time_complexity, 0) + 1
            )

        # Save stats
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)

    def generate_and_save(
        self,
        num_samples=100,
        complexity_range=(1, 3),
        include_bugs=True,
        add_special_samples=True,
        output_file="enhanced_code_dataset.jsonl.gz",
    ):
        """Generate and save a dataset in one operation"""
        samples = self.generate_dataset(
            num_samples, complexity_range, include_bugs, add_special_samples
        )
        return self.save_dataset(samples, output_file)

    def generate_until_size(
        self,
        target_size_mb=1,
        max_samples=5000,
        complexity_range=(1, 3),
        include_bugs=True,
        add_special_samples=True,
        output_file="enhanced_code_dataset.jsonl.gz",
    ):
        """Generate samples until reaching approximately target_size_mb"""
        samples = []
        current_size = 0
        target_bytes = target_size_mb * 1024 * 1024  # Convert MB to bytes

        logging.info(
            f"Generating enhanced dataset of approximately {target_size_mb} MB..."
        )

        with tqdm(total=100) as pbar:  # Progress as percentage
            while current_size < target_bytes and len(samples) < max_samples:
                complexity = random.randint(complexity_range[0], complexity_range[1])
                sample = self.generator.generate_sample(
                    complexity,
                    include_bugs=include_bugs,
                    add_special_samples=add_special_samples,
                )

                if sample is not None:
                    # Estimate size by converting to JSON
                    sample_json = json.dumps(sample)
                    sample_size = len(sample_json.encode("utf-8"))

                    samples.append(sample)
                    current_size += sample_size

                    # Update progress bar
                    progress = min(100, int(current_size / target_bytes * 100))
                    pbar.update(progress - pbar.n)

        # Check final size
        final_size_mb = current_size / (1024 * 1024)
        logging.info(
            f"Generated {len(samples)} samples with total size approximately {final_size_mb:.2f} MB"
        )

        return self.save_dataset(samples, output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Generate enhanced code dataset for AI training"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./enhanced_code_dataset",
        help="Output directory",
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=100,
        help="Number of code samples to generate",
    )
    parser.add_argument(
        "--min-complexity", type=int, default=1, help="Minimum complexity level"
    )
    parser.add_argument(
        "--max-complexity", type=int, default=3, help="Maximum complexity level"
    )
    parser.add_argument(
        "--include-bugs", action="store_true", help="Include buggy versions of code"
    )
    parser.add_argument(
        "--target-size", type=float, default=1.0, help="Target dataset size in MB"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["count", "size"],
        default="size",
        help="Generation mode: fixed count or fixed size",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--no-special-samples",
        action="store_true",
        help="Don't include special algorithm/pattern samples",
    )

    args = parser.parse_args()

    generator = EnhancedDatasetGenerator(output_dir=args.output_dir, seed=args.seed)

    if args.mode == "count":
        output_path = generator.generate_and_save(
            num_samples=args.num_samples,
            complexity_range=(args.min_complexity, args.max_complexity),
            include_bugs=args.include_bugs,
            add_special_samples=not args.no_special_samples,
        )
    else:  # size mode
        output_path = generator.generate_until_size(
            target_size_mb=args.target_size,
            complexity_range=(args.min_complexity, args.max_complexity),
            include_bugs=args.include_bugs,
            add_special_samples=not args.no_special_samples,
        )

    logging.info(f"Enhanced dataset generation complete. Output saved to {output_path}")
    logging.info(f"Dataset can be used for training AI models on code analysis tasks")


if __name__ == "__main__":
    main()
