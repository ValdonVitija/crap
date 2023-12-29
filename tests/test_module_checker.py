import unittest
import ast
from crap.module_checker import ImportsVisitor

class TestImportsVisitor(unittest.TestCase):
    def setUp(self):
        self.visitor = ImportsVisitor()

    def test_visit_Import(self):
        node = ast.parse('import os')
        self.visitor.visit_Import(node.body[0])
        self.assertIn('os', self.visitor.imported_modules)

    def test_visit_ImportFrom(self):
        node = ast.parse('from os import path')
        self.visitor.visit_ImportFrom(node.body[0])
        self.assertIn('os', self.visitor.imported_modules)

if __name__ == "__main__":
    unittest.main()