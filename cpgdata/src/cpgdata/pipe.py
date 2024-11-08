"""Validation pipeline modules.

This module collects data I/O and transformers into a
sequentially parallel pipeline.
"""

import math
import os
from pathlib import Path
from typing import Any, Generator, List, Optional, Type, Union

import cpgparser
import polars as pl
import pyarrow as pa
from lark import ParseError
from pyarrow import parquet as pq
from pyarrow.parquet import FileMetaData
from pydantic import TypeAdapter, ValidationError
from pydantic.fields import ComputedFieldInfo, FieldInfo
from tqdm import tqdm

from cpgdata.parser import MeasuredPrefix, py_to_pa
from cpgdata.rule import BaseRule, CheckJUMPProjectStructure, CheckWorkspaceDirs
from cpgdata.utils import parallel


def get_field_type(model_field: Union[FieldInfo, ComputedFieldInfo]) -> Any:  # noqa
    """Get type of the model field.

    Parameters
    ----------
    model_field : Union[FieldInfo, ComputedFieldInfo]
        Combined model fields dict.

    Returns
    -------
    Any
        Type of the model field.
    """
    return (
        model_field.annotation
        if isinstance(model_field, FieldInfo)
        else model_field.return_type
    )


def gen_pq_schema(pydantic_model: Type[MeasuredPrefix]) -> pa.Schema:
    """Generate parquet schema from pydantic type.

    Parameters
    ----------
    pydantic_model : Type[MeasuredPrefix]
        Pydantic model type.

    Returns
    -------
    pa.Schema
        Parquet schema.
    """
    constructed_model = pydantic_model.model_construct()
    model_fields = constructed_model.get_all_fields()
    schema = [
        pa.field(key, py_to_pa[get_field_type(val)])  # noqa
        for key, val in model_fields.items()
    ]
    return pa.schema(schema)


def gen_lazy_slice(lazy_df: pl.LazyFrame, metadata: FileMetaData) -> Generator:
    """Split dataframe using row groups as boundaries.

    Parameters
    ----------
    lazy_df : pl.LazyFrame
        Polars lazy dataframe.
    metadata : FileMetaData
        Parquet metadata for row group information.
    """
    row_groups = metadata.num_row_groups
    num_rows = [metadata.row_group(i).num_rows for i in range(row_groups)]
    offsets = [sum(num_rows[0:i]) for i in range(row_groups)]
    for row in range(row_groups):
        yield lazy_df.slice(offsets[row], metadata.row_group(row).num_rows)


def parse_batch(batch: pl.DataFrame) -> dict:
    """Generate measurements for a batch.

    Parameters
    ----------
    batch : pl.DataFrame
        Polars dataframe for the batch.

    Returns
    -------
    dict
        Generated column major dict of MeasuredPrefix objects.
    """
    measured_prefix_adapter = TypeAdapter(MeasuredPrefix)
    row_dicts = batch.to_dicts()
    parsed_batch = {
        key: [] for key in MeasuredPrefix.model_construct().get_all_fields().keys()
    }
    for row in row_dicts:
        try:
            parsed_prefix_dict = cpgparser.parse_prefix(row["key"])  # type: ignore
            measured_prefix = measured_prefix_adapter.validate_python(
                {**row, **parsed_prefix_dict}
            )
        except ParseError as e:
            measured_prefix = MeasuredPrefix.gen_error_entry(row["key"], e)
        except ValidationError as e:
            measured_prefix = MeasuredPrefix.gen_error_entry(row["key"], e)
        except ValueError as e:
            measured_prefix = MeasuredPrefix.gen_error_entry(row["key"], e)
        except Exception as e:
            raise (e)
        for key, value in measured_prefix.model_dump().items():
            parsed_batch[key].append(value)
    return parsed_batch


def gen_measurement(
    file_path_list: List[Path], out_path: Path, job_idx: int = 0
) -> None:
    """Generate measurement parquet files.

    Parameters
    ----------
    file_path_list : List[Path]
        List of file paths to read raw inventory parquet files.
    out_path : Path
        Path to output dir for writing generated measurement files.
    job_idx : int
        Job index for tqdm progress bar ordering.
    """
    w_id = os.getpid()
    for i, file in tqdm(
        enumerate(file_path_list),
        desc=f"Measurement Worker {w_id} is processing file: ",
        position=job_idx,
    ):
        file_meta = pq.read_metadata(file)
        # Streaming the parquet file instead of reading the whole file
        df = pl.scan_parquet(file)
        # Creating parquet schema for streaming write
        pq_schema = gen_pq_schema(MeasuredPrefix)
        with pq.ParquetWriter(out_path.joinpath(file.name), pq_schema) as pq_writer:
            for j, frame in enumerate(gen_lazy_slice(df, file_meta)):
                # loading one frame into memory ~ 500MB(AWS row grouping is sub optimal)
                frame = frame.collect()
                rows, _ = frame.shape
                # Iterating over slices vs iterating row wise
                # Look warning here: https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/api/polars.DataFrame.iter_rows.html#polars.DataFrame.iter_rows
                for batch in tqdm(
                    frame.iter_slices(),
                    desc=f"Worker {w_id} | ({i+1}/{len(file_path_list)}) | ({j+1}/{file_meta.num_row_groups}): {file.name}",  # noqa: E501
                    position=job_idx,
                    total=math.ceil(rows / 10000),
                ):
                    parsed_batch = parse_batch(batch)
                    pq_writer.write_table(
                        pa.Table.from_pydict(parsed_batch, schema=pq_schema)
                    )


def apply_rules(
    rule_list: List[BaseRule], measurements_dir: Path, job_idx: int
) -> None:
    """Apply rules on the measurement parquet files.

    Parameters
    ----------
    rule_list : List[BaseRule]
        A list of `Rule` to apply.
    measurements_dir : Path
        Path to dir containing measurement files.
    job_idx : int
        Job index for tqdm progress bar ordering.
    """
    files = [file for file in measurements_dir.glob("*.parquet")]
    df = pl.scan_parquet(files)
    w_id = os.getpid()
    for _, rule in (pbar := tqdm(enumerate(rule_list), position=job_idx)):
        pbar.set_description(f"Worker {w_id} applying rule: {rule}")
        rule.validate(df)


def measure(in_path: Path, out_path: Path, jobs: Optional[int] = None) -> None:
    """Measure inventory.

    Parameters
    ----------
    in_path : Path
        Path to raw inventory parquet files.
    out_path : Path
        Path to save generated parquet files.
    jobs : Optional[int]
        Number of jobs to launch.
    """
    files = [file for file in in_path.glob("*.parquet")]
    measurement_out_path = out_path.joinpath("measurements")
    measurement_out_path.mkdir(parents=True, exist_ok=True)
    if len(files) != 0:
        parallel(files, gen_measurement, [measurement_out_path], jobs=jobs)


def check(in_path: Path, out_path: Path, jobs: Optional[int] = None) -> None:
    """Check inventory.

    Parameters
    ----------
    in_path : Path
        Path to raw inventory parquet files.
    out_path : Path
        Path to save generated parquet files.
    jobs : Optional[int]
        Number of jobs to launch.
    """
    measurement_out_path = out_path.joinpath("measurements")
    check_out_path = out_path.joinpath("checks")
    check_out_path.mkdir(parents=True, exist_ok=True)
    rules = [
        # CheckWorkspaceDirs(check_out_path),
        CheckJUMPProjectStructure(check_out_path),
    ]
    if len(rules) != 0:
        parallel(rules, apply_rules, [measurement_out_path], jobs=jobs)


def validate(in_path: Path, out_path: Path, jobs: Optional[int] = None) -> None:
    """Valiadate inventory.

    Parameters
    ----------
    in_path : Path
        Path to raw inventory parquet files.
    out_path : Path
        Path to save generated parquet files.
    jobs : Optional[int]
        Number of jobs to launch.
    """
    # Create Measurements
    measure(in_path, out_path, jobs)
    # Apply rules
    # check(in_path, out_path, jobs)
