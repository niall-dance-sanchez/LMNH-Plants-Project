"""Tests for functions created in the load_master_data file."""

from load_master_data import is_new_master_data

incoming_data = [
    {"data": "some data", "plant_id": 1},
    {"data": "other data", "plant_id": 2},
    {"data": "more data", "plant_id": 3},
    {"data": "lots of data", "plant_id": 4},
    {"data": "informative data", "plant_id": 5},
    {"data": "dkhddsada", "plant_id": 6},
    {"data": "hi", "plant_id": 7},
    {"data": "done", "plant_id": 8}
]
existing_ids = [2, 3, 5, 8]


def test_is_new_master_data_new_data():
    """Test that only new master data is returned when present."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert all(record["plant_id"] not in existing_ids for record in new_data)


def test_is_new_master_data_new_data_matches():
    """Assert that the new master data returned actually matches what was given."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert all(record in incoming_data for record in new_data)


def test_is_new_master_data_new_data_contains_dicts():
    """Ensure the new data is returned as dictionaries."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert all(isinstance(record, dict) for record in new_data)


def test_is_new_master_data_new_data_is_list():
    """Ensure new data is passed back as a list."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert isinstance(new_data, list)


def test_is_new_master_data_no_new_data():
    """Test that new_data is None when there is no new master data."""
    all_ids = list(range(1, 9))
    new_data = is_new_master_data(incoming_data, all_ids)
    assert new_data is None
