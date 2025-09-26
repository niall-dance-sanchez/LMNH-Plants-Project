"""Tests for insert_transactional_data.py."""

from insert_transactional_data import get_reading_tuples


def test_get_reading_tuples_regular_record_data(cleaned_data, readings):
    """Just test readings are extract correctly from the dummy data."""
    reading_tuples = get_reading_tuples(data=cleaned_data)
    assert reading_tuples == readings


def test_get_reading_tuples_singleton_data(cleaned_data, readings):
    """Test readings returned when data only has one record."""
    singleton_data = [cleaned_data[1]]
    reading_tuples = get_reading_tuples(data=singleton_data)
    assert reading_tuples == [readings[1]]


def test_get_reading_tuples_empty_data():
    """Make sure an empty list is returned when data is empty."""
    reading_tuples = get_reading_tuples([])
    assert len(reading_tuples) == 0


def test_get_reading_tuples_all_tuples(cleaned_data):
    """Test all objects in the returned readings and make sure they're all tuples."""
    reading_tuples = get_reading_tuples(data=cleaned_data)
    assert all(isinstance(reading, tuple) for reading in reading_tuples)
