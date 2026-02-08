from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Any


@dataclass(frozen=True)
class ImmutableList[T]:
    value: tuple[T, ...] = ()

    def append(self, value: T) -> ImmutableList[T]:
        return ImmutableList((*self.value, value))

    def remove(self, value: T) -> ImmutableList[T]:
        return ImmutableList(
            tuple(item for item in self.value if item != value)
        )

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, key: int) -> T:
        return self.value[key]

    def __iter__(self) -> Iterator[T]:
        return self.value.__iter__()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ImmutableList) and self.value == other.value
