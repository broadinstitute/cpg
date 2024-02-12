"""CPG CLI."""

import click

from cpgdata.cli.index import index
from cpgdata.cli.inventory import inventory
from cpgdata.cli.report import report


@click.group
def main() -> None:
    """CPG CLI."""
    pass


main.add_command(index)
main.add_command(inventory)
main.add_command(report)
