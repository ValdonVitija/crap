import ast
import pathlib
from crap.module_checker import ImportsVisitor

class PythonFileAnalyzer:
    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path
        self.imported_modules = set()

    def analyze(self):
        """
        Analyzes the Python file and extracts the imported modules.
        """
        code = self.file_path.read_text()
        tree = ast.parse(code)
        visitor = ImportsVisitor()
        visitor.visit(tree)
        self.imported_modules = visitor.imported_modules