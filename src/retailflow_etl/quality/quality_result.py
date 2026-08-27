"""Data-quality result."""

from dataclasses import dataclass, field

import pandas as pd

from retailflow_etl.models.validation_error import ValidationError


@dataclass
class QualityResult:
    valid: pd.DataFrame
    rejected: pd.DataFrame
    errors: list[ValidationError] = field(default_factory=list)
