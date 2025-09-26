"""This module configures the LMNH plants dashboard."""
from datetime import datetime

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from data import (start_s3_session,
                  get_db_connection,
                  retrieve_all_summary_plant_data,
                  retrieve_all_live_plant_data)

from live_plant_data_functions import (create_moisture_level_line_graph,
                                       create_temperature_line_graph)
from all_plant_data_functions import (historic_plant_temperature,
                                      historic_plant_moisture,
                                      historic_plant_waterings)



# Create sidebar

def create_sidebar():
    """Creates the sidebar and sets up the tabs"""
    page_options = ["Live Data", "All Plant Data"]

    if "page" not in st.session_state:
        st.session_state.page = "Live Data"

    st.session_state.page = st.sidebar.radio("Currently Viewing", page_options)

    if st.session_state.page == "All Plant Data":
        st.session_state.page = "All Plant Data"


# Create pages from sidebar

def live_data_page(df: pd.DataFrame):
    """The default homepage of the dashboard which shows the live data."""
    # Page Title
    st.title("LMNH Botany Department Dashboard")
    st.header("Live Dashboard")

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PLACEHOLDER PLANT NUMBER
    plant_number = df["plant_id"].nunique()

    plant_id_list = df["plant_id"].unique()

    st.divider()

    # Set up for plant count and date/time at top of page
    with st.container(border=True, height=108):
        st.multiselect(
            label=":seedling: Plants: :seedling:", options=plant_id_list, default=plant_id_list)

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

    # Set up graphs
    st.altair_chart(create_moisture_level_line_graph(df, plant_id_list))

    st.altair_chart(create_temperature_line_graph(df, plant_id_list))



def all_plant_data_page(df: pd.DataFrame):
    """A selectable tab of the dashboard which shows all stored plant data."""
    # Page Title
    st.title("LMNH Botany Department Dashboard")
    st.header("All Plant Data")


    plant_id_list = df["plant_id"].unique()

    # Set up for plant count and date/time at top of page
    with st.container(border=True, height=108):
        st.multiselect(
            label=":seedling: Plants: :seedling:", options=plant_id_list, default=[1, 2, 3])

    st.divider()

    start_date = st.date_input(
        "Start Date:", value="2025-09-19")
    end_date = st.date_input("End Date: ", value="today")
    # Set up columns for graphs
    st.altair_chart(historic_plant_temperature(df, start_date, end_date, plant_id_list))


    st.altair_chart(historic_plant_moisture(df, start_date, end_date,plant_id_list))

    st.altair_chart(historic_plant_waterings(df, start_date, end_date, plant_id_list))




if __name__ == "__main__":
    load_dotenv()
    session = start_s3_session()
    conn = get_db_connection()

    live_data = retrieve_all_live_plant_data(conn)
    historic_data = retrieve_all_summary_plant_data("c19-ajldka-lmnh-plants-db", session)

    create_sidebar()
    if st.session_state.page == "Live Data":
        live_data_page(live_data)
    if st.session_state.page == "All Plant Data":
        all_plant_data_page(historic_data)
