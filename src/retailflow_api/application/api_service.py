"""HTTP API routing and response shaping."""

import base64
import json
import logging
import re
from typing import Any

from retailflow_api.common.exceptions import ApiError, NotFoundError
from retailflow_api.config.settings import ApiSettings
from retailflow_api.storage.s3_gateway import S3Gateway
from retailflow_api.uploads.validation import build_object_key, build_upload_id, validate_upload_request

LOG = logging.getLogger(__name__)
RUN_ROUTE = re.compile(r"^/runs/([^/]+)$")
UPLOAD_ROUTE = re.compile(r"^/uploads/([^/]+)$")
RUN_ACTION_ROUTE = re.compile(r"^/runs/([^/]+)/(result|errors|download|quarantine-download)$")


class ApiService:
    def __init__(self, gateway: S3Gateway, settings: ApiSettings) -> None:
        self.gateway = gateway
        self.settings = settings

    def handle(self, event: dict[str, Any]) -> dict[str, Any]:
        method = str(event.get("requestContext", {}).get("http", {}).get("method", event.get("httpMethod", "GET"))).upper()
        path = str(event.get("rawPath") or event.get("path") or "/").rstrip("/") or "/"
        try:
            if method == "POST" and path == "/uploads":
                return self._post_upload(event)
            if method == "GET" and path == "/runs":
                return self._response(200, {"items": self.gateway.list_runs(self._limit(event))})
            match = UPLOAD_ROUTE.fullmatch(path)
            if method == "GET" and match:
                return self._upload_status(match.group(1))
            match = RUN_ACTION_ROUTE.fullmatch(path)
            if method == "GET" and match:
                return self._run_action(match.group(1), match.group(2), self._limit(event))
            match = RUN_ROUTE.fullmatch(path)
            if method == "GET" and match:
                return self._response(200, self.gateway.get_run(match.group(1)))
            raise NotFoundError("Endpoint no encontrado")
        except ApiError as exc:
            return self._response(exc.status_code, {"error": {"code": exc.code, "message": exc.message}})
        except Exception:
            LOG.exception("La solicitud al API falló")
            return self._response(500, {"error": {"code": "INTERNAL_ERROR", "message": "No se pudo completar la solicitud"}})

    def _post_upload(self, event: dict[str, Any]) -> dict[str, Any]:
        payload = self._body(event)
        request = validate_upload_request(payload)
        upload_id = build_upload_id()
        object_key = build_object_key(self.settings.input_prefix, request, upload_id)
        presigned = self.gateway.generate_upload_post(request, upload_id)
        return self._response(
            201,
            {
                "upload_id": upload_id,
                "dataset": request.dataset,
                "file_name": request.file_name,
                "object_key": object_key,
                "upload_url": presigned["url"],
                "fields": presigned["fields"],
                "expires_in": self.settings.upload_url_expiry,
                "max_upload_bytes": self.settings.max_upload_bytes,
            },
        )

    def _upload_status(self, upload_id: str) -> dict[str, Any]:
        if not upload_id.startswith("UPLOAD-"):
            raise NotFoundError("ID de subida inválido")
        run = self.gateway.find_latest_run_by_upload(upload_id)
        if run is None:
            return self._response(200, {"upload_id": upload_id, "status": "PROCESSING"})
        return self._response(
            200,
            {
                "upload_id": upload_id,
                "run_id": run.get("run_id"),
                "original_run_id": run.get("original_run_id"),
                "dataset": run.get("dataset"),
                "status": run.get("status", "PROCESSING"),
                "records_received": run.get("records_received", 0),
                "records_valid": run.get("records_valid", 0),
                "records_rejected": run.get("records_rejected", 0),
            },
        )

    def _run_action(self, run_id: str, action: str, limit: int) -> dict[str, Any]:
        run = self.gateway.get_run(run_id)
        artifact_run = run
        if run.get("status") == "SKIPPED" and run.get("original_run_id"):
            artifact_run = self.gateway.get_run(str(run["original_run_id"]))
        if action == "result":
            return self._response(200, self.gateway.gold_preview(artifact_run, limit))
        if action == "errors":
            return self._response(200, self.gateway.quarantine_summary(artifact_run, limit))
        if action == "download":
            key = _primary_gold_key(artifact_run)
            if key is None:
                raise NotFoundError("La salida Gold no está disponible para esta ejecución")
            return self._response(200, self.gateway.presign_get(key))
        key = artifact_run.get("quarantine_key")
        if not isinstance(key, str):
            raise NotFoundError("La salida Quarantine no está disponible para esta ejecución")
        return self._response(200, self.gateway.presign_get(key))

    @staticmethod
    def _body(event: dict[str, Any]) -> object:
        body = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            body = base64.b64decode(body).decode("utf-8")
        try:
            return json.loads(body) if isinstance(body, str) else body
        except (TypeError, json.JSONDecodeError) as exc:
            raise ApiError("El cuerpo debe contener JSON válido") from exc

    @staticmethod
    def _limit(event: dict[str, Any]) -> int:
        query = event.get("queryStringParameters") or {}
        try:
            return max(1, min(int(query.get("limit", 50)), 100))
        except (TypeError, ValueError):
            return 50

    def _response(self, status_code: int, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "statusCode": status_code,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": self.settings.allowed_origin,
                "Access-Control-Allow-Headers": "content-type",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            },
            "body": json.dumps(payload, default=str),
        }


def _primary_gold_key(run: dict[str, Any]) -> str | None:
    keys = [key for key in run.get("gold_keys", []) if isinstance(key, str)]
    return next((key for key in keys if key.endswith("fact_sales.parquet")), None) or (keys[0] if keys else None)
