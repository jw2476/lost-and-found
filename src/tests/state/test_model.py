from datetime import datetime
from lost_and_found.core import ImmutableList
from lost_and_found.state import (
    SearchParamsModel,
    Hierarchy,
    App,
    Item,
    ItemsModel,
    Category,
)


class CallableMock[T]:
    def __init__(self):
        self.calls: list[T] = []

    def __call__(self, arg: T):
        self.calls.append(arg)

    def reset(self):
        self.calls.clear()


def lost_item(name: str) -> Item:
    return Item.create_lost_item(
        name, Category.BOOKS, datetime.now(), "owner@test.com"
    )


def test_search_params_model_name_updates_on_hierarchy_update():
    hierarchy = Hierarchy[App](App.new())
    params = hierarchy.root.search_params

    model = SearchParamsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.search_params)
    )

    assert model.name.value == ""

    subscriber = CallableMock[str]()
    model.name.subscribe(subscriber)
    assert subscriber.calls == [""]

    hierarchy.update(params.update_name("Shoe"))
    assert model.name.value == "Shoe"
    assert subscriber.calls == ["", "Shoe"]

    model.name.update("Boot")
    assert model.name.value == "Boot"
    assert subscriber.calls == ["", "Shoe", "Boot"]


def test_search_params_model_name_no_update_on_same_value():
    hierarchy = Hierarchy[App](App.new())
    model = SearchParamsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.search_params)
    )

    subscriber = CallableMock[str]()
    model.name.subscribe(subscriber)
    subscriber.reset()

    model.name.update("Shoe")
    assert model.name.value == "Shoe"
    assert subscriber.calls == ["Shoe"]

    model.name.update("Shoe")
    assert model.name.value == "Shoe"
    assert subscriber.calls == ["Shoe"]


def test_items_model_search_filters_items():
    hierarchy = Hierarchy[App](App.new())
    search_params = SearchParamsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.search_params)
    )
    items = ItemsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.items)
    )

    items.append(lost_item("Shoe"))
    items.append(lost_item("Boot"))

    search_results = items.search(search_params)
    assert len(search_results.value) == 2
    assert search_results.value[0].name == "Shoe"
    assert search_results.value[1].name == "Boot"

    search_params.name.update("Sh")
    assert len(search_results.value) == 1
    assert search_results.value[0].name == "Shoe"


def test_items_model_search_no_update_on_same_value():
    hierarchy = Hierarchy[App](App.new())
    search_params = SearchParamsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.search_params)
    )
    items = ItemsModel(
        hierarchy, hierarchy.observable.map(lambda app: app.items)
    )

    items.append(lost_item("Shoe"))
    items.append(lost_item("Boot"))

    search_results = items.search(search_params)
    assert len(search_results.value) == 2

    subscriber = CallableMock[ImmutableList[Item]]()
    search_results.subscribe(subscriber)

    search_params.name.update("Shoe")
    subscriber.reset()
    search_params.name.update("Shoe")
    assert subscriber.calls == []
