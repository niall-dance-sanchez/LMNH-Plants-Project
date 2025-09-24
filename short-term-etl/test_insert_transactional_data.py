from insert_transactional_data import get_reading_tuples

# TODO: Ideally this would be in a conftest.py, but since
# we haven't got many tests yet I'll just keep it simple
# and add it as a global. Should be removed when we have
# a proper test suite and added to to conftest.py instead
dummy_data = [
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
readings = [
    (8, 16.3483444707664, 31.7511122641509,
     '2025-9-22 13:33:20', '2025-9-23 09:39:03'),
    (5, 44.3483444707664, 51.7511122641509,
     '2025-9-19 13:33:20', '2025-9-21 09:39:03')
]


def test_get_reading_tuples_regular_record_data():
    """Just test readings are extract correctly from the dummy data."""
    reading_tuples = get_reading_tuples(data=dummy_data)
    assert reading_tuples == readings


def test_get_reading_tuples_singleton_data():
    """Test readings returned when data only has one record."""
    singleton_data = [dummy_data[1]]
    reading_tuples = get_reading_tuples(data=singleton_data)
    assert reading_tuples == [readings[1]]


def test_get_reading_tuples_empty_data():
    """Make sure an empty list is returned when data is empty."""
    reading_tuples = get_reading_tuples([])
    assert len(reading_tuples) == 0


def test_get_reading_tuples_all_tuples():
    """Test all objects in the returned readings and make sure they're all tuples."""
    reading_tuples = get_reading_tuples(data=dummy_data)
    assert all(isinstance(reading, tuple) for reading in reading_tuples)
