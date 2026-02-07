from typing import Callable
from lost_and_found.core.observable import ValueObservable, Property
from lost_and_found.state.entity import Entity, Hierarchy, SearchParams
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


class SearchParamsModel(Model[SearchParams]):
    @property
    def name(self) -> Property[str]:
        return self.property(
            lambda params: params.name, lambda params, name: params.update_name(name)
        )
