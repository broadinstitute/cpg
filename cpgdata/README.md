# Cell painting gallery data handling and validation

## Getting started


### Install `cpgdata` package

```bash
pip install cpgdata
```

### Sync pre-generated index files

```bash
cpg index sync -o "path to save index files"
```

### Example of using the index for filtering files to download from the Cell painting gallery

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
