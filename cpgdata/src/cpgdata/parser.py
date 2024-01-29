"""Parsers for data validation.

This module provide parsers that automatically
generate measurements for the parsed inputs.

The parsed inputs can later be passed to the
`Rules` classes to enforce `cpg` schema.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

import pyarrow as pa
from lark import Lark
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    computed_field,
)
from typing_extensions import Annotated

from cpgdata.measurement import (
    get_is_dir,
    get_key_parts,
)

# A python implementation of the prefix parser
# This can be useful in checking the specification with two different parsers
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
    PIPELINES = "pipelines"
    SOFTWARE = "software"
    NONE = "None"


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
    obj_key: Annotated[str, Field(validation_alias="key")]
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


class ParsedPrefix(BaseModel):
    """Container for storing results from the parser."""

    key: Optional[str] = None
    root_dir: Optional[str] = None
    images_root_dir: Optional[str] = None
    images_batch_root_dir: Optional[str] = None
    images_illum_root_dir: Optional[str] = None
    images_images_root_dir: Optional[str] = None
    images_images_aligned_root_dir: Optional[str] = None
    images_images_corrected_root_dir: Optional[str] = None
    images_images_corrected_cropped_root_dir: Optional[str] = None
    workspace_root_dir: Optional[str] = None
    analysis_root_dir: Optional[str] = None
    backend_root_dir: Optional[str] = None
    load_data_csv_root_dir: Optional[str] = None
    metadata_root_dir: Optional[str] = None
    profiles_root_dir: Optional[str] = None
    assaydev_root_dir: Optional[str] = None
    embeddings_root_dir: Optional[str] = None
    pipelines_root_dir: Optional[str] = None
    qc_root_dir: Optional[str] = None
    segmentation_root_dir: Optional[str] = None
    software_root_dir: Optional[str] = None
    workspace_dl_root_dir: Optional[str] = None
    collated_root_dir: Optional[str] = None
    consensus_root_dir: Optional[str] = None
    dl_embeddings_root_dir: Optional[str] = None
    dl_profiles_root_dir: Optional[str] = None
    sep: Optional[str] = None
    images: Optional[str] = None
    workspace: Optional[str] = None
    workspace_dl: Optional[str] = None
    dataset_id: Optional[str] = None
    source_id: Optional[str] = None
    batch_id: Optional[str] = None
    plate_id: Optional[str] = None
    well_id: Optional[str] = None
    site_id: Optional[str] = None
    well_site_id: Optional[str] = None
    plate_well_site_id: Optional[str] = None
    # Required a validation_alias because model_ is a protected namespace for pydantic
    ml_model_id: Optional[str] = Field(validation_alias="model_id", default=None)
    leaf_node: Optional[str] = None
    filename: Optional[str] = None
    extension: Optional[str] = None
    software_hash: Optional[str] = None
    software: Optional[str] = None
    hash: Optional[str] = None
    allowed_names: Optional[str] = None


class MeasuredPrefix(InventoryRowParser, ParsedPrefix):
    """Generate measurement for a prefix."""

    is_parsing_error: bool = Field(default=False)
    errors: Optional[str] = Field(default=None)
    is_dir: Annotated[bool, BeforeValidator(get_is_dir)] = Field(
        validation_alias="key", default=False
    )
    key_parts: Annotated[
        List[str],
        BeforeValidator(get_key_parts),
    ] = Field(validation_alias="key", default=[])

    # Model configuration
    model_config = ConfigDict(populate_by_name=True)

    @computed_field(return_type=Optional[str])
    @property
    def workspace_dir(self: "MeasuredPrefix") -> Optional[str]:
        """Computed workspace directory value.

        Returns
        -------
        Optional[str]
            Computed workspace directory value.
        """
        workspace_dir = self.workspace_root_dir
        workspace_dir = str(workspace_dir).split("/")[0]
        return WorkspaceFolder(workspace_dir).value

    def get_all_fields(self: "MeasuredPrefix") -> dict:
        """Get all the fields of the model.

        Returns
        -------
        dict
            A dict with field key and FieldInfo or ComputedFieldInfo.
        """
        model_fields = self.model_fields
        return {**model_fields, **self.model_computed_fields}

    @staticmethod
    def gen_error_entry(obj_key: str, e: Exception) -> "MeasuredPrefix":
        """Generate an error entry for the parsed object.

        Parameters
        ----------
        obj_key : str
            Object key.
        e : Exception
            Pydantic validation error.

        Returns
        -------
        "MeasuredPrefix"
           Validation error as a parsed object.
        """
        print(f"I am called with the error {e}")
        return MeasuredPrefix.model_construct(
            obj_key=obj_key,
            is_parsing_error=True,
            errors=str(e),
        )


py_to_pa = {
    int: pa.int64(),
    str: pa.string(),
    datetime: pa.timestamp(unit="ms", tz="UTC"),
    Optional[datetime]: pa.timestamp(unit="ms", tz="UTC"),
    List[str]: pa.list_(pa.string()),
    bool: pa.bool_(),
    Optional[WorkspaceFolder]: pa.string(),
    Optional[str]: pa.string(),
    Optional[int]: pa.int64(),
}
