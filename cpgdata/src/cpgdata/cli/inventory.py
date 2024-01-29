"""Inventory cli commands."""

from pathlib import Path
from typing import Optional

import click

from cpgdata.pipe import check as _check
from cpgdata.pipe import measure as _measure
from cpgdata.pipe import validate
from cpgdata.utils import sync_inventory


@click.command(help="Sync inventory files to a local directory.")
@click.option(
    "-o",
    "--out",
    type=click.Path(),
    help="Path to write generated measurement files",
    required=True,
)
@click.option(
    "-b",
    "--bucket",
    type=click.STRING,
    help="Name of the bucket",
    default="cellpainting-gallery-inventory",
)
@click.option(
    "-p",
    "--prefix",
    type=click.STRING,
    help="Prefix of the bucket",
    default="cellpainting-gallery/whole_bucket/",
)
@click.option(
    "-f", "--force", is_flag=True, help="Force re-generating all measurement files."
)
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def sync(out: str, bucket: str, prefix: str, force: bool, debug: bool) -> None:
    """Sync inventory files to a local directory.

    Parameters
    ----------
    out : str
        Path to output inventory.
    bucket: str
        Bucket name.
    prefix: str
        Bucket prefix.
    force : bool
        Force re-validation.
    debug : bool
        Run in debug mode.
    """
    sync_inventory(bucket, prefix, Path(out))


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
    "-j",
    "--jobs",
    type=click.INT,
    help="Number of jobs to launch.",
)
@click.option(
    "-f", "--force", is_flag=True, help="Force re-generating all measurement files."
)
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def gen(inp: str, out: str, jobs: Optional[int], force: bool, debug: bool) -> None:
    """Generate inventory.

    Parameters
    ----------
    inp : str
        Path to the inventory.
    out : str
        Path to output reports.
    jobs: Optional[int]
        Number of jobs to launch.
    force : bool
        Force re-validation.
    debug : bool
        Run in debug mode.
    """
    validate(Path(inp), Path(out), jobs=jobs)


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
    help="Path to write output files",
    required=True,
)
@click.option(
    "-j",
    "--jobs",
    type=click.INT,
    help="Number of jobs to launch.",
)
@click.option(
    "-f", "--force", is_flag=True, help="Force re-generating all measurement files."
)
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def val(inp: str, out: str, jobs: Optional[int], force: bool, debug: bool) -> None:
    """Run validation.

    Parameters
    ----------
    inp : str
        Path to the inventory.
    out : str
        Path to output reports.
    jobs: Optional[int]
        Number of jobs to launch.
    force : bool
        Force re-validation.
    debug : bool
        Run in debug mode.
    """
    validate(Path(inp), Path(out), jobs=jobs)


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
    "-j",
    "--jobs",
    type=click.INT,
    help="Number of jobs to launch.",
)
@click.option(
    "-f", "--force", is_flag=True, help="Force re-generating all measurement files."
)
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def measure(inp: str, out: str, jobs: Optional[int], force: bool, debug: bool) -> None:
    """Run measurement module.

    Parameters
    ----------
    inp : str
        Path to the inventory.
    out : str
        Path to output reports.
    jobs: Optional[int]
        Number of jobs to launch.
    force : bool
        Force re-validation.
    debug : bool
        Run in debug mode.
    """
    _measure(Path(inp), Path(out), jobs=jobs)


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
    "-j",
    "--jobs",
    type=click.INT,
    help="Number of jobs to launch.",
)
@click.option(
    "-f", "--force", is_flag=True, help="Force re-generating all measurement files."
)
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def check(inp: str, out: str, jobs: Optional[int], force: bool, debug: bool) -> None:
    """Run check module.

    Parameters
    ----------
    inp : str
        Path to the inventory.
    out : str
        Path to output reports.
    jobs: Optional[int]
        Number of jobs to launch.
    force : bool
        Force re-validation.
    debug : bool
        Run in debug mode.
    """
    _check(Path(inp), Path(out), jobs=jobs)


@click.group
def inventory() -> None:
    """CPG Inventory commands."""
    pass


inventory.add_command(val)
inventory.add_command(sync)
inventory.add_command(gen)
inventory.add_command(measure)
inventory.add_command(check)
