import sys
import os


class VirtualEnvChecker:
    def __init__(self):
        self.venv_indicators = {
            "linux": {"bin", "include", "lib", "pyvenv.cfg"},
            "win32": {"Scripts", "Include", "Lib", "pyvenv.cfg"}
        }

    def is_likely_venv(self, path):
        platform = sys.platform
        indicators = self.venv_indicators.get(platform, set())
        return all(os.path.exists(os.path.join(path, ind)) for ind in indicators)

