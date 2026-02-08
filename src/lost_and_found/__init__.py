def main() -> None:
    import tkinter

    from .state import App, Hierarchy, AppModel
    from .ui import AppViewModel

    hierarchy = Hierarchy(App.new())
    model = AppModel(hierarchy, hierarchy.observable)

    root = tkinter.Tk()
    AppViewModel(model).draw(root).pack()
    root.mainloop()
