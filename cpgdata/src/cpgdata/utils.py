"""Utilities.

This module provide utility functions shared by other modules in the package.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Any, Callable, List, Optional

from joblib import Parallel, cpu_count, delayed


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
) -> List[Any]:
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
    List[Any]
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
