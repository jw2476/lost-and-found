from typing import Type
import sqlite3
from abc import ABC, abstractmethod
from .converters import Converter
from .tables import Table


class Database(ABC):
    @abstractmethod
    def register_converter(self, converter: Type[Converter]) -> None:
        pass

    @abstractmethod
    def add_table(self, table: Type[Table]) -> None:
        pass


class FileDatabase(Database):
    def __init__(self, path: str) -> None:
        self.conn = sqlite3.connect(path)
        self.conn.isolation_level = None
        self.cursor = self.conn.cursor()

    def register_converter(self, converter: Type[Converter]) -> None:
        sqlite3.register_adapter(converter.type(), converter.to_str)
        sqlite3.register_converter(
            converter.type().__name__, converter.from_bytes
        )

    def add_table(self, table: Type[Table]) -> None:
        t = table(self.cursor)
        t.create_table()
