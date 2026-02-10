from __future__ import annotations
import abc
import uuid
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, cast
from uuid import UUID
from ..core import ImmutableList, Property, ValueObservable

"""Entity and hierarchy primitives for the application state.

Defines `EntityId`, `Entity` and simple collection entities used to
construct the application's in-memory hierarchical state. `Hierarchy` wraps
an entity tree and provides update utilities.
"""


@dataclass(frozen=True)
class EntityId:
    """Lightweight wrapper around a UUID used to identify entities."""

    id: UUID

    @staticmethod
    def new() -> EntityId:
        """Create a new `EntityId` with a random UUID."""
        return EntityId(uuid.uuid4())


@dataclass(frozen=True)
class Entity(abc.ABC):
    """Base class for state entities.

    Entities are immutable dataclasses containing an `id` and zero or more
    children. Subclasses must implement `update_child` to return a new
    instance with a replaced child entity.
    """

    id: EntityId
    children: ImmutableList[Entity]

    @abstractmethod
    def update_child(self, child: Entity) -> Entity:
        pass

    def get(self, id: EntityId) -> Optional[Entity]:
        """Recursively find an entity with `id` in this subtree, or `None`."""
        if self.id == id:
            return self

        for child in self.children:
            entity = child.get(id)
            if entity is not None:
                return entity


@dataclass(frozen=True)
class ListEntity[T: Entity](Entity):
    """An `Entity` that holds an ordered list of child entities in `items`."""

    items: ImmutableList[T] = ImmutableList[T]()

    @staticmethod
    def new() -> ListEntity[T]:
        items = ImmutableList[T]()
        return ListEntity[T](EntityId.new(), items, items)

    def append(self, entity: T) -> ListEntity[T]:
        """Return a new `ListEntity` with `entity` appended to `items`."""
        items = self.items.append(entity)
        return ListEntity[T](self.id, items, items)

    def remove_all(self, to_remove: ImmutableList[T]) -> ListEntity[T]:
        """Return a new `ListEntity` with `to_remove` removed."""
        items = self.items

        for item in to_remove:
            items = items.remove(item)

        return ListEntity[T](self.id, items, items)

    def set(self, items: ImmutableList[T]) -> ListEntity[T]:
        """Replace the `items` collection and return a new `ListEntity`."""
        return ListEntity[T](self.id, items, items)

    def update_child(self, child: Entity) -> ListEntity[T]:
        items: ImmutableList[T] = ImmutableList[T]()

        for item in self.items:
            if item.id == child.id:
                items = items.append(cast(T, child))
            else:
                items = items.append(item)

        return ListEntity[T](self.id, items, items)


class Hierarchy[T: Entity]:
    """Wrap an entity tree and provide atomic update operations."""

    def __init__(self, root: T) -> None:
        self._root: Property[T] = Property[T](root)

    @property
    def root(self) -> T:
        return self._root.value

    @property
    def observable(self) -> ValueObservable[T]:
        return self._root

    def update(self, entity: Entity) -> None:
        """Apply an update to the tree by replacing the matching entity."""
        root: T = cast(T, Hierarchy._update(self.root, entity))
        self._root.update(root)

    @staticmethod
    def _update[T: Entity](entity: Entity, updated: Entity) -> Entity:
        if any(child.id == updated.id for child in entity.children):
            return entity.update_child(updated)

        for child in entity.children:
            updated_child = Hierarchy._update(child, updated)
            if id(child) != id(updated_child):
                return entity.update_child(updated_child)

        return entity
