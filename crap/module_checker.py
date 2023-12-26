import ast
import json
from functools import lru_cache
import subprocess
from typing import Set, Any, Tuple


class ImportsVisitor(ast.NodeVisitor):
    """
    AST visitor to check if a specific module or names are imported in the code.
    """

    __slots__: Tuple[str] = ("module_name", "imported", "names")

    def __init__(self) -> None:
        """
        Args:
            module_name (str): The name of the module to check for.
            imported (bool): Whether the module is imported or not.
            names (Set[str]): Names to check for in case of 'from import' (default is None).
        """
        self.imported_modules = set()

    def visit_Import(self, node: ast.Import) -> Any:
        """
        Visit an Import node.

        Check if the specified module is imported.

        Args:
            node (ast.Import): The Import node to visit.
        """
        for name in node.names:
            self.imported_modules.add(name.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """
        Visit an ImportFrom node.

        Check if the specified module is imported using 'from import'.

        Args:
            node (ast.ImportFrom): The ImportFrom node to visit.
        """
        self.imported_modules.add(node.module)





# code_ = """
# import numpy
# import pandas
# import x
# from array import asdsasdasas
# """
# tree = ast.parse(code_)
# visitor = ImportsVisitor()
# visitor.visit(tree)
# print(visitor.imported_modules)




code = """
import math
module_name = "math"
math_module = __import__(module_name, fromlist=[""])

"""

class VariableValueVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variable_values = {}

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                value = self._evaluate(node.value)
                self.variable_values[variable_name] = value

    def _evaluate(self, node):
        if isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            return self.variable_values.get(node.id)
        elif isinstance(node, ast.BinOp):
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return left + right

# # Parse the code into an Abstract Syntax Tree (AST)
# parsed_code = ast.parse(code)

# # Create a visitor instance and visit the AST
# visitor = VariableValueVisitor()
# visitor.visit(parsed_code)

# # Now you can access the values from the visitor's dictionary
# print(f"The value of variable module_name is: {visitor.variable_values.get('module_name')}")
