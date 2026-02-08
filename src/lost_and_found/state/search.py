from __future__ import annotations
from ..core import ImmutableList
from .entity import Entity, EntityId
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchParams(Entity):
    name: str

    @staticmethod
    def new() -> SearchParams:
        return SearchParams(EntityId.new(), ImmutableList(), "")

    def update_child(self, child: Entity) -> SearchParams:
        return self

    def update_name(self, name: str) -> SearchParams:
        return SearchParams(self.id, self.children, name)
