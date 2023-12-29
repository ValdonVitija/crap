import unittest
from crap.subprocesses import run_subprocess, execute_command_without_output, get_installed_packages

class SubprocessesTests(unittest.TestCase):
    def test_run_subprocess(self):
        command = ["echo", "Hello, World!"]
        result = run_subprocess(command)
        self.assertEqual(result.stdout.strip(), "Hello, World!")

    def test_execute_command_without_output(self):
        command = ["echo", "Hello, World!"]
        result = execute_command_without_output(command)
        self.assertIsNone(result)

    def test_get_installed_packages(self):
        packages = get_installed_packages()
        self.assertIsInstance(packages, list)

if __name__ == "__main__":
    unittest.main()