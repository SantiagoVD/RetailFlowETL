"""S3 adapter used by the API Lambda."""

import json
import re
from collections import Counter
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import boto3
import pyarrow as pa
import pyarrow.parquet as parquet
from botocore.exceptions import ClientError

from retailflow_api.common.exceptions import ApiError, NotFoundError
from retailflow_api.config.settings import ApiSettings
from retailflow_api.uploads.validation import UploadRequest

RUN_ID_PATTERN = re.compile(r"^RUN-[A-Za-z0-9-]+$")


class S3Gateway:
    def __init__(self, settings: ApiSettings, client: Any | None = None) -> None:
        self.settings = settings
        self.client = client or boto3.client("s3")

    def generate_upload_post(self, request: UploadRequest, upload_id: str) -> dict[str, Any]:
        key = "/".join((self.settings.input_prefix, request.dataset, upload_id, request.file_name))
        fields = {"key": key, "Content-Type": request.content_type}
        conditions: list[Any] = [
            {"key": key},
            {"Content-Type": request.content_type},
            ["content-length-range", 1, self.settings.max_upload_bytes],
        ]
        return self.client.generate_presigned_post(
            Bucket=self.settings.bucket,
            Key=key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=self.settings.upload_url_expiry,
        )

    def list_run_keys(self) -> list[str]:
        prefix = f"{self.settings.metadata_prefix}/runs/"
        paginator = self.client.get_paginator("list_objects_v2")
        return [item["Key"] for page in paginator.paginate(Bucket=self.settings.bucket, Prefix=prefix) for item in page.get("Contents", [])]

    def get_json(self, key: str) -> dict[str, Any]:
        try:
            response = self.client.get_object(Bucket=self.settings.bucket, Key=key)
            return json.loads(response["Body"].read().decode("utf-8"))
        except ClientError as exc:
            code = str(exc.response.get("Error", {}).get("Code", ""))
            if code in {"404", "NoSuchKey", "NotFound"}:
                raise NotFoundError(f"Objeto S3 no encontrado: {key}") from exc
            raise

    def get_run(self, run_id: str) -> dict[str, Any]:
        if not RUN_ID_PATTERN.fullmatch(run_id):
            raise NotFoundError("ID de ejecución inválido")
        return self.get_json(f"{self.settings.metadata_prefix}/runs/{run_id}.json")

    def list_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        runs = []
        for key in self.list_run_keys():
            try:
                runs.append(self.get_json(key))
            except NotFoundError:
                continue
        runs.sort(key=lambda item: str(item.get("start_time", "")), reverse=True)
        return runs[: max(1, min(limit, 100))]

    def find_latest_run_by_upload(self, upload_id: str) -> dict[str, Any] | None:
        matches = [run for run in self.list_runs(100) if run.get("upload_id") == upload_id]
        return matches[0] if matches else None

    def get_bytes(self, key: str) -> bytes:
        try:
            response = self.client.get_object(Bucket=self.settings.bucket, Key=key)
            return response["Body"].read()
        except ClientError as exc:
            code = str(exc.response.get("Error", {}).get("Code", ""))
            if code in {"404", "NoSuchKey", "NotFound"}:
                raise NotFoundError(f"Objeto S3 no encontrado: {key}") from exc
            raise

    def gold_preview(self, run: dict[str, Any], limit: int = 50) -> dict[str, Any]:
        gold_keys = [key for key in run.get("gold_keys", []) if isinstance(key, str)]
        preferred = next((key for key in gold_keys if key.endswith("fact_sales.parquet")), None)
        key = preferred or (gold_keys[0] if gold_keys else None)
        if key is None:
            raise NotFoundError("La salida Gold no está disponible para esta ejecución")
        table = self.read_parquet(key)
        safe_limit = max(1, min(limit, 100))
        return {
            "run_id": run.get("run_id"),
            "dataset": run.get("dataset"),
            "total_records": table.num_rows,
            "preview_count": min(table.num_rows, safe_limit),
            "columns": table.column_names,
            "rows": [_json_safe(row) for row in table.slice(0, safe_limit).to_pylist()],
            "source_key": key,
        }

    def quarantine_summary(self, run: dict[str, Any], limit: int = 50) -> dict[str, Any]:
        key = run.get("quarantine_key")
        if not isinstance(key, str):
            raise NotFoundError("La salida Quarantine no está disponible para esta ejecución")
        table = self.read_parquet(key)
        rows = table.to_pylist()
        summary: Counter[str] = Counter()
        preview: list[dict[str, Any]] = []
        for row in rows:
            codes = _split_values(row.get("_error_codes"), "QUALITY_ERROR")
            messages = _split_values(row.get("_error_messages"), "El registro no superó la calidad de datos")
            summary.update(codes)
            if len(preview) < max(1, min(limit, 100)):
                record_id = next((value for name, value in row.items() if not name.startswith("_")), None)
                preview.append({"record_id": _json_safe(record_id), "error_codes": codes, "error_messages": messages})
        return {
            "run_id": run.get("run_id"),
            "records_rejected": int(run.get("records_rejected", table.num_rows)),
            "summary": dict(summary),
            "preview": preview,
        }

    def presign_get(self, key: str) -> dict[str, Any]:
        if not isinstance(key, str) or not key:
            raise ApiError("La salida solicitada no está disponible", 404, "OUTPUT_NOT_FOUND")
        return {
            "download_url": self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.settings.bucket, "Key": key},
                ExpiresIn=self.settings.download_url_expiry,
            ),
            "expires_in": self.settings.download_url_expiry,
        }

    def read_parquet(self, key: str) -> pa.Table:
        return parquet.read_table(pa.BufferReader(self.get_bytes(key)))


def _split_values(value: Any, fallback: str) -> list[str]:
    if value is None:
        return [fallback]
    return [part for part in str(value).split(";") if part] or [fallback]


def _json_safe(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value.item() if hasattr(value, "item") else value
