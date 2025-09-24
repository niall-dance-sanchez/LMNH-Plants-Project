"""Script to insert new readings data into SQL Server."""

from os import environ as ENV

from dotenv import load_dotenv
import pyodbc


def get_connection() -> pyodbc.Connection:
    """Get connection to SQL Server DB."""
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
    return pyodbc.connect(conn_str)


def get_reading_tuples(data: list[dict]) -> list[tuple]:
    """
    Takes a list of transformed data, and returns a list of tuples
    containing data about each reading transaction.
    Args:
        data (list[dict]): Data list returned from transform stage.

    Returns:
        list[tuple]: reading data as tuples.
    """
    readings = []
    for record in data:
        reading = (
            record["plant_id"],
            record["temperature"],
            record["soil_moisture"],
            record["last_watered"],
            record["recording_taken"]
        )
        readings.append(reading)
    return readings


def insert_transactional_data(data: list[dict], con: pyodbc.Connection) -> None:
    """Loads readings from cleaned data into SQL Server at `con`."""
    with con.cursor() as cur:
        # Enable fast execute
        cur.fast_executemany = True
        readings = get_reading_tuples(data)
        cur.executemany(
            """
            INSERT INTO reading
                (plant_id, temperature, soil_moisture, last_watered, recording_taken)
            VALUES
                (?, ?, ?, ?, ?)
            """,
            readings
        )


if __name__ == "__main__":
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
    # Check reading tuples are correct
    print(get_reading_tuples(dummy_data))
