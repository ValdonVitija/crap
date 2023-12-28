from functools import lru_cache
from typing import List
import typer
from typing_extensions import Annotated, Optional
from crap.crap_manager import CrapManager
from crap.package_management import PackageManagement

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

    package_management = PackageManagement()
    if important:
        package_management.add_important_package(important)
    elif remove:
        package_management.remove_important_package(remove)
    elif flush:
        package_management.flush_important_packages()
    elif show:
        package_management.show_important_packages()
    elif factory_reset:
        package_management.factory_reset_important_packages()
    else:
        manager = CrapManager(path_=path_)
        manager.run()


@lru_cache
def get_app():
    """
    Get the main typer cli app
    """
    return app()
