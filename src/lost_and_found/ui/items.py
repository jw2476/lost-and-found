"""View models composing the main items UI.

This module wires smaller view-model widgets into the top-level
`ItemsViewModel` used by the UI to present and operate on `Item` entities.
"""

from ..state import ItemsModel, SearchParamsModel
from ..ui.claim import ClaimItemsViewModel
from .add_found_item import AddFoundItemViewModel
from .add_lost_item import AddLostItemViewModel
from .mark_as_found import MarkItemsAsFoundViewModel
from .widgets import (
    ButtonViewModel,
    HorizontalListViewModel,
    TableViewModel,
    VerticalListViewModel,
)


class ItemsViewModel(VerticalListViewModel):
    """Composes table and action button view models for the items screen."""

    def __init__(
        self, items: ItemsModel, search_params: SearchParamsModel
    ) -> None:
        table = TableViewModel(
            ("Name", "Category", "Location", "Finder", "Owner"),
            items.search(search_params),
            lambda item: (
                str(item.id.id),
                item.name,
                str(item.category.value),
                item.location if item.location else "-",
                item.finder_email if item.finder_email else "-",
                item.owner_email if item.owner_email else "-",
            ),
        )

        add_lost_item_button = ButtonViewModel("Add Lost Item")
        add_found_item_button = ButtonViewModel("Add Found Item")
        delete_button = ButtonViewModel(
            "Delete",
            enabled=table.selected.map(lambda selected: len(selected) != 0),
        )
        mark_items_as_found_button = ButtonViewModel(
            "Mark Item as Found",
            enabled=table.selected.map(
                lambda selected: (
                    len(selected) != 0
                    and all([item.found is None for item in selected])
                )
            ),
        )
        claim_items_button = ButtonViewModel(
            "Claim Items",
            enabled=table.selected.map(
                lambda selected: (
                    len(selected) != 0
                    and all([item.found is not None for item in selected])
                    and all([item.claimed is None for item in selected])
                )
            ),
        )

        add_lost_item_button.on_click.subscribe(
            lambda _: AddLostItemViewModel(items)
        )
        add_found_item_button.on_click.subscribe(
            lambda _: AddFoundItemViewModel(items)
        )
        delete_button.on_click.subscribe(
            lambda _: items.remove_all(table.selected.value)
        )
        mark_items_as_found_button.on_click.subscribe(
            lambda _: MarkItemsAsFoundViewModel(
                items.hierarchy, table.selected.value
            )
        )
        claim_items_button.on_click.subscribe(
            lambda _: ClaimItemsViewModel(
                items.hierarchy, table.selected.value
            )
        )

        super().__init__(
            table,
            HorizontalListViewModel(
                add_lost_item_button,
                add_found_item_button,
                delete_button,
                mark_items_as_found_button,
                claim_items_button,
            ),
        )
