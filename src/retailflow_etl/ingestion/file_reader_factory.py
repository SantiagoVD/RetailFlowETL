"""Reader factory."""

from retailflow_etl.common.exceptions import UnsupportedFileException
from retailflow_etl.ingestion.readers.base_reader import BaseReader
from retailflow_etl.ingestion.readers.csv_reader import CsvReader
from retailflow_etl.ingestion.readers.excel_reader import ExcelReader
from retailflow_etl.ingestion.readers.json_reader import JsonReader


class FileReaderFactory:
    _readers: dict[str, type[BaseReader]] = {".csv": CsvReader, ".json": JsonReader, ".xlsx": ExcelReader}

    @classmethod
    def create(cls, extension: str) -> BaseReader:
        try:
            return cls._readers[extension.lower()]()
        except KeyError as exc:
            raise UnsupportedFileException(f"Unsupported extension: {extension}") from exc
