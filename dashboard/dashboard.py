"""This module configures the LMNH plants dashboard."""
from os import environ as ENV
from datetime import datetime

import boto3
import streamlit as st
import pandas as pd
import awswrangler as wr
from dotenv import load_dotenv

# Start Boto3 Session to get the data


def start_boto3_session():
    """Starts a boto3 session."""
    session = boto3.Session(
        aws_access_key_id=ENV["AWS_ACCESS_KEY_AJLDKA"],
        aws_secret_access_key=ENV["AWS_SECRET_KEY_AJLDKA"],
        region_name=ENV["AWS_REGION_AJLDKA"]
    )
    return session


@st.cache_data
def load_data_from_athena():
    """Function that loads data from the plants database using Athena."""
    query = "SELECT * FROM plant;" # Create big query for all data here
    session = start_boto3_session()

    data = wr.athena.read_sql_query(
        query, database=ENV["DB_NAME"], boto3_session=session)

    return data


# Sidebar

def create_sidebar():
    """Creates the sidebar and sets up the tabs"""
    page_options = ["Live Data", "All Plant Data"]

    if "page" not in st.session_state:
        st.session_state.page = "Live Data"

    st.session_state.page = st.sidebar.radio("Currently Viewing", page_options)

    if st.session_state.page == "All Plant Data":
        st.session_state.page = "All Plant Data"




# Pages from Sidebar

def live_data_page():#conn: Connection, live_plant_data: list[str]):
    """The default homepage of the dashboard which shows the live data."""
    # Page Title
    st.title("LMNH Botany Department Dashboard")
    st.header("Live Dashboard")

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PLACEHOLDER PLANT NUMBER
    plant_number = 50

    # Set up for plant count and date/time at top of page
    left_text, right_text = st.columns(2)
    with left_text:
        with st.container(border=True, height=108):
            st.metric(label=":hibiscus: Total number of plants: :hibiscus:", value=plant_number)
    with right_text:
        with st.container(border=True):
            st.metric(label="Current date and time:", value=current_datetime)

    # Separate the plant count and current date/time from the graphical
    # data
    st.divider()

    # Set up columns for graphs
    left_col, right_col = st.columns(2)
    with left_col:
        pass # Insert first graph (function to be made)

    with right_col:
        pass # Insert second graph (function to be made)



def all_plant_data_page():  # conn: Connection, live_plant_data: list[str]):
    """A secectable tab of the dashboard which shows all stored plant data."""
    # Page Title
    st.title("LMNH Botany Department Dashboard")
    st.header("All Plant Data")

    # PLACEHOLDER REPLACE WITH ACTUAL PLANT LIST
    plant_list = ["Aglaonema Commutatum", "Aloe Vera", "Amaryllis",
                  "Anthurium", "Araucaria Heterophylla", "Asclepias Curassavica",
                  "Begonia", "Bird of paradise", "Black bat flower"
                  "Brugmansia X Candida", "Cactus"]

    # Set up for plant count and date/time at top of page
    with st.container(border=True, height=108):
        st.multiselect(
            label=":seedling: Plants: :seedling:", options=plant_list, default=plant_list)

    st.divider()

    start_date = st.date_input("Start Date:", value=None)

    end_date = st.date_input("End Date: ", value=None)

    # Set up columns for graphs
    left_col, right_col = st.columns(2)
    with left_col:
        pass  # Insert first graph (function to be made)

    with right_col:
        pass  # Insert second graph (function to be made)




if __name__ == "__main__":
    load_dotenv()

    # print(load_data_from_athena())
    create_sidebar()
    if st.session_state.page == "Live Data":
        live_data_page()
    if st.session_state.page == "All Plant Data":
        all_plant_data_page()