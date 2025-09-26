"""Functions to connect and retrieve the plant data."""

from os import environ as ENV
import awswrangler as wr
import pandas as pd
import boto3
import streamlit as st


@st.cache_resource
def start_s3_session() -> boto3.Session:
    """Establishes an s3 connection."""

    return boto3.Session(
        aws_access_key_id=ENV["AWS_ACCESS_KEY_AJLDKA"],
        aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY_AJLDKA"],
        region_name="eu-west-2"
    )


@st.cache_data
def retrieve_all_summary_truck_data(database: str, _session: boto3.Session) -> pd.DataFrame:
    """Retrieve all of the truck data."""

    query = """
            SELECT *
            FROM c19_ajldka_lmnh_plants
            ;
            """

    return wr.athena.read_sql_query(
        query,
        database=database,
        boto3_session=_session)


@st.cache_data
def retrieve_all_live_plant_data(con) -> list[dict]:
    """Extract all relevant (dropping unnecessary ids) plant data from the RDS."""

    with con.cursor() as cur:
        query = """
                SELECT 
                    delta.plant.plant_id,
                    delta.species.species_name,
                    delta.country.country_name,
                    delta.city.city_name,
                    delta.reading.temperature,
                    delta.reading.soil_moisture,
                    delta.reading.last_watered,
                    delta.reading.recording_taken,
                    delta.botanist.botanist_name,
                    delta.botanist.botanist_email
                FROM delta.plant
                JOIN delta.species ON delta.plant.species_id = delta.species.species_id
                JOIN delta.country ON delta.plant.country_id = delta.country.country_id
                JOIN delta.city ON delta.plant.city_id = delta.city.city_id
                JOIN delta.reading ON delta.plant.plant_id = delta.reading.plant_id
                JOIN delta.botanist ON delta.plant.botanist_id = delta.botanist.botanist_id
                ;
                """
        cur.execute(query)
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in cur.fetchall()]

    return data
