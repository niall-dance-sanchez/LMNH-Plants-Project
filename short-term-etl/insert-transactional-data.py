from os import environ as ENV

from dotenv import load_dotenv
import pyodbc


def get_connection():
    """Get connection to SQL Server DB."""
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
    return pyodbc.connect(conn_str)


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    with conn.cursor() as cur:
        q = "SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"
        cur.execute(q)
        data = cur.fetchone()
    print(data)
    conn.close()
