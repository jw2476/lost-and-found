"""Table view backed by a `ValueObservable` of rows."""

from typing import Callable, cast, Any
import tkinter as tk
import tkinter.ttk as ttk
from ...core import ValueObservable, ImmutableList, Property
from .base import View, ViewModel


class TableViewModel[T](ViewModel):
    """View-model exposing table headers, rows and selected items."""

    def __init__(
        self,
        headers: tuple[str, ...],
        rows: ValueObservable[ImmutableList[T]],
        formatter: Callable[[T], tuple[str, ...]],
    ) -> None:
        self._headers: tuple[str, ...] = headers
        self._rows: ValueObservable[ImmutableList[T]] = rows
        self._formatter: Callable[[T], tuple[str, ...]] = formatter
        self.selected = Property[ImmutableList[T]](ImmutableList[T]())

        super().__init__(TableView(self))


class TableView[T](View[TableViewModel[T]]):
    """Render a `ttk.Treeview` and keep selection in sync with
    the view-model."""

    def draw(self, parent: tk.Misc) -> ttk.Treeview:
        treeview = ttk.Treeview(
            parent,
            show="headings",
            columns=[i for i in range(0, len(self.vm._headers) + 1)],
            displaycolumns=[i for i in range(1, len(self.vm._headers) + 1)],
        )
        self.vm._rows.subscribe(lambda rows: self._set_rows(treeview, rows))

        treeview.heading(0, text="id")
        for i, header in enumerate(self.vm._headers):
            treeview.heading(i + 1, text=header)

        treeview.bind(
            "<<TreeviewSelect>>",
            lambda *_: self._update_selection(treeview),
        )

        return treeview

    def _set_rows(
        self, treeview: ttk.Treeview, rows: ImmutableList[T]
    ) -> None:
        treeview.delete(*treeview.get_children())

        for row in rows:
            treeview.insert("", "end", values=self.vm._formatter(row))

        self._set_selected(treeview, self.vm.selected.value)

    def _set_selected(
        self, treeview: ttk.Treeview, selected: ImmutableList[T]
    ) -> None:
        treeview.selection_clear()

        rows = [
            (child, cast(tuple[Any, ...], treeview.item(child, "values")))
            for child in treeview.get_children()
        ]

        for selected_row in selected:
            for row_id, row_values in rows:
                if row_values[0] == self.vm._formatter(selected_row)[0]:
                    treeview.selection_add(row_id)

    def _update_selection(self, treeview: ttk.Treeview) -> None:
        selected = ImmutableList[T](())

        for id in treeview.selection():
            row_values = cast(tuple[str, ...], treeview.item(id, "values"))
            for row in self.vm._rows.value:
                if row_values[0] == self.vm._formatter(row)[0]:
                    selected = selected.append(row)

        self.vm.selected.update(selected)
