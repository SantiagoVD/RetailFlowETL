$ErrorActionPreference = 'Stop'
python -m pytest -q --cov=src/retailflow_etl --cov-report=term-missing
