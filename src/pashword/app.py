import typer

from pashword.lib import generate_pashword
from pashword.lib import sanitize

app = typer.Typer(add_completion=False)


@app.command(name="generate")
def generate(
    website: str = typer.Argument(..., envvar=["PASHWORD_WEBSITE"]),
    username: str = typer.Argument(..., envvar=["PASHWORD_USERNAME"]),
    secret: str = typer.Option(..., prompt=True, hide_input=True, envvar=["PASHWORD_SECRET"]),
    numbers: bool = typer.Option(True),
    symbols: bool = typer.Option(True),
    length: int = typer.Option(32, min=16),
):
    pashword = generate_pashword(website=website, username=username, secret=secret, length=length)
    if not (numbers and symbols):
        pashword = sanitize(pashword, symbols=symbols, numbers=numbers)
    print(pashword)


@app.command(name="sanitize")
def do_sanitize(
    secret: str,
    numbers: bool = typer.Option(False),
    symbols: bool = typer.Option(False),
):
    sanitized_secret = sanitize(secret, symbols=symbols, numbers=numbers)
    print(sanitized_secret)
