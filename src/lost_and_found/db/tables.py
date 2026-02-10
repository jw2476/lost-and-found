from abc import ABC, abstractmethod
from sqlite3 import Cursor
from typing import Any, Optional, cast
from ..core import ImmutableList
from ..state import Entity, EntityId, Item

"""Database table abstractions.

`Table` provides a mapping between Python entity objects and rows in a
SQLite table. Concrete tables should implement the SQL query helpers and
row (de)serialization functions.
"""


class Table[T: Entity](ABC):
    """Base class representing a DB table for entities of type `T`.

    The class stores a cursor and maintains a mapping between SQLite primary
    keys and in-memory `EntityId`s so rows can be correlated with model
    entities.
    """

    def __init__(self, cursor: Cursor) -> None:
        self.cursor: Cursor = cursor
        self._pk_to_id: dict[int, EntityId] = {}

        self.create_table()

    def id(self, pk: int) -> EntityId:
        """Return the `EntityId` for a given primary key, creating one if
        none exists yet.
        """
        for key, value in self._pk_to_id.items():
            if key == pk:
                return value

        return EntityId.new()

    def pk(self, id: EntityId) -> Optional[int]:
        """Return the primary key for an `EntityId` if known, otherwise
        `None`.
        """
        for key, value in self._pk_to_id.items():
            if value == id:
                return key

    @abstractmethod
    def from_row(self, id: EntityId, row: tuple[Any, ...]) -> T:
        pass

    @abstractmethod
    def to_row(self, value: T) -> tuple[Any, ...]:
        pass

    @abstractmethod
    def create_table_query(self) -> str:
        pass

    @abstractmethod
    def select_all_query(self) -> str:
        pass

    @abstractmethod
    def insert_query(self) -> str:
        pass

    @abstractmethod
    def update_query(self) -> str:
        pass

    @abstractmethod
    def delete_query(self) -> str:
        pass

    def create_table(self) -> None:
        """Execute the table creation SQL returned by `create_table_query`."""
        self.cursor.execute(self.create_table_query())

    def select_all(self) -> ImmutableList[T]:
        """Select all rows from the table and return them as an
        `ImmutableList` of entities.
        """
        self.cursor.execute(self.select_all_query())
        values = ImmutableList[T](())

        for row in self.cursor.fetchall():
            pk = int(row[0])
            id = self.id(pk)
            values = values.append(self.from_row(id, row[1:]))
            self._pk_to_id[pk] = id

        return values

    def insert(self, value: T) -> None:
        """Insert `value` as a new row and record its primary key mapping."""
        assert self.pk(value.id) is None, "Cannot reinsert an existing value"

        self.cursor.execute(
            self.insert_query(),
            self.to_row(value),
        )

        self._pk_to_id[cast(int, self.cursor.lastrowid)] = value.id

    def update(self, value: T) -> None:
        """Update an existing row corresponding to `value`."""
        pk = self.pk(value.id)
        assert pk is not None, (
            "Cannot update a value that is not in the database"
        )

        self.cursor.execute(
            self.update_query(),
            (
                *self.to_row(value),
                pk,
            ),
        )

    def delete(self, value: T) -> None:
        """Remove the row that corresponds to `value`."""
        pk = self.pk(value.id)
        assert pk is not None, (
            "Cannot remove a value that is not in the database"
        )

        self.cursor.execute(
            self.delete_query(),
            (pk,),
        )


class ItemsTable(Table[Item]):
    """Concrete table implementation for `Item` entities."""

    def from_row(self, id: EntityId, row: tuple[Any, ...]) -> Item:
        return Item(id, ImmutableList[Entity](()), *row)

    def to_row(self, value: Item) -> tuple[Any, ...]:
        return (
            value.name,
            value.category,
            value.lost,
            value.found,
            value.claimed,
            value.location,
            value.finder_email,
            value.owner_email,
        )

    def create_table_query(self) -> str:
        return """
            CREATE TABLE IF NOT EXISTS items (
                pk INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                category Category NOT NULL,
                lost datetime NOT NULL,
                found datetime,
                claimed datetime,
                location TEXT,
                finder_email TEXT,
                owner_email TEXT
            )
        """

    def select_all_query(self) -> str:
        return """
            SELECT
                pk,
                name,
                category,
                lost,
                found,
                claimed,
                location,
                finder_email,
                owner_email
            FROM items
            """

    def insert_query(self) -> str:
        return """
            INSERT INTO items (
                name,
                category,
                lost,
                found,
                claimed,
                location,
                finder_email,
                owner_email
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

    def update_query(self) -> str:
        return """
            UPDATE items
            SET
                name = ?,
                category = ?,
                lost = ?,
                found = ?,
                claimed = ?,
                location = ?,
                finder_email = ?,
                owner_email = ?
            WHERE pk = ?
            """

    def delete_query(self) -> str:
        return """
            DELETE FROM items
            WHERE pk = ?
            """
