from retailflow_etl.ingestion.readers.csv_reader import CsvReader


def test_csv_reader_reads_columns():
    frame = CsvReader().read(b"id,name\n1,Ana\n")
    assert list(frame.columns) == ["id", "name"]
    assert frame.iloc[0]["name"] == "Ana"
