from __future__ import annotations
from typing import Callable
from abc import abstractmethod
import abc


class Observable[T](abc.ABC):
    @abstractmethod
    def subscribe(self, subscriber: Callable[[T], None]) -> None:
        pass

    def start_with(self, initial: T) -> ValueObservable[T]:
        property: Property[T] = Property(initial)
        self.subscribe(property.update)
        return property

    def filter(self, predicate: Callable[[T], bool]) -> Observable[T]:
        return ObservableFilter(self, predicate)


class ValueObservable[T](Observable[T]):
    @property
    @abstractmethod
    def value(self) -> T:
        pass

    def map[TResult](
        self, transform: Callable[[T], TResult]
    ) -> ValueObservable[TResult]:
        mapped: Property[TResult] = Property(transform(self.value))
        self.subscribe(lambda new_value: mapped.update(transform(new_value)))
        return mapped

    def on_change_only(self) -> ValueObservable[T]:
        changes_only = Property[T](self.value)
        self.filter(
            lambda new_value: new_value != changes_only.value
        ).subscribe(changes_only.update)
        return changes_only

    @staticmethod
    def combine[TA, TB](
        a: ValueObservable[TA], b: ValueObservable[TB]
    ) -> ValueObservable[tuple[TA, TB]]:
        combined = Property((a.value, b.value))

        a.subscribe(lambda new_a: combined.update((new_a, combined.value[1])))
        b.subscribe(lambda new_b: combined.update((combined.value[0], new_b)))

        return combined


class ObservableFilter[T](Observable[T]):
    def __init__(self, parent: Observable[T], predicate: Callable[[T], bool]):
        self._parent: Observable[T] = parent
        self._predicate: Callable[[T], bool] = predicate
        self._subscribers: list[Callable[[T], None]] = []

        self._parent.subscribe(self._on_parent_update)

    def _on_parent_update(self, new_value: T) -> None:
        if self._predicate(new_value):
            for subscriber in self._subscribers:
                subscriber(new_value)

    def subscribe(self, subscriber: Callable[[T], None]) -> None:
        self._subscribers.append(subscriber)


class Property[T](ValueObservable[T]):
    def __init__(self, initial: T):
        self._value: T = initial
        self._subscribers: list[Callable[[T], None]] = []

    def subscribe(self, subscriber: Callable[[T], None]) -> None:
        subscriber(self._value)
        self._subscribers.append(subscriber)

    @property
    def value(self) -> T:
        return self._value

    def update(self, new_value: T) -> None:
        self._value: T = new_value
        for subscriber in self._subscribers:
            subscriber(self._value)


class Trigger[T](Observable[T]):
    def __init__(self) -> None:
        self._subscribers: list[Callable[[T], None]] = []

    def subscribe(self, subscriber: Callable[[T], None]) -> None:
        self._subscribers.append(subscriber)

    def trigger(self, value: T) -> None:
        for subscriber in self._subscribers:
            subscriber(value)
