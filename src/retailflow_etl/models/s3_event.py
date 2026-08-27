"""S3 event parsing models."""

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from retailflow_etl.common.constants import DATASETS, INPUT_PREFIX
from retailflow_etl.common.exceptions import IngestionException
from retailflow_etl.common.file_utils import dataset_from_key, decode_s3_key, extension_from_key
from retailflow_etl.models.dataset import Dataset


@dataclass(frozen=True)
class S3InputEvent:
    bucket: str
    key: str
    dataset: Dataset

    @property
    def upload_id(self) -> str | None:
        """Return the backend upload identifier when it is present in the key."""
        parts = PurePosixPath(self.key).parts
        if len(parts) >= 4 and parts[2].startswith("UPLOAD-"):
            return parts[2]
        return None

    @classmethod
    def from_event(cls, event: dict[str, Any]) -> "S3InputEvent":
        try:
            record = event["Records"][0]
            bucket = record["s3"]["bucket"]["name"]
            key = decode_s3_key(record["s3"]["object"]["key"])
            dataset_name = dataset_from_key(key)
        except (KeyError, IndexError, ValueError) as exc:
            raise IngestionException("Malformed S3 event") from exc
        extension = extension_from_key(key)
        if not key.startswith(INPUT_PREFIX) or dataset_name not in DATASETS:
            raise IngestionException(f"Unsupported input key: {key}")
        return cls(bucket, key, Dataset(dataset_name, key, key.rsplit("/", 1)[-1], extension))
