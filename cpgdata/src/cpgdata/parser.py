"""Parsers for data validation.

This module provide parsers that automatically
generate measurements for the parsed inputs.

The parsed inputs can later be passed to the
`Rules` classes to enforce `cpg` schema.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from lark import Lark
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
)
from typing_extensions import Annotated

from cpgdata.measurement import (
    get_is_dir,
    get_key_parts,
    get_proj_id,
    get_root_dir,
    get_source_id,
    get_workspace_dir,
)

key_parser = Lark.open("key_parser.lark", rel_to=__file__, parser="lalr")


def enum_to_str(v: Enum) -> str:
    """Convert enum to its str value.

    Parameters
    ----------
    v : Enum
        Enum value to convert.

    Returns
    -------
    str
        String value of the enum.
    """
    return v.value


class S3Folder(Enum):
    """Enum for root folder names."""

    IMAGE = "images"
    WORKSPACE = "workspace"
    WORKSPACE_DL = "workspace_dl"
    NA = "na"


class ImageFolder(Enum):
    """Enum for image folder names."""

    ILLUM = "illum"
    IMAGE = "images"


class MetadataFolder(Enum):
    """Enum for metadata folder names."""

    EXTERNAL = "external_metadata"
    PLATEMAPS = "platemaps"


class WorkspaceFolder(Enum):
    """Enum for workspace folder names."""

    ANALYSIS = "analysis"
    BACKEND = "backend"
    LOAD_DATA = "load_data_csv"
    METADATA = "metadata"
    PROFILES = "profiles"
    QUALITY_CONTROL = "quality_control"
    QC = "qc"
    ASSAY_DEV = "assaydev"
    NA = "na"


class File(BaseModel):
    """Parser for a file object."""

    file_id: str
    is_dir: Annotated[bool, AfterValidator(get_is_dir)]


class Directory(BaseModel):
    """Parser for a directory object."""

    dir_id: str
    child_dir_ids: List[str]
    child_file_ids: List[str]


class InventoryRowParser(BaseModel):
    """Parser for S3 Inventory row."""

    bucket: str
    key: str
    size: int
    last_modified_date: datetime
    e_tag: str
    storage_class: str
    is_multipart_uploaded: bool
    replication_status: Optional[str]
    encryption_status: str
    object_lock_retain_until_date: Optional[datetime]
    object_lock_mode: Optional[str]
    object_lock_legal_hold_status: Optional[str]
    intelligent_tiering_access_tier: Optional[str]
    bucket_key_status: str
    checksum_algorithm: Optional[str]
    object_access_control_list: str
    object_owner: str


class S3ObjectParser(BaseModel):
    """Parser for S3 object."""

    obj_key: Annotated[str, Field(validation_alias="key")]
    is_parsing_error: bool = Field(default=False)
    errors: str = Field(default="")
    is_dir: Annotated[bool, BeforeValidator(get_is_dir)] = Field(
        validation_alias="key", default=False
    )
    key_parts: Annotated[
        List[str],
        BeforeValidator(get_key_parts),
    ] = Field(validation_alias="key", default=[])
    project_id: Annotated[str, BeforeValidator(get_proj_id)] = Field(
        validation_alias="key", default=""
    )
    source_id: Annotated[str, BeforeValidator(get_source_id)] = Field(
        validation_alias="key", default=""
    )
    root_dir: Annotated[
        S3Folder,
        BeforeValidator(get_root_dir),
        AfterValidator(enum_to_str),
    ] = Field(validation_alias="key", default="")
    workspace_dir: Annotated[
        WorkspaceFolder,
        BeforeValidator(get_workspace_dir),
        AfterValidator(enum_to_str),
    ] = Field(validation_alias="key", default="")
    batch_id: Annotated[
        str,
        BeforeValidator(get_workspace_dir),
    ] = Field(validation_alias="key", default="")
    plate_id: Annotated[
        str,
        BeforeValidator(get_workspace_dir),
    ] = Field(validation_alias="key", default="")
    well_id: Annotated[
        str,
        BeforeValidator(get_workspace_dir),
    ] = Field(validation_alias="key", default="")
    site_id: Annotated[
        str,
        BeforeValidator(get_workspace_dir),
    ] = Field(validation_alias="key", default="")
    container: Annotated[
        str,
        BeforeValidator(get_workspace_dir),
    ] = Field(validation_alias="key", default="")

    # Model configuration
    model_config = ConfigDict(populate_by_name=True)

    @staticmethod
    def gen_error_entry(obj_key: str, e: ValidationError) -> "S3ObjectParser":
        """Generate an error entry for the parsed object.

        Parameters
        ----------
        obj_key : str
            Object key.
        e : ValidationError
            Pydantic validation error.

        Returns
        -------
        "S3ObjectParser"
           Validation error as a parsed object.
        """
        return S3ObjectParser(
            obj_key=obj_key,
            is_parsing_error=True,
            errors=str(e),
        )


# file_type: Annotated[Optional[WorkspaceFolder], AfterValidator(get_file_type)]
