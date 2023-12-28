from functools import lru_cache
from typing import List
import typer
import shutil
import pathlib
from typing_extensions import Annotated, Optional
from crap.crap_manager import CrapManager

__all__: List[str] = ["get_app"]

app = typer.Typer(no_args_is_help=True)


@app.command()
def crap(
    path_: Annotated[str, typer.Argument(help="path to file/files")] = ".",
    important: Optional[str] = typer.Option(
        None,
        "--important",
        "-i",
        help="Add a package to the list of important packages",
    ),
    remove: Optional[str] = typer.Option(
        None,
        "--remove",
        "-r",
        help="Remove a package from the list of important packages",
    ),
    flush: bool = typer.Option(
        False,
        "--flush",
        "-f",
        help="Remove all packages from the list of important packages",
    ),
    show: bool = typer.Option(
        False,
        "--show",
        "-s",
        help="Show all important packages",
    ),
    factory_reset: bool = typer.Option(
        False,
        "--factory-reset",
        "-fr",
        help="Reset all settings to default",
    ),
):
    if (
        sum(
            [
                bool(opt)
                for opt in [path_ != ".", important, remove, flush, show, factory_reset]
            ]
        )
        > 1
    ):
        print("Error: Options cannot be used together.")
        raise typer.Exit(code=1)

    if important:
        add_important_package(important)
    elif remove:
        remove_important_package(remove)
    elif flush:
        flush_important_packages()
    elif show:
        show_important_packages()
    elif factory_reset:
        factory_reset_important_packages()
    else:
        manager = CrapManager(path_=path_)
        manager.run()


def add_important_package(package: str, filename="important_packages.txt"):
    """
    Add a package to the list of important packages.

    Args:
        package (str): The name of the package to add.
        filename (str, optional): The name of the file to store the list of important packages. 
            Defaults to "important_packages.txt".
    """
    with open(f"{pathlib.Path(__file__).parent}/data/{filename}", "r+", encoding="utf-8") as file:
        existing_packages = {line.strip() for line in file}
        if package not in existing_packages:
            file.write(package + "\n")
            print(f"Added '{package}' to important packages")
        else:
            print(f"'{package}' is already listed as an important package")


def show_important_packages(filename="important_packages.txt") -> List[str]:
    """
    Display the list of important packages.

    Args:
        filename (str): The name of the file containing the list of important packages.
            Default is "important_packages.txt".

    Returns:
        List[str]: The list of important packages.

    """
    with open(f"{pathlib.Path(__file__).parent}/data/{filename}", "r", encoding="utf-8") as file:
        important_packages = [line.strip() for line in file]
        print("📦 Important packages:")
        for package in important_packages:
            print(f" - {package}")


def remove_important_package(package: str, filename="important_packages.txt"):
    """
    Removes a package from the list of important packages.

    Args:
        package (str): The name of the package to be removed.
        filename (str, optional): The name of the file containing the list of important packages.
            Defaults to "important_packages.txt".
    """
    filepath = f"{pathlib.Path(__file__).parent}/data/{filename}"
    with open(filepath, "r+", encoding="utf-8") as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate(0)
        for line in lines:
            if line.strip() != package:
                file.write(line)

        if package in (line.strip() for line in lines):
            print(f"Removed '{package}' from important packages")
        else:
            print(f"'{package}' was not found in important packages")



def flush_important_packages(filename="important_packages.txt"):
    """
    Flushes the important packages by removing the contents of the specified file.

    Args:
        filename (str, optional): The name of the file to flush. Defaults to "important_packages.txt".
    """
    filepath = f"{pathlib.Path(__file__).parent}/data/{filename}"
    with open(filepath, "w"):
        pass
    print("All important packages have been removed.")


def factory_reset_important_packages():
    """
    Reset the list of important packages to the default packages
    """
    DEFAULT_PACKAGES_FILE = "default_important_packages.txt"
    default_packages_path = (
        pathlib.Path(__file__).parent / "data" / DEFAULT_PACKAGES_FILE
    )
    important_packages_path = (
        pathlib.Path(__file__).parent / "data" / "important_packages.txt"
    )

    try:
        shutil.copyfile(default_packages_path, important_packages_path)
        print("Reset important packages to default")
    except FileNotFoundError:
        print(f"Default packages file '{DEFAULT_PACKAGES_FILE}' not found")

@lru_cache
def get_app():
    """
    Get the main typer cli app
    """
    return app()
