from .db import FileDatabase, CategoryConverter, DatetimeConverter, ItemsTable


def main() -> None:
    import tkinter

    from .state import App, Hierarchy, AppModel
    from .ui import AppViewModel

    db = FileDatabase("app.db")
    db.register_converter(CategoryConverter)
    db.register_converter(DatetimeConverter)
    db.add_table(ItemsTable)

    hierarchy = Hierarchy(App.new())
    model = AppModel(hierarchy, hierarchy.observable)

    root = tkinter.Tk()
    AppViewModel(model).draw(root).pack()
    root.mainloop()
