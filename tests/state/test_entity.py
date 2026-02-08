from datetime import datetime
from lost_and_found.core import ImmutableList
from lost_and_found.state import (
    Item,
    App,
    ListEntity,
    Hierarchy,
    Category,
    SearchParams,
)


class CallableMock[T]:
    def __init__(self):
        self.calls: list[T] = []

    def __call__(self, arg: T):
        self.calls.append(arg)

    def reset(self):
        self.calls.clear()


def lost_item(name: str) -> Item:
    return Item.create_lost_item(name, Category.BOOKS, datetime.now(), "owner@test.com")


def test_list_entity_new():
    items = ListEntity[Item].new()

    assert items.items == ImmutableList[Item]()


def test_list_entity_append():
    items = ListEntity[Item].new()
    items = items.append(lost_item("Shoe"))

    assert [item.name for item in items.items] == ["Shoe"]


def test_list_entity_remove_all():
    items = ListEntity[Item].new()
    item1 = lost_item("Shoe")
    item2 = lost_item("Boot")
    items = items.append(item1).append(item2)
    items = items.remove_all(ImmutableList[Item]((item1,)))

    assert [item.name for item in items.items] == ["Boot"]


def test_list_entity_update_child():
    list_entity = ListEntity[SearchParams].new()
    list_entity = list_entity.append(SearchParams.new())
    list_entity = list_entity.update_child(list_entity.items[0].update_name("Boot"))

    assert [item.name for item in list_entity.items] == ["Boot"]


def test_hierarchy_update():
    app = App.new()
    hierarchy = Hierarchy[App](app)

    item = lost_item("Shoe")
    hierarchy.update(app.items.append(item))

    assert [item.finder_email for item in hierarchy.root.items.items] == [None]

    hierarchy.update(item.mark_as_found(datetime.now(), "Library", "finder@test.com"))
    assert [item.finder_email for item in hierarchy.root.items.items] == [
        "finder@test.com"
    ]


def test_hierarchy_observable():
    app = App.new()
    hierarchy = Hierarchy[App](app)

    subscriber = CallableMock()
    hierarchy.observable.subscribe(subscriber)
    assert subscriber.calls == [app]

    item = lost_item("Shoe")
    hierarchy.update(app.items.append(item))
    assert subscriber.calls == [app, hierarchy.root]
