"""Environment-backed API settings."""

import os
from dataclasses import dataclass


def _integer(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class ApiSettings:
    bucket: str
    input_prefix: str
    metadata_prefix: str
    gold_prefix: str
    quarantine_prefix: str
    upload_url_expiry: int
    download_url_expiry: int
    max_upload_bytes: int
    allowed_origin: str

    @classmethod
    def from_env(cls) -> "ApiSettings":
        return cls(
            bucket=os.getenv("DATA_BUCKET", "retailflow-local"),
            input_prefix=os.getenv("INPUT_PREFIX", "input").strip("/"),
            metadata_prefix=os.getenv("METADATA_PREFIX", "metadata").strip("/"),
            gold_prefix=os.getenv("GOLD_PREFIX", "gold").strip("/"),
            quarantine_prefix=os.getenv("QUARANTINE_PREFIX", "quarantine").strip("/"),
            upload_url_expiry=max(60, min(_integer("UPLOAD_URL_EXPIRY", 300), 900)),
            download_url_expiry=max(60, min(_integer("DOWNLOAD_URL_EXPIRY", 300), 900)),
            max_upload_bytes=max(1, min(_integer("MAX_UPLOAD_BYTES", 10 * 1024 * 1024), 10 * 1024 * 1024)),
            allowed_origin=os.getenv("ALLOWED_ORIGIN", "http://localhost:5173"),
        )
