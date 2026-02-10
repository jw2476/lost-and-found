"""Dialog view-model for marking multiple items as found."""

import re
import tkinter.messagebox as msg
from datetime import datetime

from ..core import ImmutableList, Property
from ..state import Entity, Hierarchy, Item
from .widgets import (
    DialogViewModel,
    EntryViewModel,
    GridViewModel,
    LabelViewModel,
)


class MarkItemsAsFoundViewModel(DialogViewModel):
    """Collects location and contact info and marks provided items as found."""

    def __init__(
        self, hierarchy: Hierarchy[Entity], items: ImmutableList[Item]
    ) -> None:
        self.location: Property[str] = Property[str]("")
        self.email: Property[str] = Property[str]("")
        self._hierarchy: Hierarchy[Entity] = hierarchy
        self._items: ImmutableList[Item] = items

        super().__init__(
            "Mark Items as Found",
            GridViewModel(
                (LabelViewModel("Location:"), EntryViewModel(self.location)),
                (LabelViewModel("Your email:"), EntryViewModel(self.email)),
            ),
        )

    def validate(self) -> bool:
        location = self.location.value.strip()
        if not location:
            msg.showerror("Input Error", "Location cannot be empty.")
            return False

        email = self.email.value.strip()
        if not email:
            msg.showerror("Input Error", "Your email cannot be empty.")
            return False

        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            msg.showerror(
                "Input Error", "Your email must be a valid email address."
            )
            return False

        return True

    def apply(self) -> None:
        for item in self._items:
            self._hierarchy.update(
                item.mark_as_found(
                    datetime.now(),
                    self.location.value.strip(),
                    self.email.value.strip(),
                )
            )
