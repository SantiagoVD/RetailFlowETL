import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))


@pytest.fixture
def quality_config():
    return {
        "datasets": {
            "sales": [
                {"type": "null", "columns": ["sale_id", "sale_date", "quantity"]},
                {"type": "duplicate", "columns": ["sale_id"]},
                {"type": "date", "column": "sale_date"},
                {"type": "range", "column": "quantity", "min": 0.000001},
                {"type": "range", "column": "unit_price", "min": 0},
            ]
        }
    }
