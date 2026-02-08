from typing import Callable
from ..core import ValueObservable, Property, ImmutableList
from .entity import Entity, Hierarchy, SearchParams, ListEntity, Item
from abc import ABC


class Model[T: Entity](ABC):
    def __init__(self, hierarchy: Hierarchy, entity: ValueObservable[T]) -> None:
        self.hierarchy = hierarchy
        self.entity = entity

    def property[TValue](
        self, getter: Callable[[T], TValue], setter: Callable[[T, TValue], T]
    ) -> Property[TValue]:
        property = Property[TValue](getter(self.entity.value))

        self.entity.map(getter).on_change_only().subscribe(property.update)
        property.on_change_only().subscribe(
            lambda value: self.hierarchy.update(setter(self.entity.value, value))
        )

        return property

    def observe[TValue](self, getter: Callable[[T], TValue]) -> ValueObservable[TValue]:
        return self.entity.map(getter).on_change_only()

    def update(self, update: Callable[[T], T]) -> None:
        self.hierarchy.update(update(self.entity.value))


class SearchParamsModel(Model[SearchParams]):
    @property
    def name(self) -> Property[str]:
        return self.property(
            lambda params: params.name,
            lambda params, new_name: params.update_name(new_name),
        )


class ItemsModel(Model[ListEntity[Item]]):
    @property
    def items(self) -> ValueObservable[ImmutableList[Item]]:
        return self.observe(lambda items: items.items)

    def search(self, params: SearchParamsModel) -> ValueObservable[ImmutableList[Item]]:
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
            if name_match:
                filtered = filtered.append(item)

        return filtered

    def append(self, item: Item) -> None:
        self.update(lambda items: items.append(item))

    def remove_all(self, to_remove: ImmutableList[Item]) -> None:
        self.update(lambda items: items.remove_all(to_remove))
