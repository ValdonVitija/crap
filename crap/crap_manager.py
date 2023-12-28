# import ast
# import subprocess
# import sys
# import os
# import shutil
# from typing import List, Tuple, Set
# import pathlib


# # from crap.subprocesses import (
# from subprocesses import (
#     get_installed_packages,
#     get_package_counter_dict,
#     uninstall_package,
#     pre_cleanup_with_ruff,
#     freeze_into_requirements,
#     reinstall_from_requirements
# )
# # from crap.module_checker import (
# from module_checker import (
#     ImportsVisitor,
# )


# class CrapManager:
#     """ """

#     __slots__ = ("path_", "pack_counter")

#     def __init__(self, path_: str) -> None:
#         self.path_ = pathlib.Path(path_).absolute()
#         self.pack_counter = get_package_counter_dict()

#     def run(self):
#         if not self.path_.exists():
#             raise FileNotFoundError("File/Dir not found")

#         if self.path_.is_file():
#             self._check_file(self.path_)
#         elif self.path_.is_dir():
#             self._check_directory()

#         self.remove_unused_packages()
#         freeze_into_requirements()
#         reinstall_from_requirements()


#     def _check_file(self, file_path: pathlib.Path) -> None:
#         print(file_path)
#         pre_cleanup_with_ruff(file_path)
#         code = file_path.read_text()
#         tree_ = ast.parse(code)
#         visitor = ImportsVisitor()
#         visitor.visit(tree_)
#         for package_ in get_installed_packages():
#             if package_ in visitor.imported_modules:
#                 self.pack_counter[package_] += 1

#     def is_likely_venv(self, path):
#         """
#         Check if the given path is likely a virtual environment.
#         """
#         if sys.platform == "linux":
#             venv_indicators = {"bin", "include", "lib", "pyvenv.cfg"}
#         elif sys.platform == "win32":
#             venv_indicators = {"Scripts", "Include", "Lib", "pyvenv.cfg"}

#         if all(
#             os.path.exists(os.path.join(path, indicator))
#             for indicator in venv_indicators
#         ):
#             return True

#         return False

#     def _check_directory(self):
#         excluded_dirs = {"__pycache__", ".git"}

#         for dirpath, dirnames, filenames in os.walk(self.path_):
#             dirnames[:] = [
#                 d
#                 for d in dirnames
#                 if not self.is_likely_venv(os.path.join(dirpath, d))
#                 and d not in excluded_dirs
#             ]
#             for filename in filenames:
#                 if filename.endswith(".py"):
#                     file_path = pathlib.Path(dirpath) / filename
#                     self._check_file(file_path)

#     def get_unused_packages(self) -> List[str]:
#         unused_packages = []
#         for package_, count in self.pack_counter.items():
#             if count == 0:
#                 if package_ not in self.get_important_packages():
#                     unused_packages.append(package_)
#         return unused_packages

#     def get_important_packages(self) -> Set[str]:
#         return {"crap", "pipdeptree", "pip","ruff"}

#     def remove_unused_packages(self):
#         unused_packages = self.get_unused_packages()
#         for package in unused_packages:
#             uninstall_package(package)


# # manager = CrapManager(path_="/root/open_source/crap/crap/cli.py")
# manager = CrapManager(path_="/root/temp_dir/code_exec/a.py")
# manager.run()
# # print(manager.get_unused_packages())
# # manager.remove_unused_packages()


######
######
######
######
######


# class PythonFileAnalyzer:
#     def __init__(self, file_path: pathlib.Path):
#         self.file_path = file_path
#         self.imported_modules = set()

#     def analyze(self):
#         code = self.file_path.read_text()
#         tree = ast.parse(code)
#         visitor = ImportsVisitor()
#         visitor.visit(tree)
#         self.imported_modules = visitor.imported_modules


# class VirtualEnvChecker:
#     def __init__(self):
#         self.venv_indicators = {
#             "linux": {"bin", "include", "lib", "pyvenv.cfg"},
#             "win32": {"Scripts", "Include", "Lib", "pyvenv.cfg"}
#         }

#     def is_likely_venv(self, path):
#         platform = sys.platform
#         indicators = self.venv_indicators.get(platform, set())
#         return all(os.path.exists(os.path.join(path, ind)) for ind in indicators)


# class PackageUsageCounter:
#     def __init__(self):
#         self.pack_counter = get_package_counter_dict()

#     def increment_package_count(self, package):
#         if package in self.pack_counter:
#             self.pack_counter[package] += 1

#     def get_unused_packages(self, important_packages) -> List[str]:
#         return [pkg for pkg, count in self.pack_counter.items() if count == 0 and pkg not in important_packages]


import os
from typing import Set
import pathlib
from crap.file_analyzer import PythonFileAnalyzer
from crap.virtual_env_checker import VirtualEnvChecker
from crap.package_usage_counter import PackageUsageCounter
from crap.subprocesses import (
    get_installed_packages,
    uninstall_package,
    pre_cleanup_with_ruff,
    reinstall_from_requirements,
    freeze_into_requirements
)


class CrapManager:
    __slots__ = ("path_", "venv_checker", "package_usage_counter")

    def __init__(self, path_: str):
        self.path_ = pathlib.Path(path_).absolute()
        self.venv_checker = VirtualEnvChecker()
        self.package_usage_counter = PackageUsageCounter()

    def run(self):
        if not self.path_.exists():
            raise FileNotFoundError("File/Dir not found")

        self._process_path()
        self._cleanup_packages()
        """
        After we cleanup remove the unused packages, we need to freeze the current environment to requirements.txt.
        The left packages in requirements.txt are the ones that are actually used by the project. These packages might have dependecies
        that we have deleted since they haven't directly been used by the project. So we need to reinstall the packages from requirements.txt.
        When using pip to install packages, any dependecy gets installed automatically. So we don't need to worry about that.
        """
        freeze_into_requirements()
        reinstall_from_requirements()

    def _process_path(self):
        if self.path_.is_file():
            self._analyze_file(self.path_)
        elif self.path_.is_dir():
            self._analyze_directory()

    def _analyze_file(self, file_path):
        pre_cleanup_with_ruff(file_path)
        analyzer = PythonFileAnalyzer(file_path)
        analyzer.analyze()
        for package in get_installed_packages():
            if package in analyzer.imported_modules:
                self.package_usage_counter.increment_package_count(package)


    def _analyze_directory(self):
        excluded_dirs = self._get_excluded_dirs()

        for dirpath, dirnames, filenames in os.walk(self.path_):
            dirnames[:] = [
                d
                for d in dirnames
                if not self.venv_checker.is_likely_venv(os.path.join(dirpath, d))
                and d not in excluded_dirs
            ]

            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = pathlib.Path(dirpath) / filename
                    self._analyze_file(file_path)

    def _cleanup_packages(self):
        important_packages = self._get_important_packages()
        unused_packages = self.package_usage_counter.get_unused_packages(
            important_packages
        )
        for package in unused_packages:
            uninstall_package(package)

    @staticmethod
    def _get_important_packages() -> Set[str]:
        with open(f"{pathlib.Path(__file__).parent}/data/important_packages.txt", "r") as file:
            return {line.strip() for line in file}

    @staticmethod
    def _get_excluded_dirs() -> Set[str]:
        return {"__pycache__", ".git"}
