from typing import Type
import sqlite3
from ..state import Category
from datetime import datetime
from abc import ABC, abstractmethod


class Converter[T](ABC):
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
    @staticmethod
    def type() -> Type[Category]:
        return Category

    @staticmethod
    def to_str(value: Category) -> str:
        return value.value

    @staticmethod
    def from_bytes(bytes: bytes) -> Category:
        return Category(bytes.decode())
