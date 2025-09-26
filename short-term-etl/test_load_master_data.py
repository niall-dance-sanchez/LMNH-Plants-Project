"""Tests for functions created in the load_master_data file."""

from load_master_data import is_new_master_data


def test_is_new_master_data_new_data(incoming_data, existing_ids):
    """Test that only new master data is returned when present."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert all(record["plant_id"] not in existing_ids for record in new_data)


def test_is_new_master_data_new_data_matches(incoming_data, existing_ids):
    """Assert that the new master data returned actually matches what was given."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert all(record in incoming_data for record in new_data)


def test_is_new_master_data_new_data_contains_dicts(incoming_data, existing_ids):
    """Ensure the new data is returned as dictionaries."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert all(isinstance(record, dict) for record in new_data)


def test_is_new_master_data_new_data_is_list(incoming_data, existing_ids):
    """Ensure new data is passed back as a list."""
    new_data = is_new_master_data(incoming_data, existing_ids)
    assert isinstance(new_data, list)


def test_is_new_master_data_no_new_data(incoming_data):
    """Test that new_data is None when there is no new master data."""
    all_ids = list(range(1, 9))
    new_data = is_new_master_data(incoming_data, all_ids)
    assert new_data is None
