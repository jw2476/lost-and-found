from datetime import datetime

from lost_and_found.db import (
    DatetimeConverter,
    CategoryConverter,
    ItemsTable,
    InMemoryDatabase,
)
from lost_and_found.state import Item, Category


def setup():
    db = InMemoryDatabase()
    db.register_converter(DatetimeConverter)
    db.register_converter(CategoryConverter)
    return ItemsTable(db.cursor)


def test_insert_and_select_all_roundtrip():
    items_table = setup()

    found = datetime.now()
    item = Item.create_found_item(
        "Phone", Category.ELECTRONICS, found, "Library", "finder@example.com"
    )

    items_table.insert(item)

    all_items = items_table.select_all()
    assert len(all_items) == 1

    item_in_db = all_items[0]
    assert item_in_db.name == item.name
    assert item_in_db.category == item.category
    assert item_in_db.found == item.found
    assert item_in_db.finder_email == item.finder_email

    pk = items_table.pk(item_in_db.id)
    assert pk == 1


def test_update_item():
    items_table = setup()

    lost = datetime.now()
    item = Item.create_lost_item(
        "Book", Category.BOOKS, lost, "owner@example.com"
    )
    items_table.insert(item)

    found = datetime.now()
    item = item.mark_as_found(found, "Library", "finder@example.com")

    items_table.update(item)

    all_items = items_table.select_all()
    assert len(all_items) == 1
    item_in_db = all_items[0]
    assert item_in_db.found == item.found
    assert item_in_db.location == "Library"
    assert item_in_db.finder_email == "finder@example.com"


def test_delete_item():
    table = setup()

    found = datetime(2023, 4, 4, 4, 4, 4)
    item = Item.create_found_item(
        "Jacket",
        Category.CLOTHING,
        found,
        "Lecture Theatre A",
        "finder@example.com",
    )

    table.insert(item)
    assert len(table.select_all()) == 1

    table.delete(item)
    assert len(table.select_all()) == 0
