from .base import View, ViewModel
import tkinter as tk


class GridViewModel(ViewModel):
    def __init__(self, *rows: tuple[ViewModel, ...]) -> None:
        self._rows = rows
        super().__init__(GridView(self))


class GridView(View[GridViewModel]):
    def draw(self, parent: tk.Misc) -> tk.Frame:
        frame = tk.Frame(parent)

        for row, children in enumerate(self.vm._rows):
            for column, child in enumerate(children):
                child.draw(frame).grid(row=row, column=column)

        return frame
