"""Tests for functions created in the load_master_data file."""

from load_master_data import (check_max_plant_id, has_new_data)


def test_check_max_plant_id_returns_int():
    """Test to check if max plant id function returns an integer value."""
    id = check_max_plant_id([{"plant_id": 1}, {"plant_id": 2}, {"plant_id": 3}])
    assert isinstance(id, int) == True


def test_check_has_new_data_returns_bool():
    """Test to check if has new data function returns bool."""
    assert has_new_data([{"plant_id": 1}, {"plant_id": 2}, {"plant_id": 3}, {"plant_id": 4}], [
                        {"plant_id": 1}, {"plant_id": 2}, {"plant_id": 3}]) == True
    assert has_new_data([{"plant_id": 1}, {"plant_id": 2}], [
                        {"plant_id": 1}, {"plant_id": 2}, {"plant_id": 3}]) == False


