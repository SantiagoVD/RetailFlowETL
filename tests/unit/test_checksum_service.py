from retailflow_etl.metadata.checksum_service import ChecksumService


def test_checksum_is_stable_and_content_based():
    first = ChecksumService.calculate(b"retail")
    assert first == ChecksumService.calculate(b"retail")
    assert first != ChecksumService.calculate(b"different")
