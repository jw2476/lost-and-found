from abc import ABC, abstractmethod
import tkinter as tk


class View[T: ViewModel](ABC):
    def __init__(self, vm: T) -> None:
        self.vm = vm

    @abstractmethod
    def draw(self, parent: tk.Misc) -> tk.Widget:
        pass


class ViewModel(ABC):
    def __init__(self, view: View):
        self.view: View[ViewModel] = view

    def draw(self, parent: tk.Misc) -> tk.Widget:
        return self.view.draw(parent)
