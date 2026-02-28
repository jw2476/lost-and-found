from datetime import datetime

from lost_and_found.db import (
    DatetimeConverter,
    CategoryConverter,
    ItemsTable,
    Database,
    InMemoryDatabase,
)
from lost_and_found.state import (
    App,
    AppModel,
    Hierarchy,
    Item,
    Category,
    ItemsModel,
)


def setup() -> tuple[Database, ItemsModel]:
    db: Database = InMemoryDatabase()
    db.register_converter(DatetimeConverter)
    db.register_converter(CategoryConverter)
    db.add_table(ItemsTable)

    hierarchy: Hierarchy[App] = Hierarchy[App](App.new())
    app: AppModel = AppModel(hierarchy, hierarchy.observable)
    items: ItemsModel = app.items

    db.replicate_table_to(ItemsTable, items)

    return db, items


def test_replicator_seeds_model_from_table():
    db, items = setup()
    assert len(items.items.value) == 0

    # Create an item, this should be added to the DB
    item: Item = Item.create_found_item(
        "Phone",
        Category.ELECTRONICS,
        datetime.now(),
        "Library",
        "finder@example.com",
    )
    items.append(item)

    # Create a new app hierarchy, simulates closing and reopening the app
    new_hierarchy = Hierarchy[App](App.new())
    new_app = AppModel(new_hierarchy, new_hierarchy.observable)
    new_items = new_app.items

    # Setup second replication, this should be seeded with the
    # newly created item
    db.replicate_table_to(ItemsTable, new_items)

    assert len(new_items.items.value) == 1
    assert new_items.items.value[0] == item


def test_replicator_updates_table_on_change():
    db, items = setup()
    assert len(items.items.value) == 0

    # Create an item, this should be added to the DB
    item: Item = Item.create_found_item(
        "Phone",
        Category.ELECTRONICS,
        datetime.now(),
        "Library",
        "finder@example.com",
    )
    items.append(item)

    # Update the item, the change should cause the DB to update
    item = item.claim(datetime.now(), "owner@example.com")
    items.hierarchy.update(item)

    # Create a new app hierarchy, simulates closing and reopening the app
    new_hierarchy = Hierarchy[App](App.new())
    new_app = AppModel(new_hierarchy, new_hierarchy.observable)
    new_items = new_app.items

    # Setup second replication, this should be seeded with the
    # newly updated item
    db.replicate_table_to(ItemsTable, new_items)

    assert len(new_items.items.value) == 1
    assert new_items.items.value[0] == item
