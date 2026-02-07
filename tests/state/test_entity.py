from lost_and_found.core import ImmutableList
from lost_and_found.state import Item, Entity, App, ListEntity, Hierarchy


class CallableMock[T]:
    def __init__(self):
        self.calls: list[T] = []

    def __call__(self, arg: T):
        self.calls.append(arg)

    def reset(self):
        self.calls.clear()


def test_item_new():
    item = Item.new("Shoe")

    assert item.children == ImmutableList[Entity]()
    assert item.name == "Shoe"


def test_list_entity_new():
    items = ListEntity[Item].new()

    assert items.items == ImmutableList[Item]()


def test_list_entity_append():
    items = ListEntity[Item].new()
    items = items.append(Item.new("Shoe"))

    assert [item.name for item in items.items] == ["Shoe"]


def test_list_entity_update_child():
    items = ListEntity[Item].new()
    items = items.append(Item.new("Shoe"))
    items = items.update_child(items.items[0].update_name("Boot"))

    assert [item.name for item in items.items] == ["Boot"]


def test_hierarchy_update():
    app = App.new()
    hierarchy = Hierarchy[App](app)

    item = Item.new("Shoe")
    hierarchy.update(app.items.append(item))

    assert [item.name for item in hierarchy.root.items.items] == ["Shoe"]

    hierarchy.update(item.update_name("Boot"))
    assert [item.name for item in hierarchy.root.items.items] == ["Boot"]


def test_hierarchy_observable():
    app = App.new()
    hierarchy = Hierarchy[App](app)

    subscriber = CallableMock()
    hierarchy.observable.subscribe(subscriber)
    assert subscriber.calls == [app]

    item = Item.new("Shoe")
    hierarchy.update(app.items.append(item))
    assert subscriber.calls == [app, hierarchy.root]
