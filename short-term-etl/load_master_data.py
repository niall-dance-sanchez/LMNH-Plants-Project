"""Helper script that detects for new master data and loads it to the database."""

import pyodbc


def check_species_exists_in_species_table(conn: pyodbc.Connection, species_name: str) -> int | None:
    """Returns the species_id if the species_name already exists in the table."""
    with conn.cursor() as cur:
        query = """
                SELECT species_id
                FROM delta.species
                WHERE species_name = ?
                """
        cur.execute(query, (species_name,))
        species_id = cur.fetchone()

    return species_id[0] if species_id is not None else None


def check_country_exists_in_country_table(conn: pyodbc.Connection, country_name: str) -> int | None:
    """Returns the country_id if the country_name already exists in the table."""
    with conn.cursor() as cur:
        query = """
                SELECT country_id
                FROM delta.country
                WHERE country_name = ?
                """
        cur.execute(query, (country_name,))
        country_id = cur.fetchone()

    return country_id[0] if country_id is not None else None


def check_city_exists_in_city_table(conn: pyodbc.Connection, city_name: str) -> int | None:
    """Returns the city_id if the city_name already exists in the table."""
    with conn.cursor() as cur:
        query = """
                SELECT city_id
                FROM delta.city
                WHERE city_name = ?
                """
        cur.execute(query, (city_name,))
        city_id = cur.fetchone()

    return city_id[0] if city_id is not None else None


def check_botanist_exists_in_botanist_table(
        conn: pyodbc.Connection, botanist_email: str) -> int | None:
    """Returns the botanist_id if the botanist_email already exists in the table."""
    with conn.cursor() as cur:
        query = """
                SELECT botanist_id
                FROM delta.botanist
                WHERE botanist_email = ?
                """
        cur.execute(query, (botanist_email,))
        botanist_id = cur.fetchone()

    return botanist_id[0] if botanist_id is not None else None


def insert_species_into_species_table(conn: pyodbc.Connection, species_name: str) -> int:
    """Inserts data into the species table."""
    with conn.cursor() as cur:
        query = """
                INSERT INTO delta.species
                    (species_name)
                OUTPUT INSERTED.species_id
                VALUES
                    (?)
                """
        cur.execute(query, (species_name,))
        new_id = cur.fetchone()[0]

    conn.commit()
    return new_id


def insert_country_into_country_table(conn: pyodbc.Connection, country_name: str) -> int:
    """Inserts data into the country table."""
    with conn.cursor() as cur:
        query = """
                INSERT INTO delta.country
                    (country_name)
                OUTPUT INSERTED.country_id
                VALUES
                    (?)
                """
        cur.execute(query, (country_name,))
        new_id = cur.fetchone()[0]

    conn.commit()
    return new_id


def insert_city_into_city_table(conn: pyodbc.Connection, city_name: str) -> int:
    """Inserts data into the city table."""
    with conn.cursor() as cur:
        query = """
                INSERT INTO delta.city
                    (city_name)
                OUTPUT INSERTED.city_id
                VALUES
                    (?)
                """
        cur.execute(query, (city_name,))
        new_id = cur.fetchone()[0]

    conn.commit()
    return new_id


def insert_botanist_into_botanist_table(
        conn: pyodbc.Connection, botanist_name: str, botanist_email: str) -> int:
    """Inserts data into the botanist table."""
    with conn.cursor() as cur:
        query = """
                INSERT INTO delta.botanist
                    (botanist_name, botanist_email)
                OUTPUT INSERTED.botanist_id
                VALUES
                    (?, ?)
                """
        cur.execute(query, (botanist_name, botanist_email,))
        new_id = cur.fetchone()[0]

    conn.commit()
    return new_id


def insert_plant_into_plant_table(
        conn: pyodbc.Connection, plant_id: int, species_id: int,
        country_id: int, city_id: int, botanist_id: int):
    """Inserts data into the plant table."""
    with conn.cursor() as cur:
        query = """
                INSERT INTO delta.plant
                    (plant_id, species_id, country_id, city_id, botanist_id)
                VALUES
                    (?, ?, ?, ?, ?)
                """
        cur.execute(
            query,
            (plant_id, species_id, country_id, city_id, botanist_id,)
        )

    conn.commit()


def single_load(conn: pyodbc.Connection, data: dict):
    """Loads one record of new master data into the database if new data is found."""
    # Check "static" tables and insert when data isn't found
    plant_id = data["plant_id"]

    species_id = check_species_exists_in_species_table(conn, data["name"])
    if not species_id:
        species_id = insert_species_into_species_table(conn, data["name"])

    country_id = check_country_exists_in_country_table(
        conn, data["origin_location"]["country"])
    if not country_id:
        country_id = insert_country_into_country_table(
            conn, data["origin_location"]["country"])

    city_id = check_city_exists_in_city_table(
        conn, data["origin_location"]["city"])
    if not city_id:
        city_id = insert_city_into_city_table(
            conn, data["origin_location"]["city"])

    botanist_id = check_botanist_exists_in_botanist_table(
        conn, data["botanist"]["email"])
    if not botanist_id:
        botanist_id = insert_botanist_into_botanist_table(conn, data["botanist"]["name"],
                                                          data["botanist"]["email"])

    insert_plant_into_plant_table(
        conn, plant_id, species_id, country_id, city_id, botanist_id)


def return_plant_ids_in_rds(conn: pyodbc.Connection) -> list[int]:
    """Returns a list of all plant IDs currently in the SQL server."""
    with conn.cursor() as cur:
        cur.execute("SELECT plant_id FROM plant")
        plant_ids = cur.fetchall()
    plant_ids = [row[0] for row in plant_ids]
    return plant_ids


def is_new_master_data(data: list[dict], all_plant_ids: list[int]) -> list[dict] | None:
    """
    Checks if there's new master data to be inserted. If so, returns only the
    records with new master data, otherwise returns None.
    """
    new_data = list(filter(lambda r: r["plant_id"] not in all_plant_ids, data))
    if len(new_data) == 0:
        # No new master data
        return None
    return new_data


def load_master_data(conn: pyodbc.Connection, data: list[dict]) -> None:
    """Loads all master data from the records passed in from the transform stage."""
    all_rds_plant_ids = return_plant_ids_in_rds(conn)
    data = is_new_master_data(data, all_rds_plant_ids)

    if data:
        for record in data:
            single_load(conn, data=record)
