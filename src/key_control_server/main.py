import typer
import uvicorn
from ruamel.yaml import YAML

from key_control_server.globals import config_file

# Read allowed keys
yaml = YAML()

app = typer.Typer()


@app.command()
def up(
    host: str = typer.Option(metavar="-h", default="0.0.0.0"),
    port: int = typer.Option(metavar="-p", default=80),
    ):
    """
    Start key control server
    """
    uvicorn.run(
        "key_control_server.server:app",
        host=host,
        port=port,
        log_level="info",
    )


@app.command()
def list():
    """
    Show allowed keys
    """
    with open(config_file, "r") as stream:
        read = yaml.load(stream)

    for key in read["allowed_keys"]:
        typer.echo(key)


@app.command()
def add(new_key: str):
    """
    Add to allowed keys
    """
    with open(config_file, "r") as stream:
        read = yaml.load(stream)

    read["allowed_keys"].append(new_key)

    with open(config_file, "wb") as stream:
        yaml.dump(read, stream)

    typer.echo(f"Added {new_key}")


@app.command(name="del")
def delete(new_key: str):
    """
    Delete from allowed keys
    """
    with open(config_file, "r") as stream:
        read = yaml.load(stream)

    try:
        read["allowed_keys"].remove(new_key)
    except ValueError:
        raise Exception(f"Key '{new_key}' not found")

    with open(config_file, "wb") as stream:
        yaml.dump(read, stream)

    typer.echo(f"Removed {new_key}")