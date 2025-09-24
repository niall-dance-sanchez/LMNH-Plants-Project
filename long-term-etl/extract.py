"""
"""

from os import environ as ENV

from dotenv import load_dotenv
import pyodbc


def get_db_connection():

    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    return pyodbc.connect(conn_str)


if __name__ == "__main__":
    load_dotenv()

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            query = "SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"
            cur.execute(query)
            data = cur.fetchone()

    print(data)
