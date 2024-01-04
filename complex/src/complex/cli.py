"""Complex CLI."""

from collections import OrderedDict
from pathlib import Path
from typing import Optional

import click

module_map = OrderedDict({"s3_object_tags": ""})


@click.command(name="list")
def list_() -> None:
    """List available stacks."""
    click.echo(module_map)


@click.command
@click.option(
    "-s",
    "--stack",
    type=click.Choice([k for k in module_map.keys()]),
    required=True,
    help="Name of the stack to deploy.",
)
@click.option(
    "-e",
    "--env",
    type=click.Choice(["prod", "staging", "test"]),
    required=True,
    help="Project Environment to deploy.",
)
def up(stack: str, env: str) -> None:
    """Deploy selected stack."""
    click.echo(f"Deploying {stack} in {env}")
    if stack == "hanaski-soldiers":
        module = module_map["hanaski-soldiers"](stack, env)
        stack = module.create_stack(module.create_pulumi_config())
        stack.refresh(on_output=print)
        stack.up(on_output=print)


@click.command
@click.option(
    "-s",
    "--stack",
    type=click.Choice([k for k in module_map.keys()]),
    required=True,
    help="Name of the stack to deploy.",
)
@click.option(
    "-e",
    "--env",
    type=click.Choice(["prod", "staging", "test"]),
    required=True,
    help="Project Environment to deploy.",
)
def down(stack: str, env: str) -> None:
    """Destroy selected stack."""
    click.echo(f"Destroying {stack} in {env}")
    if stack == "hanaski-soldiers":
        module = module_map["hanaski-soldiers"](stack, env)
        stack = module.create_stack(module.create_pulumi_config())
        stack.destroy(on_output=print)
        stack.up(on_output=print)


@click.command
@click.argument("bucket name", required=False)
def ls(bucket: Optional[str]) -> None:
    """Fetch S3 bucket details."""


@click.group
def stack() -> None:
    """Stack commands."""
    pass


stack.add_command(list_)
stack.add_command(up)
stack.add_command(down)


@click.group
def s3() -> None:
    """S3 commnd group."""
    pass


@click.group
def main() -> None:
    """Complex CLI."""
    pass


main.add_command(stack)


QUERY = """'Metrics':[
    {'Dimensions': [{}]}
    ]"""


{
    "Metrics": [
        {
            "Namespace": "AWS/S3",
            "MetricName": "BucketSizeBytes",
            "Dimensions": [
                {"Name": "StorageType", "Value": "DeepArchiveObjectOverhead"},
                {"Name": "BucketName", "Value": "imaging-platform"},
            ],
        },
        {
            "Namespace": "AWS/S3",
            "MetricName": "NumberOfObjects",
            "Dimensions": [
                {"Name": "StorageType", "Value": "AllStorageTypes"},
                {"Name": "BucketName", "Value": "imaging-platform-cold"},
            ],
        },
    ]
}

from boto import c
