import unittest
from pathlib import Path
from unittest.mock import patch
from crap.crap_manager import CrapManager

class TestCrapManager(unittest.TestCase):
    def setUp(self):
        self.crap_manager = CrapManager(".")

    @patch('crap.crap_manager.CrapManager._analyze_file')
    def test_process_path_file(self, mock_analyze_file):
        self.crap_manager.path_ = Path(__file__)
        self.crap_manager._process_path()
        mock_analyze_file.assert_called_once_with(Path(__file__))

    @patch('crap.crap_manager.CrapManager._analyze_directory')
    def test_process_path_directory(self, mock_analyze_directory):
        self.crap_manager.path_ = Path('.')
        self.crap_manager._process_path()
        mock_analyze_directory.assert_called_once()

    @patch('crap.crap_manager.get_installed_packages', return_value=['os', 'pathlib'])
    @patch('crap.crap_manager.PythonFileAnalyzer')
    def test_analyze_file(self, mock_analyzer, mock_get_installed_packages):
        mock_analyzer_instance = mock_analyzer.return_value
        mock_analyzer_instance.imported_modules = ['os']
        self.crap_manager.package_usage_counter.pack_counter.clear()
        self.crap_manager.package_usage_counter.pack_counter = {'os': 0}
        self.crap_manager._analyze_file(Path(__file__))
        self.assertEqual(self.crap_manager.package_usage_counter.pack_counter, {'os': 1})

    @patch('crap.crap_manager.CrapManager._analyze_file')
    def test_analyze_directory(self, mock_analyze_file):
        self.crap_manager.path_ = Path('.')
        self.crap_manager._analyze_directory()
        self.assertGreater(mock_analyze_file.call_count, 0)

    @patch('crap.crap_manager.CrapManager._get_important_packages', return_value=['os'])
    @patch('crap.crap_manager.PackageUsageCounter.get_unused_packages', return_value=['pathlib'])
    @patch('crap.crap_manager.uninstall_package')
    def test_cleanup_packages(self, mock_uninstall_package, mock_get_unused_packages, mock_get_important_packages):
        self.crap_manager.package_usage_counter.pack_counter = {'os': 1, 'pathlib': 0}
        self.crap_manager._cleanup_packages()
        mock_uninstall_package.assert_called_once_with('pathlib')

if __name__ == "__main__":
    unittest.main()