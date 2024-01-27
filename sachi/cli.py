from importlib.resources import files
from pathlib import Path
from typing import Annotated

import rich
import typer

import sachi.resources
from sachi.config import get_config_path
from sachi.engine import MediaType, SachiEngine

app = typer.Typer()


@app.command()
def config():
    config_path = get_config_path()
    if not config_path.exists():
        rich.print("No config file found, creating one")
        content = files(sachi.resources).joinpath("config.toml").read_bytes()
        config_path.write_bytes(content)
    rich.print(f'Editing "{config_path}"')
    typer.edit(filename=config_path.as_posix())


@app.command()
def series(
    file_or_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=True,
            writable=True,
            readable=True,
        ),
    ],
):
    SachiEngine(MediaType.SERIES)(file_or_dir)


@app.command()
def movie(
    file_or_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=True,
        ),
    ],
):
    SachiEngine(MediaType.MOVIE)(file_or_dir)
