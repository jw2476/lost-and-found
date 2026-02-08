from tkinter.simpledialog import Dialog
import tkinter
from ..core import Property
from ..state import ItemsModel, Category
from .base import View, ViewModel
from .button import ButtonView, ButtonViewModel
from .entry import EntryView, EntryViewModel
from .grid import GridView, GridViewModel
from .hlist import HorizontalListView, HorizontalListViewModel
from .label import LabelView, LabelViewModel
from .table import TableView, TableViewModel
import tkinter as tk

__all__ = [
    "View",
    "ViewModel",
    "ButtonView",
    "ButtonViewModel",
    "EntryView",
    "EntryViewModel",
    "GridView",
    "GridViewModel",
    "HorizontalListView",
    "HorizontalListViewModel",
    "LabelView",
    "LabelViewModel",
    "TableView",
    "TableViewModel",
    "AddLostItemViewModel",
]


class DialogViewModel(ViewModel):
    def __init__(self, body: ViewModel) -> None:
        self._body = body
        super().__init__(DialogView(self))


class DialogView(Dialog, View[DialogViewModel]):
    def __init__(self, vm: DialogViewModel) -> None:
        View.__init__(self, vm)
        Dialog.__init__(self, parent=None)

    def body(self, master: tk.Misc) -> tk.Misc:
        return self.draw(master)

    def draw(self, parent: tk.Misc) -> tk.Widget:
        body = self.vm._body.draw(parent)
        body.pack()
        return body


class AddLostItemViewModel(DialogViewModel):
    def __init__(self) -> None:
        self.name: Property[str] = Property[str]("")
        self.location: Property[str] = Property[str]("")

        super().__init__(
            GridViewModel(
                (LabelViewModel("Name:"), EntryViewModel(self.name)),
                (LabelViewModel("Location:"), EntryViewModel(self.location)),
            )
        )
