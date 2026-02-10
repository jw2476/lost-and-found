"""Simple label view and view-model."""

from .base import View, ViewModel
import tkinter as tk


class LabelViewModel(ViewModel):
    """View-model for a static text label."""

    def __init__(self, text: str):
        self._text = text
        super().__init__(LabelView(self))


class LabelView(View[LabelViewModel]):
    """Render a tkinter `Label` with the provided text."""

    def draw(self, parent: tk.Misc) -> tk.Label:
        return tk.Label(parent, text=self.vm._text)
