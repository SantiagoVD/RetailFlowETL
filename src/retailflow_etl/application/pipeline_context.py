"""Context propagated through every pipeline stage."""

from dataclasses import dataclass
from datetime import datetime, timezone

from retailflow_etl.models.s3_event import S3InputEvent


@dataclass
class PipelineContext:
    event: S3InputEvent
    run_id: str
    checksum: str
    event_time: datetime

    @classmethod
    def create(cls, event: S3InputEvent, run_id: str, checksum: str, event_time: datetime | None = None) -> "PipelineContext":
        return cls(event, run_id, checksum, event_time or datetime.now(timezone.utc))
