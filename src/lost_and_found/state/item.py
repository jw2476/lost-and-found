from __future__ import annotations
from typing import Optional
from datetime import datetime
from enum import Enum
from ..core import ImmutableList
from .entity import Entity, EntityId
from dataclasses import dataclass

"""Item entity and `Category` enum.

`Item` represents a lost-or-found item tracked by the application and
provides factory methods and convenience operations for common state
transitions such as marking found or claiming an item.
"""


class Category(Enum):
    ELECTRONICS = "Electronics"
    BOOKS = "Books"
    CLOTHING = "Clothing"


@dataclass(frozen=True)
class Item(Entity):
    """Immutable representation of an item in the system."""

    name: str
    category: Category
    lost: datetime
    found: Optional[datetime]
    claimed: Optional[datetime]
    location: Optional[str]
    finder_email: Optional[str]
    owner_email: Optional[str]

    @staticmethod
    def create_lost_item(
        name: str,
        category: Category,
        lost: datetime,
        owner_email: str,
    ) -> Item:
        """
        Create a new lost item.

        :param name: The name of the item
        :type name: str
        :param category: The category of the item
        :type category: Category
        :param lost: The time the item was lost
        :type lost: datetime
        :param owner_email: The email of the item's owner
        :type owner_email: str
        :return: A new `Item` instance representing the lost item
        :rtype: Item
        """

        return Item(
            id=EntityId.new(),
            children=ImmutableList[Entity](()),
            name=name,
            category=category,
            lost=lost,
            found=None,
            claimed=lost,
            location=None,
            finder_email=None,
            owner_email=owner_email,
        )

    @staticmethod
    def create_found_item(
        name: str,
        category: Category,
        found: datetime,
        location: str,
        finder_email: str,
    ) -> Item:
        """
        Create a new found item.

        :param name: The name of the item
        :type name: str
        :param category: The category of the item
        :type category: Category
        :param found: The time the item was found
        :type found: datetime
        :param location: The location where the item was found
        :type location: str
        :param finder_email: The email of the person who found the item
        :type finder_email: str
        :return: A new `Item` instance representing the found item
        :rtype: Item
        """

        return Item(
            id=EntityId.new(),
            children=ImmutableList[Entity](()),
            name=name,
            category=category,
            lost=found,
            found=found,
            claimed=None,
            location=location,
            finder_email=finder_email,
            owner_email=None,
        )

    def mark_as_found(
        self, found: datetime, location: str, finder_email: str
    ) -> Item:
        """
        Mark an item as found. Item must not have been found already.

        :param self: The item to mark as found
        :param found: The time the item was found
        :type found: datetime
        :param location: The location where the item was found
        :type location: str
        :param finder_email: The email of the person who found the item
        :type finder_email: str
        :return: A new `Item` instance representing the found item
        :rtype: Item
        """

        assert self.found is None, "Item has already been found."

        return Item(
            id=self.id,
            children=self.children,
            name=self.name,
            category=self.category,
            lost=self.lost,
            found=found,
            claimed=self.claimed,
            location=location,
            finder_email=finder_email,
            owner_email=self.owner_email,
        )

    def claim(self, claimed: datetime, owner_email: str) -> Item:
        """
        Claim a found item. Item must have been found and not claimed already.

        :param self: The item to claim
        :param claimed: The time the item was claimed
        :type claimed: datetime
        :param owner_email: The email of the person claiming the item
        :type owner_email: str
        :return: A new `Item` instance representing the claimed item
        :rtype: Item
        """

        assert self.found is not None, "Missing item cannot be claimed."
        assert self.claimed is None, "Item has already been claimed."

        return Item(
            id=self.id,
            children=self.children,
            name=self.name,
            category=self.category,
            lost=self.lost,
            found=self.found,
            claimed=claimed,
            location=self.location,
            finder_email=self.finder_email,
            owner_email=owner_email,
        )

    def update_child(self, child: Entity) -> Item:
        return self
