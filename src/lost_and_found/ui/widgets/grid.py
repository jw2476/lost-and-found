"""Grid layout helpers for composing views in rows/columns."""

from .base import View, ViewModel
import tkinter as tk


class GridViewModel(ViewModel):
    """View-model holding rows of child view-models for a grid layout."""

    def __init__(self, *rows: tuple[ViewModel, ...]) -> None:
        self._rows = rows
        super().__init__(GridView(self))


class GridView(View[GridViewModel]):
    """Render child view-models into a grid using tkinter's `grid`."""

    def draw(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent)

        for row, children in enumerate(self.vm._rows):
            for column, child in enumerate(children):
                child.draw(frame).grid(row=row, column=column)

        return frame
