"""Horizontal list helpers for arranging children left-to-right."""

from .base import View, ViewModel
import tkinter as tk


class HorizontalListViewModel(ViewModel):
    """View-model holding child view-models arranged horizontally."""

    def __init__(self, *children: ViewModel):
        self._children = children
        super().__init__(HorizontalListView(self))


class HorizontalListView(View[HorizontalListViewModel]):
    """Render child view-models using tkinter's `pack` side="left"."""

    def draw(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent)

        for child in self.vm._children:
            child.draw(frame).pack(side="left")

        return frame
