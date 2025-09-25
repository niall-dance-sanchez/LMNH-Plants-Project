"""Script to insert new readings data into SQL Server."""

import pyodbc


def get_reading_tuples(data: list[dict]) -> list[tuple]:
    """
    Takes a list of data from the transform stage, and returns
    a list of tuples containing data about each reading transaction.
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
