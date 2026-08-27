"""Dataset model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Dataset:
    name: str
    source_key: str
    file_name: str
    extension: str
