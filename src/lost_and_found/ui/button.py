from typing import Optional
from ..core import Trigger, Observable, ValueObservable
from .base import View, ViewModel
import tkinter as tk


class ButtonViewModel(ViewModel):
    def __init__(
        self, text: str, enabled: Optional[ValueObservable[bool]] = None
    ) -> None:
        self._text = text
        self._on_click: Trigger[tuple[()]] = Trigger[tuple[()]]()
        self._enabled: Optional[ValueObservable[bool]] = enabled
        super().__init__(ButtonView(self))

    @property
    def on_click(self) -> Observable[tuple[()]]:
        return self._on_click


class ButtonView(View[ButtonViewModel]):
    def draw(self, parent: tk.Misc) -> tk.Button:
        button = tk.Button(
            parent, text=self.vm._text, command=lambda: self.vm._on_click.trigger(())
        )

        if self.vm._enabled is not None:
            self.vm._enabled.subscribe(
                lambda enabled: button.config(state="normal" if enabled else "disabled")
            )

        return button
