import ast
from typing import Any, Tuple


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

