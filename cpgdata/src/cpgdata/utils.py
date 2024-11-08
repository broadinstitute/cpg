"""Utilities.

This module provide utility functions shared by other modules in the package.
"""

import json
import os
import re
import subprocess
from collections.abc import Sequence
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable, List, Optional

from joblib import Parallel, cpu_count, delayed
from tqdm import tqdm


def slice_iterable(iterable: Sequence, count: int) -> List[slice]:
    """Create slices of the given iterable.

    Parameters
    ----------
    iterable : Sequence
        A iterable to create slices.
    count : int
        Number of slices to create.

    Returns
    -------
    List[slice]
        A list of slice.

    """
    slices = []
    if count == 0:
        slices.append(slice(0, len(iterable)))
        return slices
    if len(iterable) < count:
        raise Exception(
            f"Length of iterable: {len(iterable)} is less than count: {count}"
        )
    for i in range(0, len(iterable), len(iterable) // count):
        slices.append(slice(i, i + len(iterable) // count))
    return slices


def parallel(
    iterable: Sequence,
    func: Callable[..., Any],
    args: List[Any] = [],
    jobs: Optional[int] = None,
    timeout: Optional[float] = None,
) -> Any:  # noqa: ANN401
    """Distribute process on iterable.

    Parameters
    ----------
    iterable : Sequence
        Iterable to chunk and distribute.
    func : Callable[[List[Any], Any], Any]
        Function to distribute.
    args : List[Any], optional
        Optional addtional args for the function, by default []
    jobs : int, optional
        Number of jobs to launch, by default None
    timeout: float, optional
        Timeout for worker processes.

    Returns
    -------
    Any
        A list of outputs genetated by function.

    """
    jobs = jobs or cpu_count()
    if len(iterable) <= jobs:
        jobs = len(iterable)
    slices = slice_iterable(iterable, jobs)
    return Parallel(n_jobs=jobs, timeout=timeout)(
        delayed(func)(chunk, *args, idx % jobs)
        for idx, chunk in enumerate([iterable[s] for s in slices])
    )


def get_package_root_path() -> Path:
    """Get path of the package root.

    Returns
    -------
        Path
            Package root path

    """
    return Path(__file__).parents[1].absolute()


def download_s3_file(
    bucket: str, key: str, out_path: Path, no_progress: bool = True
) -> None:
    """Download file from S3 using aws cli.

    Parameters
    ----------
    bucket : str
        S3 bucket identifier.
    key : str
        S3 bucket full key.
    out_path : Path
        Path to save the object.
    no_progress: bool
        Flag to control progress bar.

    """
    cli_args = [
        "s3",
        "cp",
        f"s3://{bucket.rstrip('/')}/{key.lstrip('/')}",
        str(out_path.absolute()),
    ]
    if no_progress is True:
        cli_args = cli_args + ["--no-progress"]
    cli_args = cli_args + ["--no-sign-request"]
    subprocess.run(["aws"] + cli_args)


def download_s3_files(
    key_list: List[str],
    bucket: str,
    out_path: Path,
    flatten: bool = False,
    idx: int = 0,
) -> None:
    """Download a list of S3 objects.

    Parameters
    ----------
    key_list : List[str]
        List of S3 keys.
    bucket : str
        Name of the S3 bucket.
    out_path : Path
        Path to save files.
    flatten : bool
        Save all files in single directory ignoring prefix structure.
    idx : int
        Index of the worker if available.

    """
    w_id = os.getpid()
    for key in tqdm(key_list, desc=f"Downloading files: Worker {w_id}", position=idx):
        if flatten is True:
            write_path = out_path.joinpath(key.split("/")[-1])
        else:
            write_path = out_path.joinpath(key)
        download_s3_file(bucket, key, write_path)


def download_s3_prefix(
    bucket: str,
    prefix: str,
    out_path: Path,
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    no_progress: bool = False,
) -> None:
    """Download files under an S3 prefix using aws cli.

    Parameters
    ----------
    bucket : str
        S3 bucket identifier.
    prefix : str
        S3 bucket full prefix.
    out_path : Path
        Path to save the object.
    include: Optional[str]
        regex pattern to include files to download.
    exclude: Optional[str]
        regex pattern to exclude files to download.
    no_progress: bool
        Flag to control display of transfer progress. Defaults to False.

    """
    cli_args = [
        "s3",
        "cp",
        f"s3://{bucket.rstrip('/')}/{prefix.lstrip('/')}",
        str(out_path.absolute()),
        "--recursive",
    ]
    if include is not None:
        cli_args = cli_args + ["--include", include]
    if exclude is not None:
        cli_args = cli_args + ["--exclude", exclude]
    if no_progress is True:
        cli_args = cli_args + ["--no-progress"]
    cli_args = cli_args + ["--no-sign-request"]
    subprocess.run(["aws"] + cli_args)


def sync_s3_prefix(
    bucket: str,
    prefix: str,
    out_path: Path,
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    no_progress: bool = False,
) -> None:
    """Download files under an S3 prefix using aws cli.

    Parameters
    ----------
    bucket : str
        S3 bucket identifier.
    prefix : str
        S3 bucket full prefix.
    out_path : Path
        Path to save the object.
    include: Optional[str]
        regex pattern to include files to download.
    exclude: Optional[str]
        regex pattern to exclude files to download.
    no_progress: bool
        Flag to control display of transfer progress. Defaults to False.

    """
    cli_args = [
        "s3",
        "sync",
        f"s3://{bucket.rstrip('/')}/{prefix.lstrip('/')}",
        str(out_path.absolute()),
    ]
    if exclude is not None:
        cli_args = cli_args + ["--exclude", exclude]
    if include is not None:
        cli_args = cli_args + ["--include", include]
    if no_progress is True:
        cli_args = cli_args + ["--no-progress"]
    cli_args = cli_args + ["--no-sign-request"]
    subprocess.run(["aws"] + cli_args)


BLANK_RGX = re.compile(r" +")


def parse_ls_out(line: str) -> str:
    """Parse s3 prefix path from aws cli ls output.

    Parameters
    ----------
    line : str
        AWS Cli ls output line.

    Returns
    -------
    str
        Parsed S3 prefix path

    """
    line = line.rstrip("\n")
    line = line.replace("//", "/")
    elems = BLANK_RGX.split(line, maxsplit=3)
    return elems[-1]


def ls_s3_prefix(
    bucket: str,
    prefix: str,
    recursive: bool = False,
) -> list:
    """Download files under an S3 prefix using aws cli.

    Parameters
    ----------
    bucket : str
        S3 bucket identifier.
    prefix : str
        S3 bucket full prefix.
    out_path : Path
        Path to save the object.
    recursive: bool
        Flag to allow recursive listing of files. Defaults to False.

    """
    bucket = bucket.strip("/")
    prefix = prefix.lstrip("/")
    cli_args = [
        "s3",
        "ls",
        f"s3://{bucket}/{prefix}",
    ]
    out_list = []
    if recursive is not False:
        cli_args = cli_args + ["--recursive"]
    cli_args = cli_args + ["--no-sign-request"]
    ls_prefix = subprocess.run(["aws"] + cli_args, capture_output=True, text=True)
    for line in ls_prefix.stdout.splitlines():
        out_list.append(f"{parse_ls_out(line)}")
    return out_list


def sync_inventory(bucket: str, prefix: str, out_path: Path, revision: int = 0) -> None:
    """Sync inventory files of a specific revision.

    Parameters
    ----------
    bucket : str
        Name of the bucket.
    prefix : str
        Prefix for the revisions.
    out_path : Path
        Path to save synced files.
    revision : int
        Revision to sync. 0 is the latest revision.

    """
    dirs = ls_s3_prefix(bucket, prefix)
    dirs.sort()
    manifest_revision = dirs[-(abs(revision) + 3)]
    print(manifest_revision)
    sync_s3_prefix(
        bucket,
        prefix,
        exclude="*",
        include=f"*{manifest_revision}*",
        no_progress=False,
        out_path=out_path,
    )
    manifest_json = out_path.joinpath(f"{manifest_revision}/manifest.json")
    with manifest_json.open() as f:
        manifest = json.load(f)
        total_size = 0
        for file in manifest["files"]:
            total_size += file["size"]
        print(f"Total no of file: {len(manifest['files'])}")
        print(f"Total file size: ~{round(total_size / (1024 * 1024 * 1024))}GB")
        file_keys = [obj["key"] for obj in manifest["files"]]
        out_path = out_path.joinpath("data")
        out_path.mkdir(parents=True, exist_ok=True)
        parallel(file_keys, download_s3_files, [bucket, out_path, True])
