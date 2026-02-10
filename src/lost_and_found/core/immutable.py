from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator

"""Immutable collection helpers.

This module provides simple immutable collection types used across the
application. Implementations are lightweight and intentionally minimal so
they are easy to reason about and test.
"""


@dataclass(frozen=True)
class ImmutableList[T]:
    """An immutable, tuple-backed list-like container.

    `ImmutableList` stores its items in a tuple and returns new
    instances on mutations such as `append` and `remove`.
    """

    value: tuple[T, ...] = ()

    def append(self, value: T) -> ImmutableList[T]:
        """Return a new `ImmutableList` with `value` appended.

        The original instance is not modified.
        """
        return ImmutableList((*self.value, value))

    def remove(self, value: T) -> ImmutableList[T]:
        """Return a new `ImmutableList` with all occurrences of `value` removed."""
        return ImmutableList(
            tuple(item for item in self.value if item != value)
        )

    def __len__(self) -> int:
        """Return the number of items in the list."""
        return len(self.value)

    def __getitem__(self, key: int) -> T:
        """Return the item at `key` (supports indexing)."""
        return self.value[key]

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the items."""
        return self.value.__iter__()

    def __eq__(self, other: Any) -> bool:
        """Equality comparison with another `ImmutableList`."""
        return isinstance(other, ImmutableList) and self.value == other.value
