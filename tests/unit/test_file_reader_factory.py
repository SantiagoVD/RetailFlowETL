import pytest

from retailflow_etl.common.exceptions import UnsupportedFileException
from retailflow_etl.ingestion.file_reader_factory import FileReaderFactory
from retailflow_etl.ingestion.readers.csv_reader import CsvReader
from retailflow_etl.ingestion.readers.excel_reader import ExcelReader
from retailflow_etl.ingestion.readers.json_reader import JsonReader


def test_factory_selects_supported_readers():
    assert isinstance(FileReaderFactory.create(".csv"), CsvReader)
    assert isinstance(FileReaderFactory.create(".json"), JsonReader)
    assert isinstance(FileReaderFactory.create(".xlsx"), ExcelReader)


def test_factory_rejects_unknown_extension():
    with pytest.raises(UnsupportedFileException):
        FileReaderFactory.create(".txt")
