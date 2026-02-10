"""Text entry view and view-model binding to a `Property`."""

from ...core import Property
from .base import ViewModel, View
import tkinter as tk


class EntryViewModel(ViewModel):
    """View-model that wraps a `Property[str]` for an entry widget."""

    def __init__(self, text: Property[str]):
        self.text = text
        super().__init__(EntryView(self))


class EntryView(View[EntryViewModel]):
    """Render a tkinter `Entry` bound bidirectionally to `text`."""

    def draw(self, parent: tk.Misc) -> tk.Widget:
        text = tk.StringVar(parent, self.vm.text.value)
        text.trace_add("write", lambda *_: self.vm.text.update(text.get()))
        self.vm.text.subscribe(text.set)

        return tk.Entry(parent, textvariable=text)
