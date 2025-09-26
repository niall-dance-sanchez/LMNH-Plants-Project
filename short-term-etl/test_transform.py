# pylint: skip-file

import pytest

from transform import (
    clean_plant_id,
    clean_plant_name
)


def test_clean_plant_id_correct_type_and_value(raw_data):
    plant_id = clean_plant_id(raw_data)
    assert plant_id == raw_data["plant_id"]


def test_clean_plant_id_incorrect_type(raw_data):
    bad_data = raw_data
    bad_data["plant_id"] = "test"
    with pytest.raises(ValueError) as exc_info:
        clean_plant_id(bad_data)
        assert "Invalid plant id type" in exc_info.value


def test_clean_plant_id_incorrect_value(raw_data):
    bad_data = raw_data
    bad_data["plant_id"] = -1
    with pytest.raises(ValueError) as exc_info:
        clean_plant_id(bad_data)
        assert "Invalid plant id" in exc_info.value


def test_clean_plant_name_correct_type(raw_data):
    plant_name = clean_plant_name(raw_data)
    assert plant_name in raw_data["name"]


def test_clean_plant_name_bad_type(raw_data):
    bad_data = raw_data
    bad_data["name"] = 101
    with pytest.raises(ValueError) as exc_info:
        clean_plant_name(bad_data)
        assert "Invalid name type" in exc_info.value
