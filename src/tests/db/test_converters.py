from datetime import datetime, timezone
import pytest

from lost_and_found.db import DatetimeConverter, CategoryConverter
from lost_and_found.state import Category


def test_datetime_converter_type():
    assert DatetimeConverter.type() is datetime


def test_datetime_converter_roundtrip_naive():
    dt = datetime(2026, 3, 14, 15, 9, 26, 535897)
    s = DatetimeConverter.to_str(dt)
    assert isinstance(s, str)
    back = DatetimeConverter.from_bytes(s.encode())
    assert back == dt


def test_datetime_converter_roundtrip_with_tz():
    dt = datetime(2026, 3, 14, 15, 9, 26, 535897, tzinfo=timezone.utc)
    s = DatetimeConverter.to_str(dt)
    assert dt == DatetimeConverter.from_bytes(s.encode())


def test_category_converter_type():
    assert CategoryConverter.type() is Category


def test_category_converter_roundtrip():
    for category in Category:
        s = CategoryConverter.to_str(category)
        assert category == CategoryConverter.from_bytes(s.encode())


def test_category_converter_invalid():
    with pytest.raises(ValueError):
        CategoryConverter.from_bytes(b"Nonexistent")
