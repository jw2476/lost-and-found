from .base import View, ViewModel
import tkinter as tk


class LabelViewModel(ViewModel):
    def __init__(self, text: str):
        self._text = text
        super().__init__(LabelView(self))


class LabelView(View[LabelViewModel]):
    def draw(self, parent: tk.Misc) -> tk.Label:
        return tk.Label(parent, text=self.vm._text)
