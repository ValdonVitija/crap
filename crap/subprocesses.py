import subprocess
import json
from functools import lru_cache
from typing import List, Dict


# @lru_cache
# def get_installed_packages_as_list():
#     """ """
#     try:
#         json_output = get_json_output()
#         return [pack["package"]["package_name"] for pack in json_output]
#     except Exception as ex:
#         print(ex)

# @lru_cache
# def get_json_output():
#     process = subprocess.run(
#             ["pipdeptree", "--json"], capture_output=True, text=True
#         )
#     json_output = json.loads(process.stdout)
#     return json_output


# @lru_cache
# def get_package_counter_dict():
#     """ """
#     try:
#         process = subprocess.run(
#             ["pipdeptree", "--json"], capture_output=True, text=True
#         )
#         json_output = json.loads(process.stdout)
#         new_json = {}

#         for item in json_output:
#             package_name = item["package"]["package_name"]
#             new_json[package_name] = 0

#         return new_json
#     except Exception as ex:
#         print(ex)


# @lru_cache
# def freeze_into_requirements_txt():
#     """
#     Freeze dependencies to requirements.txt
#     """
#     try:
#         subprocess.run(["pip3", "freeze", "> requirements.txt"])
#         print("Freezed dependencies to requirements.txt")
#     except Exception as ex:
#         print(ex)


# def reinstall_dependencies_from_requirements_txt():
#     """
#     Reinstall dependencies from requirements.txt
#     """
#     try:
#         subprocess.run(["pip3", "install", "-r", "requirements.txt","--no-cache-dir"])
#         print("Reinstalled dependencies from requirements.txt")
#     except Exception as ex:
#         print(ex)

# def uninstall_package(package):
#     """
#     Uninstall package
#     """
#     subprocess.run(["pip3", "uninstall", "-y", package])
#     print(f"Removed unused package: {package}")



# def pre_cleanup_with_ruff(path_):
#     """
#     Pre cleanup with ruff
#     """
#     try:
#         subprocess.run(["ruff", "check", path_,"--fix"])
#         print("Pre cleanup with ruff")
#     except Exception as ex:
#         print(ex)




#####
#####

@lru_cache
def get_json_output():
    process = subprocess.run(
            ["pipdeptree", "--json"], capture_output=True, text=True
        )
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

@lru_cache
def get_package_counter_dict() -> Dict[str, int]:
    """Get a dictionary of package usage counters."""
    json_output = get_json_output()
    return {item["package"]["package_name"]: 0 for item in json_output}

def freeze_into_requirements():
    """Freeze current environment to requirements.txt."""
    execute_command_without_output(["pip3", "freeze", "> requirements.txt"])

def reinstall_from_requirements():
    """Reinstall packages from requirements.txt."""
    execute_command_without_output(["pip3", "install", "-r", "requirements.txt", "--no-cache-dir"])

def uninstall_package(package_name: str):
    """Uninstall a given package."""
    execute_command_without_output(["pip3", "uninstall", "-y", package_name])


def pre_cleanup_with_ruff(path_):
    """
    Pre cleanup with ruff
    """
    execute_command_without_output(["ruff", "check", path_,"--fix"])