"""View model for adding a found item via a dialog."""

import re
from datetime import datetime
from ..core import Property
from ..state import ItemsModel, Category, Item
import tkinter.messagebox as msg
from .widgets import (
    DialogViewModel,
    EntryViewModel,
    GridViewModel,
    LabelViewModel,
    OptionMenuViewModel,
)


class AddFoundItemViewModel(DialogViewModel):
    """Dialog view-model for creating a new found `Item`."""

    def __init__(self, items: ItemsModel) -> None:
        self.name: Property[str] = Property[str]("")
        self.category: Property[Category] = Property[Category](Category.BOOKS)
        self.location: Property[str] = Property[str]("")
        self.email: Property[str] = Property[str]("")
        self._items: ItemsModel = items

        super().__init__(
            "Add Found Item",
            GridViewModel(
                (LabelViewModel("Name:"), EntryViewModel(self.name)),
                (
                    LabelViewModel("Category:"),
                    OptionMenuViewModel(
                        self.category,
                        lambda category: category.value,
                        *[category for category in Category],
                    ),
                ),
                (LabelViewModel("Location:"), EntryViewModel(self.location)),
                (LabelViewModel("Your email:"), EntryViewModel(self.email)),
            ),
        )

    def validate(self) -> bool:
        name = self.name.value.strip()
        if not name:
            msg.showerror("Input Error", "Item name cannot be empty.")
            return False

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
        self._items.append(
            Item.create_found_item(
                self.name.value,
                self.category.value,
                datetime.now(),
                self.location.value,
                self.email.value,
            )
        )
