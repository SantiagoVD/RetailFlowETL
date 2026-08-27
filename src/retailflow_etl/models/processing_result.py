"""Pipeline result model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProcessingResult:
    status: str
    run_id: str
    dataset: str
    original_run_id: str | None = None
    records_received: int = 0
    records_valid: int = 0
    records_rejected: int = 0
    bronze_key: str | None = None
    silver_key: str | None = None
    gold_keys: list[str] = field(default_factory=list)
    quarantine_key: str | None = None
    error_message: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
