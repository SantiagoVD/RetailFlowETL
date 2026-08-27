from retailflow_etl.ingestion.readers.json_reader import JsonReader


def test_json_reader_reads_records():
    frame = JsonReader().read(b'[{"id": 1, "status": "PAID"}]')
    assert frame.to_dict("records") == [{"id": 1, "status": "PAID"}]
