import os
from typing import Set
from tqdm import tqdm 
import pathlib
from crap.file_analyzer import PythonFileAnalyzer
from crap.virtual_env_checker import VirtualEnvChecker
from crap.package_usage_counter import PackageUsageCounter
from crap.subprocesses import (
    uninstall_package,
    pre_cleanup_with_ruff,
    reinstall_from_requirements,
    freeze_into_requirements,
    get_current_packages
)


class CrapManager:
    __slots__ = ("path_", "venv_checker", "package_usage_counter", "deleted_packages")

    def __init__(self, path_: str):
        self.path_ = pathlib.Path(path_).absolute()
        self.venv_checker = VirtualEnvChecker()
        self.package_usage_counter = PackageUsageCounter()
        self.deleted_packages = set()
    
    def run(self):
        if not self.path_.exists():
            raise FileNotFoundError("File/Dir not found")

        total_steps = 4  
        bar_width = 100  
        bar_color = 'red'  

        with tqdm(total=total_steps, ncols=bar_width, colour=bar_color) as pbar:
            self._process_path()
            pbar.update(1)  

            initial_packages = get_current_packages()
            pbar.update(1) 

            self._cleanup_packages()
            pbar.update(1)  

            freeze_into_requirements()
            reinstall_from_requirements()
            pbar.update(1)  

            final_packages = get_current_packages()
            self.deleted_packages = initial_packages - final_packages

        print()
        self.print_deleted_packages()

    def _process_path(self):
        if self.path_.is_file():
            self._analyze_file(self.path_)
        elif self.path_.is_dir():
            self._analyze_directory()

    def _analyze_file(self, file_path):
        pre_cleanup_with_ruff(file_path)
        analyzer = PythonFileAnalyzer(file_path)
        analyzer.analyze()
        for package in get_current_packages():
            if package in analyzer.imported_modules:
                self.package_usage_counter.increment_package_count(package)

    def _analyze_directory(self):
        """
        Analyzes the directory and its subdirectories, excluding certain directories,
        and analyzes each Python file found.

        This method walks through the directory tree using os.walk() function,
        excluding directories that are likely to be virtual environments or specified
        in the excluded_dirs list. For each file with a ".py" extension, it calls
        the _analyze_file() method to perform analysis.

        Parameters:
            None

        Returns:
            None
        """
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
            self.deleted_packages.add(package)

    @staticmethod
    def _get_important_packages() -> Set[str]:
        """
        Retrieves the important packages from the important_packages.txt file.
        These packages cannot be removed, because they are most likely dev tools that do not
        get imported in the code.

        Returns:
            A set of strings representing the important packages.
        """
        with open(
            f"{pathlib.Path(__file__).parent}/data/important_packages.txt",
            "r",
            encoding="utf-8",
        ) as file:
            return {line.strip() for line in file}

    def print_deleted_packages(self):
        print("🗑️📦Deleted packages:")
        for package in self.deleted_packages:
            print(f" - {package}")

    @staticmethod
    def _get_excluded_dirs() -> Set[str]:
        """
        These directories are excluded from the analysis.
        """
        return {"__pycache__", ".git"}
