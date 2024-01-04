"""Validation pipeline modules.

This module collects data I/O and transformers into a
sequentially parallel pipeline.
"""
import math
import os
from pathlib import Path
from typing import List

import polars as pl
import pyarrow as pa
from lark import ParseError
from pyarrow import parquet as pq
from pyarrow.parquet import FileMetaData
from pydantic import TypeAdapter, ValidationError
from tqdm import tqdm

from cpgdata.parser import InventoryRowParser, S3ObjectParser, key_parser
from cpgdata.rule import BaseRule, CheckWorkspaceDirs
from cpgdata.utils import parallel


def gen_pq_schema_from_df(df: pl.LazyFrame) -> pa.Schema:
    inventory_row_adapter = TypeAdapter(InventoryRowParser)
    s3_object_adapter = TypeAdapter(S3ObjectParser)
    parsed_batch = {
        key: []
        for key in S3ObjectParser.model_json_schema(by_alias=False)["properties"].keys()
    }
    row = df.first().collect().to_dicts()[0]
    inventory_row = inventory_row_adapter.validate_python(row)
    try:
        s3_object = s3_object_adapter.validate_python(
            inventory_row, from_attributes=True
        )
    except ValidationError as e:
        s3_object = S3ObjectParser.gen_error_entry(inventory_row.key, e)
    except Exception as e:
        print(inventory_row)
        print(e)
        raise (e)
    for key, value in s3_object.model_dump().items():
        parsed_batch[key].append(value)
    table = pa.Table.from_pydict(parsed_batch)
    return table.schema


def gen_lazy_slice(lazy_df: pl.LazyFrame, metadata: FileMetaData):
    row_groups = metadata.num_row_groups
    num_rows = [metadata.row_group(i).num_rows for i in range(row_groups)]
    offsets = [sum(num_rows[0:i]) for i in range(row_groups)]
    for row in range(row_groups):
        yield lazy_df.slice(offsets[row], metadata.row_group(row).num_rows)


def noop(_) -> bool:
    return True


def parse_batch(batch: pl.DataFrame) -> dict:
    inventory_row_adapter = TypeAdapter(InventoryRowParser)
    s3_object_adapter = TypeAdapter(S3ObjectParser)
    row_dicts = batch.to_dicts()
    parsed_batch = {
        key: []
        for key in S3ObjectParser.model_json_schema(by_alias=False)["properties"].keys()
    }
    for row in row_dicts:
        inventory_row = inventory_row_adapter.validate_python(row)
        try:
            ast = key_parser.parse(inventory_row.key, on_error=noop)
            s3_object = s3_object_adapter.validate_python(
                inventory_row, from_attributes=True
            )
        except ParseError as e:
            s3_object = S3ObjectParser.gen_error_entry(inventory_row.key, e)
        except ValidationError as e:
            s3_object = S3ObjectParser.gen_error_entry(inventory_row.key, e)
        except Exception as e:
            print(inventory_row)
            print(e)
            raise (e)
        for key, value in s3_object.model_dump().items():
            parsed_batch[key].append(value)
    return parsed_batch


def gen_measurement(
    file_path_list: List[Path], out_path: Path, job_idx: int = 0
) -> None:
    w_id = os.getpid()
    for i, file in tqdm(
        enumerate(file_path_list),
        desc=f"Worker {w_id} is processing file: ",
        position=job_idx,
    ):
        file_meta = pq.read_metadata(file)
        # Streaming the parquet file instead of reading the whole file
        df = pl.scan_parquet(file)
        # Creating parquet schema for streaming write
        pq_schema = gen_pq_schema_from_df(df)
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
                    pq_writer.write_table(pa.Table.from_pydict(parsed_batch))


def apply_rules(
    rule_list: List[BaseRule], measurements_dir: Path, job_idx: int
) -> None:
    files = [file for file in measurements_dir.glob("*.parquet")]
    df = pl.scan_parquet(files)
    w_id = os.getpid()
    for _, rule in (pbar := tqdm(enumerate(rule_list), position=job_idx)):
        pbar.set_description(f"Worker {w_id} applying rule: {rule}")
        rule.validate(df)


def run(in_path: Path, out_path: Path) -> None:
    files = [file for file in in_path.glob("*.parquet")]
    # Create Measurements
    if len(files) != 0:
        parallel(files, gen_measurement, [out_path])
    rules = [CheckWorkspaceDirs()]
    # Apply rules
    if len(rules) != 0:
        parallel(rules, apply_rules, [out_path])
