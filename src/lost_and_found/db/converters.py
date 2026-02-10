from abc import ABC, abstractmethod
from datetime import datetime
from typing import Type
from ..state import Category

"""Converters for mapping Python types to/from SQLite representations.

Converters are used to register adapters/parsers with
`sqlite3` so application-specific types (for example `datetime` or
`Category`) can be stored and retrieved cleanly.
"""


class Converter[T](ABC):
    """Base class for converting values to/from bytes/strings for DB.

    Concrete implementations must provide the Python `type`, a `to_str`
    adapter and a `from_bytes` parser used when registering with
    `sqlite3`.
    """

    @staticmethod
    @abstractmethod
    def type() -> Type[T]:
        pass

    @staticmethod
    @abstractmethod
    def to_str(value: T) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_bytes(bytes: bytes) -> T:
        pass


class DatetimeConverter(Converter[datetime]):
    """Converter for `datetime` objects using ISO format."""

    @staticmethod
    def type() -> Type[datetime]:
        return datetime

    @staticmethod
    def to_str(value: datetime) -> str:
        return value.isoformat()

    @staticmethod
    def from_bytes(bytes: bytes) -> datetime:
        return datetime.fromisoformat(bytes.decode())


class CategoryConverter(Converter[Category]):
    """Converter for the `Category` enum value used by `Item`."""

    @staticmethod
    def type() -> Type[Category]:
        return Category

    @staticmethod
    def to_str(value: Category) -> str:
        return value.value

    @staticmethod
    def from_bytes(bytes: bytes) -> Category:
        return Category(bytes.decode())
