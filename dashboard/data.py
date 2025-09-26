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
def retrieve_all_truck_data(database: str, _session: boto3.Session) -> pd.DataFrame:
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
