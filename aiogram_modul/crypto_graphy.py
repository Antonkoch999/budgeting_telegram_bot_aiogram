from typing import Union

from cryptography.fernet import Fernet

from config import encoding_key


class EncodeDecodeService:
    """Service to process encode/decode info."""

    _encoding = 'utf-8'

    def __init__(self, key: Union[bytes, str] = encoding_key):
        self._key = key

    def encode(self, value: str) -> str:
        """Return encoded value."""
        cipher_suite = Fernet(self._key)
        return cipher_suite.encrypt(bytes(value, self._encoding)).decode(self._encoding)

    def decode(self, encode_value: str) -> str:
        """Return decoded value."""
        cipher_suite = Fernet(self._key)
        return cipher_suite.decrypt(bytes(encode_value, self._encoding)).decode(self._encoding)
