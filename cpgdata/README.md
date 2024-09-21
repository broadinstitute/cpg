# CPG Data Validation

[![PyPI version](https://badge.fury.io/py/cpgdata.svg)](https://badge.fury.io/py/cpgdata)

CPG Data Validation is a Python package designed to validate and analyze data from the Cell Painting Gallery (CPG). It provides tools for parsing, measuring, and checking the structure and contents of CPG datasets stored in S3 buckets.

## Features

- Sync inventory and index files from AWS S3
- Parse and validate S3 inventory data
- Generate measurements from inventory data
- Apply custom validation rules to ensure data integrity
- Parallel processing for improved performance
- CLI interface for easy execution of validation tasks
- Generate reports based on validation results

## Prerequisites

- Python 3.10 or higher
- AWS CLI (for S3 interactions)
- AWS credentials (if accessing non-public S3 buckets)

## Installation

You can install CPG Data Validation using either pip or Poetry.

### Using pip

```bash
pip install cpgdata
```

### Using Poetry

1. Ensure you have Poetry installed. If not, install it by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

2. Install the package:

   ```bash
   poetry add cpgdata
   ```

For development:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cpgdata.git
   cd cpgdata
   ```

2. Install the project and its dependencies:

   ```bash
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

## Usage

### Example Workflow

1. Sync inventory files from S3
2. Generate measurements from inventory data
3. Apply validation rules
4. Generate reports

### CLI Commands

#### Sync Inventory Files

```bash
cpg inventory sync -o /path/to/local/inventory
```

#### Generate Measurements

```bash
cpg inventory measure -i /path/to/local/inventory -o /path/to/output/measurements -j 4
```

#### Apply Validation Rules

```bash
cpg inventory check -i /path/to/output/measurements -o /path/to/output/checks -j 4
```

#### Generate Reports

```bash
cpg report gen -i /path/to/output/checks -o /path/to/output/reports
```

For more detailed information on CLI commands and options, please refer to the full documentation.

### Python API Example

Here's an example of how to use the package's Python API to filter and download specific files from the Cell Painting Gallery. This example demonstrates how to:

1. Load index files
2. Filter the index based on specific criteria
3. Extract the keys of the filtered files
4. Use parallel processing to download the selected files from S3

```python
from pathlib import Path
from pprint import pprint

import polars as pl
from cpgdata.utils import download_s3_files, parallel

index_dir = Path("path to dir containing index files")
index_files = [file for file in index_dir.glob("*.parquet")]
df = pl.scan_parquet(index_files)

df = (
    df
    .filter(pl.col("dataset_id").eq("cpg0016-jump"))
    .filter(pl.col("source_id").eq("source_4"))
    .filter(pl.col("leaf_node").str.contains("Cells.csv"))
    .select(pl.col("key"))
    .collect()
)

# print first 10 results
pprint(df.to_dicts()[0:10])

# Download filtered files
download_keys = list(df.to_dict()["key"])
parallel(download_keys, download_s3_files, ["cellpainting-gallery", Path("path to save downloaded files")], jobs=20)
```

## Key Components

1. **Parsers**: The `parser.py` module defines models for parsing S3 inventory data and generating measurements.
2. **Rules**: The `rule.py` module contains rule classes that can be applied to the parsed data to validate its structure and contents.
3. **Pipeline**: The `pipe.py` module orchestrates the validation process, including parsing, measurement generation, and rule application.
4. **CLI**: The `cli/` directory contains modules for the command-line interface, allowing easy execution of validation tasks.

## Customization

You can extend the validation capabilities by adding new rule classes in `rule.py`. Implement the `BaseRule` abstract class and add your custom validation logic in the `validate` method.

## Development

To set up a development environment:

1. Clone the repository
2. Install the project in development mode:

   ```bash
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

Run tests using pytest:

```bash
poetry run pytest tests/
```

## License

This project is licensed under the BSD-3-Clause License.
