"""Shared constants."""

DATASETS = ("sales", "customers", "products", "stores", "payments", "inventory")
SUPPORTED_EXTENSIONS = {".csv", ".json", ".xlsx"}
INPUT_PREFIX = "input/"
PIPELINE_STAGES = ("INGESTION", "BRONZE", "QUALITY", "QUARANTINE", "SILVER", "GOLD")
RUN_STATUSES = ("STARTED", "SUCCESS", "FAILED", "SKIPPED")
