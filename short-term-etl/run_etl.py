"""ETL script designed to be run inside an AWS Lambda function as a container."""

from os import environ as ENV
from datetime import datetime, timedelta

import pyodbc
from dotenv import load_dotenv

from extract import extract_all_plant_data
from transform import clean_data
from load import load_cleaned_data


def get_connection() -> pyodbc.Connection:
    """Get connection to SQL Server DB."""
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
    return pyodbc.connect(conn_str)


def remove_readings_past_24_hours(conn: pyodbc.Connection) -> None:
    """Removes readings in the SQL server that are > 24 hours old"""
    previous_24_hours = datetime.now() - timedelta(hours=24)
    query = """
        DELETE FROM reading
        WHERE recording_taken < ?
    """
    with conn.cursor() as cur:
        cur.execute(query, (previous_24_hours,))


def lambda_handler(event, context):
    """Runs the short-term ETL process."""
    load_dotenv()
    raw_data = extract_all_plant_data()
    cleaned_data = clean_data(data=raw_data)
    conn = get_connection()
    remove_readings_past_24_hours(conn)
    load_cleaned_data(data=cleaned_data, con=conn)
    conn.close()
