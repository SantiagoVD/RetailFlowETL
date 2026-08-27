"""Centralized S3 key construction."""

from datetime import datetime


class PathBuilder:
    """Builds logical data-lake paths without embedding them in services."""

    def __init__(self, input_prefix: str = "input", output_prefix: str = "") -> None:
        self.input_prefix = input_prefix.strip("/")
        self.output_prefix = output_prefix.strip("/")

    def _join(self, *parts: str) -> str:
        return "/".join(part.strip("/") for part in parts if part.strip("/"))

    def input_key(self, dataset: str, filename: str) -> str:
        return self._join(self.input_prefix, dataset, filename)

    def data_key(self, layer: str, dataset: str, run_id: str, event_time: datetime) -> str:
        return self._join(
            self.output_prefix,
            layer,
            dataset,
            f"year={event_time.year:04d}",
            f"month={event_time.month:02d}",
            f"day={event_time.day:02d}",
            f"run_id={run_id}",
            f"{dataset}.parquet",
        )

    def gold_key(self, entity: str, run_id: str, event_time: datetime) -> str:
        return self.data_key("gold", entity, run_id, event_time)

    def quarantine_key(self, dataset: str, run_id: str, event_time: datetime) -> str:
        return self.data_key("quarantine", dataset, run_id, event_time)

    def processed_key(self, dataset: str, checksum: str) -> str:
        return self._join(self.output_prefix, "metadata/processed", dataset, f"{checksum}.json")

    def run_key(self, run_id: str) -> str:
        return self._join(self.output_prefix, "metadata/runs", f"{run_id}.json")
