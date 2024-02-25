import typer
import uvicorn

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
