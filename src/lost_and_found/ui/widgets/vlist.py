"""Vertical list helpers for stacking child view-models top-to-bottom."""

from .base import View, ViewModel
import tkinter as tk


class VerticalListViewModel(ViewModel):
    """View-model holding children arranged vertically."""

    def __init__(self, *children: ViewModel):
        self._children = children
        super().__init__(VerticalListView(self))


class VerticalListView(View[VerticalListViewModel]):
    """Render child view-models using tkinter's `pack` side="top"."""

    def draw(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent)

        for child in self.vm._children:
            child.draw(frame).pack(side="top")

        return frame
