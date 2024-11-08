"""Index cli commands."""

from pathlib import Path

import click

from cpgdata.utils import sync_s3_prefix


@click.command(help="Sync index files to a local directory.")
@click.option(
    "-o",
    "--out",
    type=click.Path(),
    help="Path to write index files",
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
    default="cellpainting-gallery/index",
)
@click.option("-f", "--force", is_flag=True, help="Force re-sync all index files.")
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode.")
def sync(out: str, bucket: str, prefix: str, force: bool, debug: bool) -> None:
    """Sync index files to a local directory.

    Parameters
    ----------
    out : str
        Path to output index.
    bucket: str
        Bucket name.
    prefix: str
        Bucket prefix.
    force : bool
        Force re-sync of all index files.
    debug : bool
        Run in debug mode.

    """
    sync_s3_prefix(bucket, prefix, Path(out))


@click.group
def index() -> None:
    """CPG Index commands."""
    pass


index.add_command(sync)
