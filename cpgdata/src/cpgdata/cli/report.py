"""Report cli commands."""

from pathlib import Path

import click

from cpgdata.pipe import validate


@click.command()
@click.option(
    "-i",
    "--inp",
    type=click.Path(),
    help="Path to read inventory files",
    required=True,
)
@click.option(
    "-o",
    "--out",
    type=click.Path(),
    help="Path to write generated measurement files",
    required=True,
)
@click.option(
    "-f", "--force", is_flag=True, help="Force re-generating all measurement files."
)
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def sync(inp: str, out: str, force: bool, debug: bool) -> None:
    """Run validation.

    Parameters
    ----------
    inp : str
        Path to the inventory.
    out : str
        Path to output reports.
    force : bool
        Force re-validation.
    debug : bool
        Run in debug mode.
    """
    validate(Path(inp), Path(out))


@click.command()
@click.option(
    "-i",
    "--inp",
    type=click.Path(),
    help="Path to read inventory files",
    required=True,
)
@click.option(
    "-o",
    "--out",
    type=click.Path(),
    help="Path to write generated measurement files",
    required=True,
)
@click.option(
    "-f", "--force", is_flag=True, help="Force re-generating all measurement files."
)
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def gen(inp: str, out: str, force: bool, debug: bool) -> None:
    """Generate reports.

    Parameters
    ----------
    inp : str
        Path to the inventory.
    out : str
        Path to output reports.
    force : bool
        Force re-validation.
    debug : bool
        Run in debug mode.
    """
    validate(Path(inp), Path(out))


@click.group
def report() -> None:
    """CPG Report commands."""
    pass


report.add_command(sync)
report.add_command(gen)
