"""Environment and YAML-backed application settings."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from retailflow_etl.common.exceptions import ConfigurationException

ROOT = Path(__file__).resolve().parents[3]


def load_yaml(name: str) -> dict[str, Any]:
    candidates = [ROOT / "config" / name, Path(__file__).parent / name]
    for path in candidates:
        if path.exists():
            try:
                with path.open(encoding="utf-8") as stream:
                    return yaml.safe_load(stream) or {}
            except OSError as exc:
                raise ConfigurationException(f"Could not read configuration {path}") from exc
    raise ConfigurationException(f"Could not find configuration {name}")


@dataclass(frozen=True)
class Settings:
    bucket: str
    region: str
    log_level: str
    input_prefix: str
    output_prefix: str
    data_quality: dict[str, Any]
    datasets: dict[str, Any]

    @classmethod
    def from_env(cls) -> "Settings":
        bucket = os.getenv("DATA_BUCKET", "retailflow-local")
        return cls(
            bucket=bucket,
            region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            input_prefix=os.getenv("INPUT_PREFIX", "input"),
            output_prefix=os.getenv("OUTPUT_PREFIX", ""),
            data_quality=load_yaml("data_quality.yaml"),
            datasets=load_yaml("datasets.yaml"),
        )
