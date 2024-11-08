# Architecture

## Complex

## CPG Data

`cpgdata` provides data validation for the Cell Painting Gallery. It parses
`inventory` files using a pydantic class. Then it generates a lot of
`measurements` and saves all the measurement to parquet files. Finally, `rules`
are applied on the generated `measurements` for validation.

All processing happens as a `stream` and in `batches`. These streams are
processed in parallel.

```mermaid
graphTD:
    Generate/Sync Inventory --> Create Measurements
    Create Measurements --> Apply Rules
    Apply Rules --> Generate Reports
```

### Inventory

We are using AWS inventory as our source data. It is a partitioned parquet
dataset (assuming AWS inventory is configured to generate output as parquet
files). For now, we do not support validating local files. But we can easily
support this is the future. This will require us to write a module to generate
the inventory file by doing a glob on the local filesystem tree.

### Measurements

It is an abstraction for `values` parsed and extracted from the `inventory` for
each file. A value can be any information related to the file required for
testing a `rule`.

It is implemented as `Validators` from the `pydantic` library. The measurement
functions are pure functions called by `Validator` for each file and can receive
inventory column values as inputs. All the measurement function are assembled in
a single pydantic class.

All the measurements are generated during the parsing step automatically by
pydantic. Also, measurements do not normalize `values`. All values are
faithfully captured and passed on to the `Rules` for validation.

### Rules

Validation rules are implemented as individual python class that encapsulates
everything that is needed to apply that rule.
