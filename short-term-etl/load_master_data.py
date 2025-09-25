"""Helper script that detects for new master data and loads it to the database."""
from os import environ as ENV
from dotenv import load_dotenv

import pyodbc


# from [transform file] import [cleaned data]


def get_db_connection():
    """Connects to the SQL Server database."""

    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    return pyodbc.connect(conn_str)


def check_max_plant_id(data: list[dict]) -> int:
    """Checks the maximum plant id found in a list of dictionaries 
    and returns the value as in integer."""
    return max(data, key=lambda x: x["plant_id"])


def has_new_data(transformed_data: list[dict], rds_data: list[dict]) -> bool:
    """Checks if the transformed data contains new entries when compared to the master rds data."""
    if check_max_plant_id(transformed_data) > check_max_plant_id(rds_data):
        return True
    return False 


def check_species_exists_in_species_table(conn: pyodbc.Connection, species_name: str) -> int | None:
    """Returns the species_id if the species_name already exists in the table."""
    with conn.cursor() as cur:
        query = f"""
                SELECT species_id
                FROM delta.species
                WHERE species_name = {species_name}
                """
        cur.execute(query)
        species_id = cur.fetchone()
    
    return species_id[0] if species_id is not None else None


def check_country_exists_in_country_table(conn: pyodbc.Connection, country_name: str) -> int | None:
    """Returns the country_id if the country_name already exists in the table."""
    with conn.cursor() as cur:
        query = f"""
                SELECT country_id
                FROM delta.country
                WHERE country_name = {country_name}
                """
        cur.execute(query)
        country_id = cur.fetchone()

    return country_id[0] if country_id is not None else None


def check_city_exists_in_city_table(conn: pyodbc.Connection, city_name: str) -> int:
    """Returns the city_id if the city_name already exists in the table."""
    with conn.cursor() as cur:
        query = f"""
                SELECT city_id
                FROM delta.city
                WHERE country_name = {city_name}
                WHERE city_name = {city_name}
        cur.execute(query)
        city_id = cur.fetchone()

    return city_id


def check_botanist_exists_in_botanist_table(conn: pyodbc.Connection, botanist_email: str) -> int | None:
    """Returns the botanist_id if the botanist_email already exists in the table."""
    with conn.cursor() as cur:
        query = f"""
                SELECT botanist_id
                FROM delta.botanist
                WHERE botanist_email = {botanist_email}
                """
        cur.execute(query)
        botanist_id = cur.fetchone()

    return botanist_id
    return botanist_id[0] if botanist_id is not None else None

def insert_species_into_species_table(conn: pyodbc.Connection, species_name: str):
    """Inserts data into the species table."""
    with conn.cursor() as cur:
        query = f"""
                INSERT INTO delta.species
                    (species_name)
                OUTPUT INSERTED.species_id
                VALUES
                    (?)
                """
        cur.execute(query, (species_name,))
        conn.commit()


def insert_country_into_country_table(conn: pyodbc.Connection, country_name: str):
    """Inserts data into the country table."""
    with conn.cursor() as cur:
        query = f"""
                INSERT INTO delta.country
                    (country_name)
                OUTPUT INSERTED.country_id
                VALUES
                    (?)
                """
        cur.execute(query, (country_name,))
        conn.commit()


def insert_city_into_city_table(conn: pyodbc.Connection, city_name: str):
    """Inserts data into the city table."""
    with conn.cursor() as cur:
        query = f"""
                INSERT INTO delta.city
                    (city_name)
                OUTPUT INSERTED.city_id
                VALUES
                    (?)
                """
        cur.execute(query, (city_name,))
        conn.commit()


def insert_botanist_into_botanist_table(conn: pyodbc.Connection, botanist_name: str, botanist_email: str):
    """Inserts data into the botanist table."""
    with conn.cursor() as cur:
        query = f"""
                INSERT INTO delta.botanist
                    (botanist_name, botanist_email)
                OUTPUT INSERTED.botanist_id
                VALUES
                    (?, ?)
                """
        cur.execute(query, (botanist_name, botanist_email,))
        conn.commit()


def insert_plant_into_plant_table(conn: pyodbc.Connection, plant_id: int, species_id: int, country_id: int, city_id: int, botanist_id: int):
    """Inserts data into the plant table."""
    with conn.cursor() as cur:
        query = f"""
                INSERT INTO delta.plant
                    (plant_id, species_id, country_id, city_id, botanist_id)
                VALUES
                    (?, ?, ?, ?, ?)
                """
        cur.execute(query, (plant_id, species_id, country_id, city_id, botanist_id,))
        conn.commit()


def load_master_data(conn: pyodbc.Connection, data: dict):
    """Loads new master data into the database if new data is found."""
    # Check "static" tables and insert when data isn't found
    plant_id = data["plant_id"]

    species_id = check_species_exists_in_species_table(conn, data["name"])
    if not species_id:
        species_id = insert_species_into_species_table(conn, data["name"])
    
    country_id = check_country_exists_in_country_table(conn, data["origin_location"]["country"]) 
    if not country_id:
        country_id = insert_country_into_country_table(conn, data["origin_location"]["country"])

    city_id = check_city_exists_in_city_table(conn, data["origin_location"]["city"])
    if not city_id:    
        city_id = insert_city_into_city_table(conn, data["origin_location"]["city"])

    botanist_id = check_botanist_exists_in_botanist_table(conn, data["botanist"]["name"], 
                                               data["botanist"]["email"])
    if not botanist_id:
        botanist_id = insert_botanist_into_botanist_table(conn, data["botanist"]["name"],
                                            data["botanist"]["email"])

    insert_plant_into_plant_table(conn, plant_id, species_id, country_id, city_id, botanist_id)



if __name__ == "__main__":
    pass



