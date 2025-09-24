"""
Script with functions to connect to the RDS and 
extract all of it's data into a single table.
"""

from os import environ as ENV

import pyodbc


def get_db_connection():
    """Connect to the plant database hosted on RDS."""

    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    return pyodbc.connect(conn_str)


def extract_day_of_data(con):
    """Extract all plant data from the RDS."""

    with con.cursor() as cur:
        query = """
                SELECT * 
                FROM delta.plant
                JOIN delta.species ON delta.plant.species_id = delta.species.species_id
                JOIN delta.country ON delta.plant.country_id = delta.country.country_id
                JOIN delta.city ON delta.plant.city_id = delta.city.city_id
                JOIN delta.reading ON delta.plant.plant_id = delta.reading.plant_id
                JOIN delta.botanist ON delta.plant.botanist_id = delta.botanist.botanist_id
                ;
                """
        cur.execute(query)
        data = cur.fetchall()

    return data
