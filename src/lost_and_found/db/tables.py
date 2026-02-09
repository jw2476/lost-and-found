import sqlite3
from lost_and_found.core import ImmutableList
from ..state import Item, Entity, EntityId
from typing import Any, Optional, cast
from sqlite3 import Cursor
from abc import ABC, abstractmethod


class Table[T: Entity](ABC):
    def __init__(self, cursor: Cursor) -> None:
        self.cursor: Cursor = cursor
        self._pk_to_id: dict[int, EntityId] = {}

        self.create_table()

    def id(self, pk: int) -> EntityId:
        for key, value in self._pk_to_id.items():
            if key == pk:
                return value

        return EntityId.new()

    def pk(self, id: EntityId) -> Optional[int]:
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
    def create_table(self) -> None:
        pass

    @abstractmethod
    def select_all(self) -> list[tuple[Any, ...]]:
        pass

    @abstractmethod
    def insert(self, value: Item) -> None:
        pass

    @abstractmethod
    def update(self, value: Item) -> None:
        pass

    @abstractmethod
    def delete(self, value: Item) -> None:
        pass


class ItemsTable(Table[Item]):
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

    def create_table(self) -> None:
        self.cursor.execute(
            """
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
        )

    def select_all(self) -> list[tuple[Any, ...]]:
        self.cursor.execute(
            """
            SELECT
                id,
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
        )

        return self.cursor.fetchall()

    def insert(self, value: Item) -> None:
        assert self.pk(value.id) is None, "Cannot reinsert an existing item"

        self.cursor.execute(
            """
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
            """,
            self.to_row(value),
        )

        self._pk_to_id[cast(int, self.cursor.lastrowid)] = value.id

    def update(self, value: Item) -> None:
        pk = self.pk(value.id)
        assert pk is not None, (
            "Cannot update an item that is not in the database"
        )

        self.cursor.execute(
            """
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
            """,
            (
                *self.to_row(value),
                pk,
            ),
        )

    def delete(self, value: Item) -> None:
        pk = self.pk(value.id)
        assert pk is not None, (
            "Cannot remove an item that is not in the database"
        )

        self.cursor.execute(
            """
            DELETE FROM items
            WHERE id = ?
            """,
            (pk,),
        )
