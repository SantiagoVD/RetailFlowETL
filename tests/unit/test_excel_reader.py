import io

import pandas as pd

from retailflow_etl.ingestion.readers.excel_reader import ExcelReader


def test_excel_reader_reads_xlsx():
    output = io.BytesIO()
    pd.DataFrame({"id": [1], "value": ["ok"]}).to_excel(output, index=False)
    assert ExcelReader().read(output.getvalue()).iloc[0]["value"] == "ok"
