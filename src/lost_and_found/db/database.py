import sqlite3
from abc import ABC, abstractmethod
from typing import Type

from ..state import Entity, ListModel
from .converters import Converter
from .replicator import Replicator
from .tables import Table

"""Database abstractions and SQLite-backed implementations.

Defines a minimal `Database` interface and small helpers to use SQLite as a
storage backend for application models. The `SqliteDatabase` class
registers converters and manages table instances used by the replication
layer.
"""


class Database(ABC):
    """A base class interface for database implementations."""

    @abstractmethod
    def register_converter(self, converter: Type[Converter]) -> None:
        """Register a converter type so custom types can be stored."""
        pass

    @abstractmethod
    def add_table(self, table: Type[Table]) -> None:
        """Create and register a `Table` instance."""
        pass

    @abstractmethod
    def replicate_table_to[T: Entity](
        self, table: Type[Table[T]], model: ListModel[T]
    ) -> None:
        """Start replicating changes from `model` into `table`."""
        pass


class SqliteDatabase(Database):
    """SQLite-backed `Database` implementation.

    This class wraps a sqlite3 connection and exposes simple helpers to
    register converters and to create table instances. Tables created via
    `add_table` will have their schema created immediately.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.isolation_level = None
        self.cursor = self.conn.cursor()

        self._tables: dict[Type[Table], Table] = {}

    def register_converter(self, converter: Type[Converter]) -> None:
        """Register adapter and converter functions with `sqlite3`."""
        sqlite3.register_adapter(converter.type(), converter.to_str)
        sqlite3.register_converter(
            converter.type().__name__, converter.from_bytes
        )

    def add_table(self, table: Type[Table]) -> None:
        """Instantiate and create the database table for `table`."""
        t = table(self.cursor)
        t.create_table()
        self._tables[table] = t

    def replicate_table_to[T: Entity](
        self, table: Type[Table[T]], model: ListModel[T]
    ) -> None:
        """Attach a `Replicator` to mirror a model into a DB table."""
        Replicator[T](model, self._tables[table])


class FileDatabase(SqliteDatabase):
    """A `SqliteDatabase` backed by a file on disk."""

    def __init__(self, path: str) -> None:
        super().__init__(
            sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        )


class InMemoryDatabase(SqliteDatabase):
    """An in-memory `SqliteDatabase` useful for tests and ephemeral use."""

    def __init__(self) -> None:
        super().__init__(
            sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        )
