import subprocess
import json
from functools import lru_cache
from typing import List, Dict
import pathlib


def get_current_packages() -> set:
    """Get the current packages installed in the environment."""
    process = subprocess.run(["pip3", "freeze"], capture_output=True, text=True)
    output = process.stdout.strip()
    packages = set(line.split("==")[0] for line in output.split("\n"))
    return packages


def run_subprocess(command: list[str]) -> subprocess.CompletedProcess:
    """Run a given subprocess command."""
    try:
        return subprocess.run(command, capture_output=True, text=True)
    except Exception as ex:
        print(ex)
        return None


def execute_command_without_output(command: list[str]):
    """Execute a command without needing the output."""
    run_subprocess(command)


def get_package_counter_dict() -> Dict[str, int]:
    """Get a dictionary of package usage counters."""
    packages_ = get_current_packages()
    return {package: 0 for package in packages_}


def freeze_into_requirements():
    """Freeze current environment to requirements.txt."""
    req_path = pathlib.Path(__file__).parent / "data" / "req.txt"
    try:
        with open(req_path, "w") as file_:
            subprocess.run(["pip3", "freeze"], stdout=file_)
    except Exception as ex:
        print(ex)


def reinstall_from_requirements() -> None:
    """Reinstall packages from requirements.txt."""
    req_path = pathlib.Path(__file__).parent / "data" / "req.txt"
    execute_command_without_output(
        ["pip3", "install", "-r", req_path, "--no-cache-dir"]
    )


def uninstall_package(package_name: str):
    """Uninstall a given package."""
    execute_command_without_output(["pip3", "uninstall", "-y", package_name])


def pre_cleanup_with_ruff(path_):
    """
    Pre cleanup with ruff
    """
    execute_command_without_output(["ruff", "check", path_, "--fix"])
