from typing import Callable
from .base import View, ViewModel
from ...core import Property
import tkinter as tk


class OptionMenuViewModel[T](ViewModel):
    def __init__(
        self,
        selected: Property[T],
        formatter: Callable[[T], str],
        *options: T,
    ):
        self.selected: Property[T] = selected
        self._formatter: Callable[[T], str] = formatter
        self._options: tuple[T, ...] = options

        super().__init__(OptionMenuView(self))


class OptionMenuView[T](View[OptionMenuViewModel[T]]):
    def draw(self, parent: tk.Misc) -> tk.OptionMenu:
        selected = tk.StringVar(
            parent, self.vm._formatter(self.vm.selected.value)
        )
        self.vm.selected.map(self.vm._formatter).subscribe(selected.set)

        selected.trace_add(
            "write", lambda *_: self._update_selected(selected.get())
        )

        menu = tk.OptionMenu(
            parent,
            selected,
            *[self.vm._formatter(option) for option in self.vm._options],
        )

        return menu

    def _update_selected(self, value: str) -> None:
        for option in self.vm._options:
            if value == self.vm._formatter(option):
                self.vm.selected.update(option)
