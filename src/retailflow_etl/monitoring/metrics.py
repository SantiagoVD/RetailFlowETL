"""CloudWatch-friendly metrics logging."""

import logging


def record_metric(logger: logging.Logger, name: str, value: int | float, unit: str = "Count") -> None:
    logger.info("metric", extra={"metric_name": name, "metric_value": value, "metric_unit": unit})
