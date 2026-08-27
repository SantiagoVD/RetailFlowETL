"""Validation and safe S3-key construction for uploads."""

from dataclasses import dataclass
from pathlib import PurePosixPath
from uuid import uuid4

from retailflow_api.common.exceptions import ApiError

ALLOWED_DATASETS = ("sales", "customers", "products", "stores", "payments", "inventory")
ALLOWED_EXTENSIONS = (".csv", ".json", ".xlsx")
CONTENT_TYPES = {
    ".csv": {"text/csv", "application/csv", "application/octet-stream"},
    ".json": {"application/json", "text/json", "application/octet-stream"},
    ".xlsx": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/octet-stream"},
}


@dataclass(frozen=True)
class UploadRequest:
    dataset: str
    file_name: str
    content_type: str


def validate_upload_request(payload: object) -> UploadRequest:
    if not isinstance(payload, dict):
        raise ApiError("El cuerpo debe ser un objeto JSON")
    dataset = payload.get("dataset")
    file_name = payload.get("file_name")
    content_type = payload.get("content_type")
    if not isinstance(dataset, str) or dataset not in ALLOWED_DATASETS:
        raise ApiError(f"dataset debe ser uno de: {', '.join(ALLOWED_DATASETS)}")
    if not isinstance(file_name, str) or not _safe_file_name(file_name):
        raise ApiError("file_name debe ser un nombre seguro sin rutas")
    extension = PurePosixPath(file_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ApiError("file_name debe terminar en .csv, .json o .xlsx")
    if not isinstance(content_type, str) or content_type not in CONTENT_TYPES[extension]:
        raise ApiError(f"content_type no está permitido para {extension}")
    return UploadRequest(dataset, file_name, content_type)


def build_upload_id() -> str:
    return f"UPLOAD-{uuid4()}"


def build_object_key(input_prefix: str, request: UploadRequest, upload_id: str) -> str:
    return "/".join((input_prefix.strip("/"), request.dataset, upload_id, request.file_name))


def _safe_file_name(file_name: str) -> bool:
    return (
        1 <= len(file_name) <= 128
        and "/" not in file_name
        and "\\" not in file_name
        and file_name not in {".", ".."}
        and not file_name.startswith(".")
        and all(ord(character) >= 32 for character in file_name)
    )
