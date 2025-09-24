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
    load_dotenv()
    conn = get_connection()
    with conn.cursor() as cur:
        q = "SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"
        cur.execute(q)
        data = cur.fetchone()
    print(data)
    conn.close()
