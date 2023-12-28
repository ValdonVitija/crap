import unittest
from pathlib import Path
from crap.file_analyzer import PythonFileAnalyzer

class PythonFileAnalyzerTests(unittest.TestCase):
    def test_analyze(self):
        test_file = Path("test_file.py")
        test_file.write_text("import os\nimport sys\nimport math")

        analyzer = PythonFileAnalyzer(test_file)

        analyzer.analyze()

        self.assertEqual(analyzer.imported_modules, {"os", "sys", "math"})

        test_file.unlink()

if __name__ == "__main__":
    unittest.main()