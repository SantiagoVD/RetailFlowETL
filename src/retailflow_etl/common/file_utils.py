"""Safe file and S3-key helpers."""

from pathlib import PurePosixPath
from urllib.parse import unquote_plus


def decode_s3_key(key: str) -> str:
    """Decode the URL encoding used by S3 notification keys."""
    return unquote_plus(key)


def dataset_from_key(key: str) -> str:
    """Extract a dataset from an input/<dataset>/... key."""
    parts = PurePosixPath(key).parts
    if len(parts) < 3 or parts[0] != "input":
        raise ValueError("S3 key must be under input/<dataset>/")
    return parts[1]


def extension_from_key(key: str) -> str:
    """Return a lowercase file extension."""
    return PurePosixPath(key).suffix.lower()
