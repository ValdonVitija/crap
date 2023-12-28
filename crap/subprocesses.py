import subprocess
import json
from functools import lru_cache
from typing import List, Dict
import pathlib


@lru_cache
def get_json_output():
    process = subprocess.run(["pipdeptree", "--json"], capture_output=True, text=True)
    json_output = json.loads(process.stdout)
    return json_output


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


@lru_cache
def get_installed_packages() -> List[str]:
    """Get a list of installed packages."""
    json_output = get_json_output()

    return [pack["package"]["package_name"] for pack in json_output]


def get_package_counter_dict() -> Dict[str, int]:
    """Get a dictionary of package usage counters."""
    json_output = get_json_output()
    return {item["package"]["package_name"]: 0 for item in json_output}


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

