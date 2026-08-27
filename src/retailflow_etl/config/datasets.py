"""Dataset configuration accessors."""

from typing import Any


def dataset_config(configuration: dict[str, Any], dataset: str) -> dict[str, Any]:
    return configuration.get("datasets", {}).get(dataset, {})
