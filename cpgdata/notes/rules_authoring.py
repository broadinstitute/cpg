import marimo

__generated_with = "0.1.79"
app = marimo.App()


@app.cell(hide_code=True)
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("# Demonstration of Rule Authoring")
    return


@app.cell
def __():
    from pprint import pprint

    import polars as pl
    from cpgdata.rule import BaseRule
    from cpgdata.utils import get_package_root_path
    return BaseRule, get_package_root_path, pl, pprint


@app.cell(disabled=True)
def __(get_package_root_path, pl):
    measurements_dir = (
        get_package_root_path().parents[1].joinpath("scratch/validation/measurements")
    )

    files = [file for file in measurements_dir.glob("*.parquet")]
    df = pl.scan_parquet(files)
    return df, files, measurements_dir


@app.cell
def __(mo):
    mo.md("## Check files do not have zero size")
    return


@app.cell
def __(BaseRule, pl, pprint):
    class CheckSizeNotZero(BaseRule):
        def validate(self, df: pl.LazyFrame) -> bool:
            df = df.filter(
                pl.col("is_dir").ne(True) & pl.col("size").eq(0)
            ).collect()
            pprint(df.to_dicts())
            if len(df) != 0:
                return False
            else:
                return True
    return CheckSizeNotZero,


@app.cell(disabled=True)
def __(CheckSizeNotZero, df, measurements_dir):
    CheckSizeNotZero(measurements_dir.parent.joinpath("checks")).validate(df)
    return


@app.cell
def __(mo):
    mo.md("## Check prefixes do not have parsing errors")
    return


@app.cell
def __(BaseRule, pl, pprint):
    class CheckParsingErrors(BaseRule):
        def validate(self, df: pl.LazyFrame) -> bool:
            df = df.filter(pl.col("is_parsing_error").eq(True)).collect()
            pprint(df.to_dicts())
            if len(df) != 0:
                return False
            else:
                return True
    return CheckParsingErrors,


@app.cell
def __(CheckParsingErrors, df, measurements_dir):
    CheckParsingErrors(measurements_dir.parent.joinpath("checks")).validate(df)
    return


@app.cell
def __(mo):
    mo.md("## Check Illum exist for images")
    return


@app.cell
def __(BaseRule, pl, pprint):
    class CheckIllumExist(BaseRule):
        def validate(self, df: pl.LazyFrame) -> bool:
            df = (
                df.filter(pl.col("dataset_id").str.contains("jump+"))
                .filter(
                    pl.col("images_images_root_dir").ne(None)
                    | pl.col("images_illum_root_dir").ne(None)
                )
                .group_by(pl.col("batch_id"))
                .select(pl.col("obj_key"))
                .collect()
            )
            print(len(df))
            pprint(df)
            # pprint(df[0:10].to_dicts()
            if len(df) != 0:
                return False
            else:
                return True
    return CheckIllumExist,


@app.cell(disabled=True)
def __():
    # CheckIllumExist(measurements_dir.parent.joinpath("checks")).validate(df)
    return


@app.cell
def __(mo):
    mo.md("## Check total size")
    return


@app.cell
def __(BaseRule, pl, pprint):
    class CheckTotalSize(BaseRule):
        def validate(self, df: pl.LazyFrame) -> bool:
            df = (
                df
                .filter(pl.col("dataset_id").eq("cpg0016-jump"))
                .filter(pl.col("source_id").eq("source_4"))
                .filter(pl.col("leaf_node").str.contains("Cells.csv"))
                .select(pl.col("key"))
                .collect()
            )
            pprint(df.to_dicts()[0:10])
            if len(df) != 0:
                return False
            else:
                return True
    return CheckTotalSize,


@app.cell(disabled=True)
def __(CheckTotalSize, df, measurements_dir):
    CheckTotalSize(measurements_dir.parent.joinpath("checks")).validate(df)
    return


@app.cell
def __():
    TERABYTE = (1024 * 1024 * 1024 * 1024)
    return TERABYTE,


@app.cell
def __(TERABYTE):
    394098534521368 / TERABYTE
    return


@app.cell
def __(TERABYTE):
    10060947803770 / TERABYTE
    return


@app.cell
def __(TERABYTE):
    63411583844158 / TERABYTE
    return


@app.cell
def __(TERABYTE):
    203778562031140 / TERABYTE
    return


@app.cell
def __(TERABYTE):
    267353842679904 / TERABYTE
    return


@app.cell
def __(TERABYTE):
    69438883941015 / TERABYTE
    return


@app.cell
def __(TERABYTE):
    126799901977471 / TERABYTE
    return


@app.cell
def __():
    #Total size: 358.43 TB
    #Images: 115.32 TB
    #Workspace: 185.33 TB
    #Workspace_dl: 57.67 TB"
    return


@app.cell(disabled=True)
def __(get_package_root_path, pl, pprint):
    raw_dir = (
        get_package_root_path().parents[1].joinpath("data/data")
    )

    raw_files = [file for file in raw_dir.glob("*.parquet")]
    raw_df = pl.scan_parquet(raw_files)
    # raw_df = raw_df
    raw_df = raw_df.filter(pl.col("key").str.contains("cpg0016-jump+") & pl.col("key").str.contains("images/+")).select(pl.col("size")).collect()
    pprint(raw_df)
    return raw_df, raw_dir, raw_files


@app.cell
def __(pl, raw_df):
    raw_df.select(pl.col("size").sum())
    return


@app.cell
def __(raw_files):
    print(len(raw_files))
    return


@app.cell
def __():
    "cpg0016-jump/source_10/workspace_dl/embeddings/efficientnet_v2_imagenet21k_s_feature_vector_2_0260bc96/2021_05_31_U2OS_48_hr_run1/Dest210531-152149/A01-01/embedding.parquet"
    return


@app.cell
def __(mo):
    mo.md("# Missing files in measurement tables")
    return


@app.cell
def __():
    import pyarrow as pa
    from s3fs import S3FileSystem
    return S3FileSystem, pa


@app.cell
def __():
    file_path = "s3://cellpainting-gallery/cpg0016-jump/source_10/workspace_dl/embeddings/efficientnet_v2_imagenet21k_s_feature_vector_2_0260bc96/2021_05_31_U2OS_48_hr_run1/Dest210531-152149/A01-01/embedding.parquet"
    return file_path,


app._unparsable_cell(
    r"""
    import pyarrow as pa
    from s3fs import S3FileSystem
    pl.read_parquet(file_path, pyarrow_options={\"filesystem\" :pa.filesystem.S3FSWrapper(S3FileSystem(anonymous=True)))}
    """,
    name="__"
)


if __name__ == "__main__":
    app.run()
