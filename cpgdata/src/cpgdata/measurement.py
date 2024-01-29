"""Measurements for parsers.

This module provide pure functions to generate measurements
for parsed files and directories either for the inventory file
or S3 API.
"""
from functools import lru_cache
from typing import Any, List

from pydantic import ValidationInfo


@lru_cache(maxsize=1, typed=True)
def get_key(_: Any, info: ValidationInfo) -> str:  # noqa: ANN401
    """Extract object key from inventory row.

    Parameters
    ----------
    info : ValidationInfo
        Validation info containing inventory row raw data.

    Returns
    -------
    str
        Object S3 key.
    """
    return info.data["key"]


def get_key_parts(key: str) -> List[str]:
    """Generate key parts.

    Parameters
    ----------
    key : str
        Object key on S3.

    Returns
    -------
    List[str]
        A list of key parts.
    """
    return key.split("/")


def get_is_dir(key: str) -> bool:
    """Check if the key is for a directory.

    Parameters
    ----------
    key : str
        Object key on S3.

    Returns
    -------
    bool
        True if key is a dir else False.
    """
    return key.endswith("/")


def get_proj_id(key: str) -> str:
    """Extract project ID from the key.

    Parameters
    ----------
    key : str
        Object key on S3.

    Returns
    -------
    str
        Project ID.
    """
    return get_key_parts(key)[0]


def get_source_id(key: str) -> str:
    """Extract source ID from the key.

    Parameters
    ----------
    key : str
        Object key on S3.

    Returns
    -------
    str
        Source ID.
    """
    return get_key_parts(key)[0]


def get_root_dir(key: str) -> str:
    """Extract root folder from the key.

    Parameters
    ----------
    key : str
        Object key on S3.

    Returns
    -------
    str
        Workspace folder.
    """
    return get_key_parts(key)[0]


def get_workspace_dir(key: str) -> str:
    """Extract workspace folder from the key.

    Parameters
    ----------
    key : str
        Object key on S3.

    Returns
    -------
    str
        Workspace folder.
    """
    return get_key_parts(key)[0]
    # elif get_root_dir(key) == "workspace":
    #     return get_key_parts(key)[3]
    # elif get_root_dir(key) == "workspace_dl":
    #     return get_key_parts(key)[3]


def get_file_type(key: str) -> bool:
    """Check if the key is for a directory.

    Parameters
    ----------
    key : str
        Object key on S3.

    Returns
    -------
    bool
        True if key is a dir else False.
    """
    if get_key_parts(key)[-1][-1] == "/":
        return True
    else:
        return False
