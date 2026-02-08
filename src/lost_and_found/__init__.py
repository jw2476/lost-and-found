from .state import SearchParamsModel, ItemsModel, App, Hierarchy, Item
from .ui import (
    EntryViewModel,
    TableViewModel,
    ButtonViewModel,
    LabelViewModel,
    HorizontalListViewModel,
)


def main() -> None:
    import tkinter

    hierarchy = Hierarchy(App.new())
    hierarchy.update(hierarchy.root.items.append(Item.new("Shoe")))

    root = tkinter.Tk()

    search_params = SearchParamsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.search_params)
    )

    search_name_entry = EntryViewModel(search_params.name)

    HorizontalListViewModel(LabelViewModel("Name:"), search_name_entry).draw(
        root
    ).pack()

    items = ItemsModel(hierarchy, hierarchy.observable.map(lambda app: app.items))
    items_table = TableViewModel(
        ("Name",),
        items.search(search_params),
        lambda item: (
            str(item.id.id),
            item.name,
        ),
    )
    items_table.draw(root).pack()

    add_button = ButtonViewModel("Add")
    add_button.on_click.subscribe(lambda _: items.append(Item.new("Boot")))

    delete_button = ButtonViewModel(
        "Delete", enabled=items_table.selected.map(lambda selected: len(selected) != 0)
    )
    delete_button.on_click.subscribe(
        lambda _: items.remove_all(items_table.selected.value)
    )

    HorizontalListViewModel(add_button, delete_button).draw(root).pack()

    root.mainloop()
