import tkinter
from lost_and_found.state.model import SearchParamsModel
from lost_and_found.ui import EntryViewModel
from lost_and_found.state import App, Hierarchy


def main() -> None:
    hierarchy = Hierarchy(App.new())

    model = SearchParamsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.search_params)
    )

    view_model = EntryViewModel(model.name)

    root = tkinter.Tk()

    view_model.view.draw(root).pack()

    root.mainloop()
