import unittest
import tempfile
import os
from crap.virtual_env_checker import VirtualEnvChecker

class TestVirtualEnvChecker(unittest.TestCase):
    def setUp(self):
        self.venv_checker = VirtualEnvChecker()

    def test_is_likely_venv_with_venv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.makedirs(os.path.join(temp_dir, 'bin'))
            os.makedirs(os.path.join(temp_dir, 'include'))
            os.makedirs(os.path.join(temp_dir, 'lib'))
            open(os.path.join(temp_dir, 'pyvenv.cfg'), 'a').close()
            self.assertTrue(self.venv_checker.is_likely_venv(temp_dir))

    def test_is_likely_venv_without_venv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertFalse(self.venv_checker.is_likely_venv(temp_dir))

if __name__ == "__main__":
    unittest.main()