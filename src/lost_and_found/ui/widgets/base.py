"""Basic view and view-model base classes for UI widgets."""

from abc import ABC, abstractmethod
import tkinter as tk


class View[T: ViewModel](ABC):
    """Base class for views that render a `ViewModel`.

    Subclasses should implement `draw` to construct tkinter widgets under a
    provided parent and return the created widget.
    """

    def __init__(self, vm: T) -> None:
        self.vm = vm

    @abstractmethod
    def draw(self, parent: tk.Misc) -> tk.Widget:
        pass


class ViewModel(ABC):
    """Base class for view-models that hold presentation logic."""

    def __init__(self, view: View):
        self.view: View[ViewModel] = view

    def draw(self, parent: tk.Misc) -> tk.Widget:
        return self.view.draw(parent)
