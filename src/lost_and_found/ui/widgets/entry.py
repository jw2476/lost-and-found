from ...core import Property
from .base import ViewModel, View
import tkinter as tk


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
