from typing import Union

from cryptography.fernet import Fernet

from config import encoding_key


class EncodeDecodeService:
    """Service to process encode/decode info."""

    _encoding = 'utf-8'

    def __init__(self, key: Union[bytes, str] = encoding_key):
        self._key = key

    def encode_amount(self, amount: str) -> str:
        """Return encoded password."""
        cipher_suite = Fernet(self._key)
        return cipher_suite.encrypt(bytes(amount, self._encoding)).decode(self._encoding)

    def decode_amount(self, encoded_amount: str) -> str:
        """Return decoded password."""
        cipher_suite = Fernet(self._key)
        return cipher_suite.decrypt(bytes(encoded_amount, self._encoding)).decode(self._encoding)
