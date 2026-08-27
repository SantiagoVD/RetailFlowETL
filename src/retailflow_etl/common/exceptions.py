"""Domain exceptions for RetailFlow."""


class RetailFlowException(Exception):
    """Base exception for expected application failures."""


class IngestionException(RetailFlowException):
    """Raised when an input object cannot be read or identified."""


class UnsupportedFileException(IngestionException):
    """Raised when an input extension is not supported."""


class DataQualityException(RetailFlowException):
    """Raised when quality processing cannot be completed."""


class StorageException(RetailFlowException):
    """Raised when object storage operations fail."""


class TransformationException(RetailFlowException):
    """Raised when a Silver or Gold transformation fails."""


class MetadataException(RetailFlowException):
    """Raised when pipeline metadata cannot be persisted."""


class ConfigurationException(RetailFlowException):
    """Raised when required configuration is invalid."""
