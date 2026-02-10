from abc import ABC
from typing import Callable, Optional
from ..core import ImmutableList, Property, ValueObservable
from .app import App
from .entity import Entity, Hierarchy, ListEntity
from .item import Category, Item
from .search import SearchParams

"""Model layer helpers that expose properties and observable views.

This module provides `Model` classes which bridge the `Hierarchy` state
structure and UI-facing observable properties. They are small adapters that
surface convenient `Property` and `ValueObservable` objects for use by the
UI code.
"""


class Model[T: Entity](ABC):
    """Base model providing property and observe helpers for an entity."""

    def __init__(
        self, hierarchy: Hierarchy, entity: ValueObservable[T]
    ) -> None:
        self.hierarchy = hierarchy
        self.entity = entity

    def property[TValue](
        self, getter: Callable[[T], TValue], setter: Callable[[T, TValue], T]
    ) -> Property[TValue]:
        """Expose a `Property` backed by a getter/setter pair on the entity.

        The returned `Property` is kept in sync with the underlying entity and
        updates propagate back into the hierarchy via `setter`.
        """
        property = Property[TValue](getter(self.entity.value))

        self.entity.map(getter).on_change_only().subscribe(property.update)
        property.on_change_only().subscribe(
            lambda value: self.hierarchy.update(
                setter(self.entity.value, value)
            )
        )

        return property

    def observe[TValue](
        self, getter: Callable[[T], TValue]
    ) -> ValueObservable[TValue]:
        """Return a `ValueObservable` view for a derived value on
        the entity."""
        return self.entity.map(getter).on_change_only()

    def update(self, update: Callable[[T], T]) -> None:
        """Apply a transformation to the current entity and update the
        hierarchy."""
        self.hierarchy.update(update(self.entity.value))


class ListModel[T: Entity](Model[ListEntity[T]]):
    """Model helpers for list-like entities exposing `items` and mutations."""

    @property
    def items(self) -> ValueObservable[ImmutableList[T]]:
        return self.observe(lambda items: items.items)

    def append(self, item: T) -> None:
        self.update(lambda items: items.append(item))

    def remove_all(self, to_remove: ImmutableList[T]) -> None:
        self.update(lambda items: items.remove_all(to_remove))

    def set(self, items: ImmutableList[T]) -> None:
        self.update(lambda x: x.set(items))


class SearchParamsModel(Model[SearchParams]):
    """Model exposing `SearchParams` fields as properties."""

    @property
    def name(self) -> Property[str]:
        return self.property(
            lambda x: x.name,
            lambda x, new_name: x.update_name(new_name),
        )

    @property
    def category(self) -> Property[Optional[Category]]:
        return self.property(
            lambda x: x.category,
            lambda x, new_category: x.update_category(new_category),
        )


class ItemsModel(ListModel[Item]):
    """Model for `Item` collections including a searchable view."""

    def search(
        self, params: SearchParamsModel
    ) -> ValueObservable[ImmutableList[Item]]:
        return (
            ValueObservable.combine(self.items, params.entity)
            .map(lambda pair: self._search(pair[0], pair[1]))
            .on_change_only()
        )

    def _search(
        self, items: ImmutableList[Item], params: SearchParams
    ) -> ImmutableList[Item]:
        filtered = ImmutableList[Item]()

        for item in items:
            name_match = params.name.lower() in item.name.lower()
            category_match = (
                params.category is None or item.category == params.category
            )

            if name_match and category_match:
                filtered = filtered.append(item)

        return filtered


class AppModel(Model[App]):
    @property
    def items(self) -> ItemsModel:
        return ItemsModel(
            self.hierarchy, self.entity.map(lambda app: app.items)
        )

    @property
    def search_params(self) -> SearchParamsModel:
        return SearchParamsModel(
            self.hierarchy, self.entity.map(lambda app: app.search_params)
        )
