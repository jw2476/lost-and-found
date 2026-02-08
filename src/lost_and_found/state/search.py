from __future__ import annotations
from typing import Optional
from ..core import ImmutableList
from .entity import Entity, EntityId
from .item import Category
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchParams(Entity):
    name: str
    category: Optional[Category]

    @staticmethod
    def new() -> SearchParams:
        return SearchParams(EntityId.new(), ImmutableList(), name="", category=None)

    def update_child(self, child: Entity) -> SearchParams:
        return self

    def update_name(self, name: str) -> SearchParams:
        return SearchParams(self.id, self.children, name, self.category)

    def update_category(self, category: Optional[Category]) -> SearchParams:
        return SearchParams(self.id, self.children, self.name, category)
