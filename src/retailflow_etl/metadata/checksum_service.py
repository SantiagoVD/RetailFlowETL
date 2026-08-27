"""Content checksum service."""

import hashlib


class ChecksumService:
    """Compute stable SHA-256 checksums for source bytes."""

    @staticmethod
    def calculate(payload: bytes) -> str:
        return hashlib.sha256(payload).hexdigest()
