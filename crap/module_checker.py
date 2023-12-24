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


@lru_cache
def get_current_packages_as_json():
    """ """
    process = subprocess.run(["pipdeptree", "--json"], capture_output=True, text=True)
    json_output = json.loads(process.stdout)
    return json_output


@lru_cache
def get_installed_packages_as_list():
    """ """
    process = subprocess.run(["pipdeptree", "--json"], capture_output=True, text=True)
    json_output = json.loads(process.stdout)
    return [pack["package"]["package_name"] for pack in json_output]

@lru_cache
def get_package_counter_dict():
    """ """
    process = subprocess.run(["pipdeptree", "--json"], capture_output=True, text=True)
    json_output = json.loads(process.stdout)
    new_json = {}

    for item in json_output:
        package_name = item['package']['package_name']
        new_json[package_name] = 0

    return new_json



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
