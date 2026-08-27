from retailflow_etl.models.s3_event import S3InputEvent


def test_s3_event_decodes_url_encoded_key():
    parsed = S3InputEvent.from_event({"Records": [{"s3": {"bucket": {"name": "b"}, "object": {"key": "input%2Fsales%2Fmonthly+sales.csv"}}}]})
    assert parsed.key == "input/sales/monthly sales.csv"
    assert parsed.dataset.name == "sales"
