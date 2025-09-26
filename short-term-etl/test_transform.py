# pylint: skip-file

import pytest

from transform import (
    clean_plant_id,
    clean_plant_name,
    clean_temperature,
    clean_origin_location
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


def test_clean_temperature_correct_value(raw_data):
    temperature = clean_temperature(raw_data)
    assert temperature == raw_data["temperature"]


def test_clean_temperature_bad_type(raw_data):
    bad_data = raw_data
    bad_data["temperature"] = True
    with pytest.raises(ValueError) as exc_info:
        clean_temperature(bad_data)
        assert "Invalid temperature type" in exc_info.value


def test_clean_temperature_bad_value(raw_data):
    bad_data = raw_data
    bad_data["temperature"] = -33.3
    with pytest.raises(ValueError) as exc_info:
        clean_temperature(bad_data)
        assert "Invalid temperature value" in exc_info.value


def test_clean_origin_location_correct_value(raw_data):
    origin_data = clean_origin_location(raw_data)
    assert origin_data["city"] in raw_data["origin_location"]["city"]
    assert origin_data["country"] in raw_data["origin_location"]["country"]


def test_clean_origin_location_bad_city_type(raw_data):
    bad_data = raw_data
    bad_data["origin_location"]["city"] = 101
    with pytest.raises(ValueError) as exc_info:
        clean_origin_location(bad_data)
        assert "Invalid city value" in exc_info.value


def test_clean_origin_location_bad_country_type(raw_data):
    bad_data = raw_data
    bad_data["origin_location"]["country"] = 101
    with pytest.raises(ValueError) as exc_info:
        clean_origin_location(bad_data)
        assert "Invalid country value" in exc_info.value
