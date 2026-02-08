from .base import View, ViewModel
import tkinter as tk


class HorizontalListViewModel(ViewModel):
    def __init__(self, *children: ViewModel):
        self._children = children
        super().__init__(HorizontalListView(self))


class HorizontalListView(View[HorizontalListViewModel]):
    def draw(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent)

        for child in self.vm._children:
            child.draw(frame).pack(side="left")

        return frame
