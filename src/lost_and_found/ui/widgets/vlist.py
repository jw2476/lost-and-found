from .base import View, ViewModel
import tkinter as tk


class VerticalListViewModel(ViewModel):
    def __init__(self, *children: ViewModel):
        self._children = children
        super().__init__(VerticalListView(self))


class VerticalListView(View[VerticalListViewModel]):
    def draw(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent)

        for child in self.vm._children:
            child.draw(frame).pack(side="top")

        return frame
