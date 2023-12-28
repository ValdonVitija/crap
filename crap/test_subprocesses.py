import unittest
from crap.subprocesses import run_subprocess
import subprocess

class SubprocessesTests(unittest.TestCase):
    def test_run_subprocess(self):
        # Define the command to run
        command = ["ls", "-l"]

        # Run the subprocess
        result = run_subprocess(command)

        # Verify the subprocess completed successfully
        self.assertIsInstance(result, subprocess.CompletedProcess)
        self.assertEqual(result.returncode, 0)
        self.assertIsInstance(result.stdout, str)
        self.assertIsInstance(result.stderr, str)

if __name__ == "__main__":
    unittest.main()