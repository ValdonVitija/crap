from functools import lru_cache
from typing import List
import typer
from typing_extensions import Annotated
from crap.crap_manager import CrapManager

__all__: List[str] = ["get_app"]

app = typer.Typer(no_args_is_help=True)

@app.command()
def crap(
    path_: Annotated[str, typer.Argument(help="path to file/files")] = ".",
):
    """
    
    """
    manager = CrapManager(path_=path_)
    manager.run()

@lru_cache
def get_app():
    """
    Get the main typer cli app
    """
    return app()