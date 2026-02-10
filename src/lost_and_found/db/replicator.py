from abc import ABC
from typing import Optional

from lost_and_found.core import ImmutableList

from ..state import Entity, EntityId, ListModel
from .tables import Table


class Replicator[T: Entity](ABC):
    def __init__(self, model: ListModel[T], table: Table[T]) -> None:
        self.table = table
        self.previous: Optional[ImmutableList[T]] = None

        model.set(table.select_all())
        model.items.subscribe(self.on_change)

    def on_change(self, values: ImmutableList[T]) -> None:
        if self.previous is not None:
            inserted, updated, deleted = Replicator[T].diff(
                self.previous, values
            )

            for value in inserted:
                self.table.insert(value)

            for value in updated:
                self.table.update(value)

            for value in deleted:
                self.table.delete(value)

        self.previous: ImmutableList[T] = values

    @staticmethod
    def diff(
        previous: ImmutableList[T], current: ImmutableList[T]
    ) -> tuple[ImmutableList[T], ImmutableList[T], ImmutableList[T]]:
        previous_ids_to_entities: dict[EntityId, T] = dict(
            [(x.id, x) for x in previous]
        )
        current_ids_to_entities: dict[EntityId, T] = dict(
            [(x.id, x) for x in current]
        )
        previous_ids: list[EntityId] = list(previous_ids_to_entities.keys())
        current_ids: list[EntityId] = list(current_ids_to_entities.keys())
        ids: set[EntityId] = set([*previous_ids, *current_ids])

        inserted: ImmutableList[T] = ImmutableList[T](())
        updated: ImmutableList[T] = ImmutableList[T](())
        deleted: ImmutableList[T] = ImmutableList[T](())

        for id in ids:
            if id not in previous_ids and id in current_ids:
                inserted = inserted.append(current_ids_to_entities[id])
            elif id in previous_ids and id not in current_ids:
                deleted = deleted.append(previous_ids_to_entities[id])
            else:  # In both
                if (
                    previous_ids_to_entities[id]
                    is not current_ids_to_entities[id]
                ):
                    updated = updated.append(current_ids_to_entities[id])

        return inserted, updated, deleted
