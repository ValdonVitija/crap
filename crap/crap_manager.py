import ast
import subprocess
import sys
import os
import shutil
from typing import List, Tuple, Set
import pathlib

from module_checker import (
    get_installed_packages_as_list,
    ImportsVisitor,
    get_package_counter_dict,
)


class CrapManager:
    """ """

    __slots__ = ("path_", "pack_counter")

    def __init__(self, path_: str) -> None:
        self.path_ = pathlib.Path(path_).absolute()
        self.pack_counter = get_package_counter_dict()

    def run(self):
        if not self.path_.exists():
            raise FileNotFoundError("File/Dir not found")

        if self.path_.is_file():
            self._check_file(self.path_)
        elif self.path_.is_dir():
            self._check_directory()

    def _check_file(self, file_path: pathlib.Path) -> None:
        print(file_path)
        code = file_path.read_text()
        tree_ = ast.parse(code)
        visitor = ImportsVisitor()
        visitor.visit(tree_)
        for package_ in get_installed_packages_as_list():
            if package_ in visitor.imported_modules:
                self.pack_counter[package_] += 1

    def is_likely_venv(self, path):
        """
        Check if the given path is likely a virtual environment.
        """
        if sys.platform == "linux":
            venv_indicators = {"bin", "include", "lib", "pyvenv.cfg"}
        elif sys.platform == "win32":
            venv_indicators = {"Scripts", "Include", "Lib", "pyvenv.cfg"}

        if all(
            os.path.exists(os.path.join(path, indicator))
            for indicator in venv_indicators
        ):
            return True

        return False

    def _check_directory(self):
        excluded_dirs = {"__pycache__", ".git"}

        for dirpath, dirnames, filenames in os.walk(self.path_):
            dirnames[:] = [
                d
                for d in dirnames
                if not self.is_likely_venv(os.path.join(dirpath, d))
                and d not in excluded_dirs
            ]
            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = pathlib.Path(dirpath) / filename
                    self._check_file(file_path)

    def get_unused_packages(self) -> List[str]:
        unused_packages = []
        for package_, count in self.pack_counter.items():
            if count == 0:
                if package_ not in self.get_important_packages():
                    unused_packages.append(package_)
        return unused_packages

    def get_important_packages(self) -> Set[str]:
        return {"crap", "pipdeptree", "pip"}

    def remove_unused_packages(self):
        unused_packages = self.get_unused_packages()
        for package in unused_packages:
            subprocess.run(["pip3", "uninstall", "-y", package])
            print(f"Removed unused package: {package}")


# manager = CrapManager(path_="/root/open_source/crap/crap/cli.py")
manager = CrapManager(path_=".")
manager.run()
# print(manager.get_unused_packages())
manager.remove_unused_packages()
