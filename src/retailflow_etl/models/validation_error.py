"""Structured data-quality error."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationError:
    record_id: str
    rule: str
    column: str
    value: Any
    error_code: str
    error_message: str
    row_index: Any | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
