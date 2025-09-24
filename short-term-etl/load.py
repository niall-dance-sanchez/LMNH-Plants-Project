from os import environ as ENV

import pyodbc
from dotenv import load_dotenv

from insert_transactional_data import insert_transactional_data


def dummy_load_master_data(data: list[dict], con: pyodbc.Connection):
    """Dummy function for the detection/insertion of new master data."""
    pass


def get_connection() -> pyodbc.Connection:
    """Get connection to SQL Server DB."""
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
    return pyodbc.connect(conn_str)


def load_cleaned_data(data: list[dict], con: pyodbc.Connection) -> None:
    """Completes the Load stage of the ETL using two helper scripts."""
    # Insert any new detected master data
    dummy_load_master_data(data, con)
    # Insert the reading transaction data
    insert_transactional_data(data, con)


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
