from lost_and_found.core.observable import Property
from abc import ABC, abstractmethod
import tkinter as tk


class View[T: ViewModel](ABC):
    def __init__(self, vm: T) -> None:
        self.vm = vm

    @abstractmethod
    def draw(self, parent: tk.Misc) -> tk.Widget:
        pass


class ViewModel(ABC):
    def __init__(self, view: View):
        self.view: View[ViewModel] = view


class EntryViewModel(ViewModel):
    def __init__(self, text: Property[str]):
        self.text = text
        super().__init__(EntryView(self))


class EntryView(View[EntryViewModel]):
    def draw(self, parent: tk.Misc) -> tk.Widget:
        text = tk.StringVar(parent, self.vm.text.value)
        text.trace_add("write", lambda *_: self.vm.text.update(text.get()))
        self.vm.text.subscribe(text.set)

        return tk.Entry(parent, textvariable=text)
