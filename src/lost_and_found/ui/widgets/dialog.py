from tkinter.simpledialog import Dialog
from abc import abstractmethod
from .base import View, ViewModel
import tkinter as tk


class DialogViewModel(ViewModel):
    def __init__(self, title: str, body: ViewModel) -> None:
        self._title = title
        self._body = body
        super().__init__(DialogView(self))

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def apply(self) -> None:
        pass


class DialogView(Dialog, View[DialogViewModel]):
    def __init__(self, vm: DialogViewModel) -> None:
        View.__init__(self, vm)
        Dialog.__init__(self, parent=None, title=self.vm._title)

    def body(self, master: tk.Misc) -> tk.Misc:
        return self.draw(master)

    def draw(self, parent: tk.Misc) -> tk.Widget:
        body = self.vm._body.draw(parent)
        body.pack()
        return body

    def validate(self) -> bool:
        return self.vm.validate()

    def apply(self) -> None:
        self.vm.apply()
