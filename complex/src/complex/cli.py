"""Complex CLI."""

import click


@click.group
def main() -> None:
    """Complex CLI."""
    pass


@click.group
def awscli() -> None:
    """AWS CLI."""
    pass
