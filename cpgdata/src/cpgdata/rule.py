"""Rules to enforce the cpg schema.

This module provide `rules` that can be chained together in a `pipe`
to enforce arbitrary schema.
"""
from abc import ABC, abstractmethod

import polars as pl


class BaseRule(ABC):
    """Base class for defining rules."""

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
        project_groups = df.groupby("project_id")
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
