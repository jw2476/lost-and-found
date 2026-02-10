import sqlite3
from abc import ABC, abstractmethod
from typing import Type

from ..state import Entity, ListModel
from .converters import Converter
from .replicator import Replicator
from .tables import Table


class Database(ABC):
    @abstractmethod
    def register_converter(self, converter: Type[Converter]) -> None:
        pass

    @abstractmethod
    def add_table(self, table: Type[Table]) -> None:
        pass

    @abstractmethod
    def replicate_table_to[T: Entity](
        self, table: Type[Table[T]], model: ListModel[T]
    ) -> None:
        pass


class SqliteDatabase(Database):
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.isolation_level = None
        self.cursor = self.conn.cursor()

        self._tables: dict[Type[Table], Table] = {}

    def register_converter(self, converter: Type[Converter]) -> None:
        sqlite3.register_adapter(converter.type(), converter.to_str)
        sqlite3.register_converter(
            converter.type().__name__, converter.from_bytes
        )

    def add_table(self, table: Type[Table]) -> None:
        t = table(self.cursor)
        t.create_table()
        self._tables[table] = t

    def replicate_table_to[T: Entity](
        self, table: Type[Table[T]], model: ListModel[T]
    ) -> None:
        Replicator[T](model, self._tables[table])


class FileDatabase(SqliteDatabase):
    def __init__(self, path: str) -> None:
        super().__init__(
            sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        )


class InMemoryDatabase(SqliteDatabase):
    def __init__(self) -> None:
        super().__init__(
            sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        )
