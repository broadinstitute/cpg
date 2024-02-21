"""Rules to enforce the cpg schema.

This module provide `rules` that can be chained together in a `pipe`
to enforce arbitrary schema.
"""
from abc import ABC, abstractmethod
from pathlib import Path

import polars as pl


class BaseRule(ABC):
    """Base class for defining rules."""

    def __init__(self: "BaseRule", out_path: Path) -> None:
        """Initialize Rule.

        Parameters
        ----------
        out_path : Path
            Path to write rule output.
        """
        self.out_path = out_path

    @abstractmethod
    def validate(self: "BaseRule", df: pl.LazyFrame) -> bool:
        """Run validation.

        Parameters
        ----------
        df : pl.LazyFrame
            Mesaurement lazyframe.

        Returns
        -------
        bool
            Flag indicating check passed or not.
        """
        pass


class CheckProjectDirs(BaseRule):
    """Check if all defined dirs are present for a project."""

    def validate(self: "CheckProjectDirs", df: pl.LazyFrame) -> bool:
        """Run validation.

        Parameters
        ----------
        df : pl.LazyFrame
            Mesaurement lazyframe.

        Returns
        -------
        bool
            Flag indicating check passed or not.
        """
        return True


class CheckJUMPProjectStructure(BaseRule):
    """Check if the JUMP projects meets the required directory structure."""

    def validate(self: "BaseRule", df: pl.LazyFrame) -> bool:
        """Run validation.

        Parameters
        ----------
        df : pl.LazyFrame
            Mesaurement lazyframe.

        Returns
        -------
        bool
            Flag indicating check passed or not.
        """
        # Setup out path for the check output
        out_path = self.out_path.joinpath("check_jump_project_structure.parquet")

        # filter and group jump project entries
        jump_projects = df.filter(pl.col("dataset_id").str.contains("jump+"))
        project_groups = jump_projects.group_by("dataset_id")

        project_workspace_dirs = project_groups.agg(pl.col("workspace_dir").unique())

        # Write out the final dataframe.
        final_df = project_workspace_dirs.collect()
        final_df.write_parquet(str(out_path.absolute()))
        final_dict = final_df.to_dict()
        for folders in final_dict["workspace_dir"]:
            print(list(folders))

        return False


class CheckWorkspaceDirs(BaseRule):
    """Check if all defined dirs are present in a workspace for all projects."""

    def validate(self: "CheckWorkspaceDirs", df: pl.LazyFrame) -> bool:
        """Run validation.

        Parameters
        ----------
        df : pl.LazyFrame
            Mesaurement lazyframe.

        Returns
        -------
        bool
            Flag indicating check passed or not.
        """
        project_groups = df.groupby("dataset_id")
        project_workspace_dirs = project_groups.agg(
            pl.col("workspace_dir").unique()
        ).collect()
        print(project_workspace_dirs.head())
        project_wdirs_unique = project_workspace_dirs.with_columns(
            (pl.col("workspace_dir").list.set_difference(["imagess"])).alias(
                "check_wdirs"
            )
        )
        print(project_wdirs_unique)
        # final_df = project_wdirs_unique.select(pl.col("check_wdirs").ne())
        return True
        # for row in project_workspace_dirs.iter_rows
