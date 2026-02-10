from .db import (
    CategoryConverter,
    DatetimeConverter,
    FileDatabase,
    ItemsTable,
)


def main() -> None:
    import tkinter

    from .state import App, AppModel, Hierarchy
    from .ui import AppViewModel

    db = FileDatabase("app.db")
    db.register_converter(CategoryConverter)
    db.register_converter(DatetimeConverter)
    db.add_table(ItemsTable)

    hierarchy = Hierarchy(App.new())
    model = AppModel(hierarchy, hierarchy.observable)

    db.replicate_table_to(ItemsTable, model.items)

    root = tkinter.Tk()
    AppViewModel(model).draw(root).pack()
    root.mainloop()
