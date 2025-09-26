# pylint: skip-file

import pytest


@pytest.fixture
def cleaned_data():
    return [
        {
            'plant_id': 8,
            'name': 'Bird of paradise',
            'temperature': 16.3483444707664,
            'origin_location': {
                'city': 'Edwardfurt',
                'country': 'Liberia'
            },
            'botanist': {
                'name': 'Bradford Mitchell Dvm',
                'email': 'bradford.mitchell.dvm@lnhm.co.uk'
            },
            'last_watered': "2025-9-22 13:33:20",
            'soil_moisture': 31.7511122641509,
            'recording_taken': "2025-9-23 09:39:03"
        },
        {
            'plant_id': 5,
            'name': 'Flowery flower',
            'temperature': 44.3483444707664,
            'origin_location': {
                'city': 'Edwardfurt',
                'country': 'Liberia'
            },
            'botanist': {
                'name': 'Bradford Mitchell Dvm',
                'email': 'bradford.mitchell.dvm@lnhm.co.uk'
            },
            'last_watered': "2025-9-19 13:33:20",
            'soil_moisture': 51.7511122641509,
            'recording_taken': "2025-9-21 09:39:03"
        }
    ]


@pytest.fixture
def readings():
    return [
        (8, 16.3483444707664, 31.7511122641509,
         '2025-9-22 13:33:20', '2025-9-23 09:39:03'),
        (5, 44.3483444707664, 51.7511122641509,
         '2025-9-19 13:33:20', '2025-9-21 09:39:03')
    ]


@pytest.fixture
def incoming_data():
    return [
        {"data": "some data", "plant_id": 1},
        {"data": "other data", "plant_id": 2},
        {"data": "more data", "plant_id": 3},
        {"data": "lots of data", "plant_id": 4},
        {"data": "informative data", "plant_id": 5},
        {"data": "dkhddsada", "plant_id": 6},
        {"data": "hi", "plant_id": 7},
        {"data": "done", "plant_id": 8}
    ]


@pytest.fixture
def existing_ids():
    return [2, 3, 5, 8]
