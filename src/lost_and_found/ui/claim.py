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


class ClaimItemsViewModel(DialogViewModel):
    def __init__(
        self, hierarchy: Hierarchy[Entity], items: ImmutableList[Item]
    ) -> None:
        self.email: Property[str] = Property[str]("")
        self._hierarchy: Hierarchy[Entity] = hierarchy
        self._items: ImmutableList[Item] = items

        super().__init__(
            "Claim Items",
            GridViewModel(
                (LabelViewModel("Your email:"), EntryViewModel(self.email)),
            ),
        )

    def validate(self) -> bool:
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
                item.claim(
                    datetime.now(),
                    self.email.value.strip(),
                )
            )
