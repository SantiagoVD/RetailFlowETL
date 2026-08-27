# S3 structure

`input/<dataset>/` is the only triggerable prefix. `bronze/`, `silver/`, `gold/` and `quarantine/` contain partitioned Parquet with `year`, `month`, `day` and `run_id`. `metadata/processed/<dataset>/<sha256>.json` is the idempotency ledger. `metadata/runs/<run_id>.json` contains counts, timings, output keys and status.
