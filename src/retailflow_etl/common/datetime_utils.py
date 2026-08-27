"""Timezone-safe datetime helpers."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return the current UTC time as an aware datetime."""
    return datetime.now(timezone.utc)


def isoformat(value: datetime) -> str:
    """Serialize a datetime consistently for metadata."""
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
