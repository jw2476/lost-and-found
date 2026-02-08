from ..state import ItemsModel, SearchParamsModel
from .widgets import (
    VerticalListViewModel,
    TableViewModel,
    ButtonViewModel,
    HorizontalListViewModel,
)
from .add_lost_item import AddLostItemViewModel
from .add_found_item import AddFoundItemViewModel


class ItemsViewModel(VerticalListViewModel):
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

        add_lost_item_button.on_click.subscribe(
            lambda _: AddLostItemViewModel(items)
        )
        add_found_item_button.on_click.subscribe(
            lambda _: AddFoundItemViewModel(items)
        )
        delete_button.on_click.subscribe(
            lambda _: items.remove_all(table.selected.value)
        )

        super().__init__(
            table,
            HorizontalListViewModel(
                add_lost_item_button, add_found_item_button, delete_button
            ),
        )
