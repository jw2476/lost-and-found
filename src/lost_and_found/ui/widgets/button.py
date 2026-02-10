"""Button widget view-model and view."""

from typing import Optional
from ...core import Trigger, Observable, ValueObservable
from .base import View, ViewModel
import tkinter as tk


class ButtonViewModel(ViewModel):
    """View-model representing a button and its enabled state."""

    def __init__(
        self, text: str, enabled: Optional[ValueObservable[bool]] = None
    ) -> None:
        self._text = text
        self._on_click: Trigger[tuple[()]] = Trigger[tuple[()]]()
        self._enabled: Optional[ValueObservable[bool]] = enabled
        super().__init__(ButtonView(self))

    @property
    def on_click(self) -> Observable[tuple[()]]:
        """Observable that emits when the button is clicked."""
        return self._on_click


class ButtonView(View[ButtonViewModel]):
    """Render a tkinter `Button` wired to the view-model."""

    def draw(self, parent: tk.Misc) -> tk.Button:
        button = tk.Button(
            parent,
            text=self.vm._text,
            command=lambda: self.vm._on_click.trigger(()),
        )

        if self.vm._enabled is not None:
            self.vm._enabled.subscribe(
                lambda enabled: button.config(
                    state="normal" if enabled else "disabled"
                )
            )

        return button
