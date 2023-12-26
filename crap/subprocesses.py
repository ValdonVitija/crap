import subprocess
import json
from functools import lru_cache


@lru_cache
def get_installed_packages_as_list():
    """ """
    try:
        process = subprocess.run(
            ["pipdeptree", "--json"], capture_output=True, text=True
        )
        json_output = json.loads(process.stdout)
        return [pack["package"]["package_name"] for pack in json_output]
    except Exception as ex:
        print(ex)


@lru_cache
def get_package_counter_dict():
    """ """
    try:
        process = subprocess.run(
            ["pipdeptree", "--json"], capture_output=True, text=True
        )
        json_output = json.loads(process.stdout)
        new_json = {}

        for item in json_output:
            package_name = item["package"]["package_name"]
            new_json[package_name] = 0

        return new_json
    except Exception as ex:
        print(ex)


@lru_cache
def freeze_into_requirements_txt():
    """

    Freeze dependencies to requirements.txt
    """
    try:
        subprocess.run(["pip3", "freeze", "> requirements.txt"])
        print("Freezed dependencies to requirements.txt")
    except Exception as ex:
        print(ex)


@lru_cache
def reinstall_dependencies_from_requirements_txt():
    """
    Reinstall dependencies from requirements.txt
    """
    try:
        subprocess.run(["pip3", "install", "-r", "requirements.txt"])
        print("Reinstalled dependencies from requirements.txt")
    except Exception as ex:
        print(ex)
