"""Processed source-file metadata."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProcessedFile:
    dataset: str
    file_name: str
    source_key: str
    checksum: str
    processed_at: str
    records_received: int
    records_valid: int
    records_rejected: int
    status: str

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
