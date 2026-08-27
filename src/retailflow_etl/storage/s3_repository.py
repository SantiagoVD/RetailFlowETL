"""S3 gateway used by every application service."""

import json
from collections.abc import Iterable
from typing import Any

try:
    import boto3
except ImportError:  # pragma: no cover - only relevant for minimal local installs
    boto3 = None

from retailflow_etl.common.exceptions import StorageException


class S3Repository:
    """Small adapter around boto3; business code never calls boto3 directly."""

    def __init__(self, bucket: str, client: Any | None = None) -> None:
        self.bucket = bucket
        if client is not None:
            self.client = client
        elif boto3 is not None:
            self.client = boto3.client("s3")
        else:
            raise StorageException("boto3 is required for S3Repository")

    def get_object(self, key: str) -> bytes:
        try:
            return self.client.get_object(Bucket=self.bucket, Key=key)["Body"].read()
        except Exception as exc:
            raise StorageException(f"Could not read s3://{self.bucket}/{key}") from exc

    def put_object(self, key: str, body: bytes, content_type: str = "application/octet-stream") -> None:
        try:
            self.client.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType=content_type)
        except Exception as exc:
            raise StorageException(f"Could not write s3://{self.bucket}/{key}") from exc

    def object_exists(self, key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except Exception as exc:
            error = getattr(exc, "response", {}).get("Error", {})
            if error.get("Code") in {"404", "NoSuchKey", "NotFound"}:
                return False
            return False

    def copy_object(self, source_key: str, destination_key: str) -> None:
        try:
            self.client.copy_object(Bucket=self.bucket, Key=destination_key, CopySource={"Bucket": self.bucket, "Key": source_key})
        except Exception as exc:
            raise StorageException("Could not copy S3 object") from exc

    def list_objects(self, prefix: str) -> Iterable[str]:
        try:
            paginator = self.client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
                yield from (item["Key"] for item in page.get("Contents", []))
        except Exception as exc:
            raise StorageException(f"Could not list s3://{self.bucket}/{prefix}") from exc

    def read_json(self, key: str) -> dict[str, Any]:
        return json.loads(self.get_object(key).decode("utf-8"))

    def write_json(self, key: str, value: dict[str, Any]) -> None:
        self.put_object(key, json.dumps(value, default=str, indent=2).encode("utf-8"), "application/json")


class InMemoryS3Repository:
    """Deterministic S3 substitute for local execution and unit tests."""

    def __init__(self, bucket: str = "local-retailflow") -> None:
        self.bucket = bucket
        self.objects: dict[str, bytes] = {}

    def get_object(self, key: str) -> bytes:
        if key not in self.objects:
            raise StorageException(f"Missing local object {key}")
        return self.objects[key]

    def put_object(self, key: str, body: bytes, content_type: str = "application/octet-stream") -> None:
        del content_type
        self.objects[key] = body

    def object_exists(self, key: str) -> bool:
        return key in self.objects

    def copy_object(self, source_key: str, destination_key: str) -> None:
        self.objects[destination_key] = self.get_object(source_key)

    def list_objects(self, prefix: str) -> Iterable[str]:
        return (key for key in self.objects if key.startswith(prefix))

    def read_json(self, key: str) -> dict[str, Any]:
        return json.loads(self.get_object(key).decode("utf-8"))

    def write_json(self, key: str, value: dict[str, Any]) -> None:
        self.put_object(key, json.dumps(value, default=str).encode("utf-8"), "application/json")
