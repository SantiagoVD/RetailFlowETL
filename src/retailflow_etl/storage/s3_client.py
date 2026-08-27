"""Compatibility factory for the storage adapter."""

from typing import Any

from retailflow_etl.storage.s3_repository import S3Repository


def create_s3_repository(bucket: str, client: Any | None = None) -> S3Repository:
    """Create the only production S3 gateway used by the application."""
    return S3Repository(bucket=bucket, client=client)
