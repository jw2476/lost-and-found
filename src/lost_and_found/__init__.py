from lost_and_found.ui import AddLostItemViewModel
from datetime import datetime


def main() -> None:
    import tkinter

    from .state import SearchParamsModel, ItemsModel, App, Hierarchy, Item, Category
    from .ui import (
        EntryViewModel,
        TableViewModel,
        ButtonViewModel,
        LabelViewModel,
        HorizontalListViewModel,
    )

    hierarchy = Hierarchy(App.new())

    root = tkinter.Tk()

    search_params = SearchParamsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.search_params)
    )

    search_name_entry = EntryViewModel(search_params.name)

    HorizontalListViewModel(LabelViewModel("Name:"), search_name_entry).draw(
        root
    ).pack()

    def item_values(item: Item) -> tuple[str, ...]:
        return (
            str(item.id.id),
            item.name,
            str(item.category.value),
            item.location if item.location else "-",
            item.finder_email if item.finder_email else "-",
            item.owner_email if item.owner_email else "-",
        )

    items = ItemsModel(hierarchy, hierarchy.observable.map(lambda app: app.items))
    items_table = TableViewModel(
        ("Name", "Category", "Location", "Finder", "Owner"),
        items.search(search_params),
        item_values,
    )
    items_table.draw(root).pack()

    add_button = ButtonViewModel("Add")
    add_button.on_click.subscribe(lambda _: AddLostItemViewModel())

    delete_button = ButtonViewModel(
        "Delete", enabled=items_table.selected.map(lambda selected: len(selected) != 0)
    )
    delete_button.on_click.subscribe(
        lambda _: items.remove_all(items_table.selected.value)
    )

    HorizontalListViewModel(add_button, delete_button).draw(root).pack()

    root.mainloop()
