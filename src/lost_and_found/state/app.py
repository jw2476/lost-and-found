from __future__ import annotations
from typing import cast
from ..core import ImmutableList
from .entity import Entity, EntityId, ListEntity
from .item import Item
from .search import SearchParams
from dataclasses import dataclass


@dataclass(frozen=True)
class App(Entity):
    items_id: EntityId
    search_params_id: EntityId

    @staticmethod
    def new() -> App:
        items: ListEntity[Item] = ListEntity[Item].new()
        search_params: SearchParams = SearchParams.new()

        return App(
            EntityId.new(),
            children=ImmutableList[Entity]((items, search_params)),
            items_id=items.id,
            search_params_id=search_params.id,
        )

    @property
    def items(self) -> ListEntity[Item]:
        return cast(ListEntity[Item], self.get(self.items_id))

    @property
    def search_params(self) -> SearchParams:
        return cast(SearchParams, self.get(self.search_params_id))

    def update_child(self, child: Entity) -> App:
        children: ImmutableList[Entity] = ImmutableList[Entity]()

        for c in self.children:
            if c.id == child.id:
                children = children.append(child)
            else:
                children = children.append(c)

        return App(self.id, children, self.items_id, self.search_params_id)
