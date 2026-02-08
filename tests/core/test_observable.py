from lost_and_found.core import Property, ValueObservable


class CallableMock[T]:
    def __init__(self):
        self.calls: list[T] = []

    def __call__(self, arg: T):
        self.calls.append(arg)

    def reset(self):
        self.calls.clear()


def test_property_initial_is_value():
    property = Property(initial=4)
    assert property.value == 4


def test_property_update_changes_value():
    property = Property(initial=4)
    property.update(5)
    assert property.value == 5


def test_property_calls_subscriber_on_subscribe():
    property = Property(initial=4)

    subscriber = CallableMock()
    property.subscribe(subscriber)

    assert len(subscriber.calls) == 1
    assert subscriber.calls[0] == 4


def test_property_calls_subscriber_on_update():
    property = Property(initial=4)

    subscriber = CallableMock()
    property.subscribe(subscriber)
    subscriber.reset()

    property.update(5)
    assert subscriber.calls == [5]

    property.update(6)
    assert subscriber.calls == [5, 6]


def test_mapped_property_calls_subscriber_on_subscribe():
    property = Property(initial=4)
    doubled = property.map(lambda value: value * 2)

    subscriber = CallableMock()
    doubled.subscribe(subscriber)

    assert subscriber.calls == [8]


def test_mapped_property_calls_subscriber_on_property_update():
    property = Property(initial=4)
    doubled = property.map(lambda value: value * 2)

    subscriber = CallableMock()
    doubled.subscribe(subscriber)
    subscriber.reset()

    property.update(5)
    assert subscriber.calls == [10]

    property.update(6)
    assert subscriber.calls == [10, 12]


def test_filtered_property_calls_subscriber_on_update_that_meets_predicate():
    property = Property(initial=4)
    even = property.filter(lambda x: x % 2 == 0)

    subscriber = CallableMock()
    even.subscribe(subscriber)

    property.update(5)
    assert subscriber.calls == []

    property.update(6)
    assert subscriber.calls == [6]


def test_filtered_property_with_initial_value_calls_subscriber_on_subscribe():
    property = Property(initial=4)
    even = property.filter(lambda x: x % 2 == 0).start_with(0)

    subscriber = CallableMock()
    even.subscribe(subscriber)

    assert subscriber.calls == [0]


def test_filtered_property_with_initial_value_calls_subscriber_on_update():
    property = Property(initial=4)
    even = property.filter(lambda x: x % 2 == 0).start_with(0)

    subscriber = CallableMock()
    even.subscribe(subscriber)
    subscriber.reset()

    property.update(5)
    assert subscriber.calls == []

    property.update(6)
    assert subscriber.calls == [6]


def test_combined_property_calls_subscriber_correctly():
    a = Property(initial=4)
    b = Property(initial=5)
    combined = ValueObservable.combine(a, b)

    subscriber = CallableMock()
    combined.subscribe(subscriber)

    assert subscriber.calls == [(4, 5)]

    a.update(6)
    assert subscriber.calls == [(4, 5), (6, 5)]

    b.update(7)
    assert subscriber.calls == [(4, 5), (6, 5), (6, 7)]
