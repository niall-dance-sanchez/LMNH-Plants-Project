"""File containing the functions necessary to create graphs for all plant data."""

import streamlit as st
import altair as alt
import pandas as pd



@st.cache_data
def historic_plant_temperature(df: pd.DataFrame, start_date: str,
                               end_date: str, _plant_id_list: list[str]) -> alt.Chart:
    """
    Produces a scatter chart of plant temperature over time
    in a specific date range for selected plant id's.
    """
    df["date"] = pd.to_datetime(
        {"year": df.year, "month": df.month, "day": df.day})
    df = df[["species_name", "plant_id", "avg_temp", "date", "botanist_email"]]
    df = df[df["date"].between(start_date, end_date)]
    mask = df["plant_id"].isin(_plant_id_list)
    df = df[mask]

    start_date = pd.to_datetime(str(start_date)).dt.date
    end_date = pd.to_datetime(str(end_date)).dt.date

    graph = alt.Chart(
        df,
        title=f"Average Plant Temperature: {start_date} - {end_date}"
        ).mark_line(point=True).encode(
        x=alt.X("date", title="Date"),
        y=alt.Y("avg_temp", title="Average Temperature"),
        color="plant_id:N",
        tooltip=[alt.Tooltip("plant_id", title="Plant ID"),
                 alt.Tooltip("species_name", title="Species"),
                 alt.Tooltip("avg_temp", title="Average Temperature"),
                 alt.Tooltip("botanist_email", title="Botanist Email")]
    ).interactive()

    return graph


@st.cache_data
def historic_plant_moisture(df: pd.DataFrame, start_date: str,
                            end_date: str, _plant_id_list: list[str]) -> alt.Chart:
    """
    Produces a scatter chart of plant moisture over time
    in a specific date range for selected plant id's.
    """
    df["date"] = pd.to_datetime(
        {"year": df.year, "month": df.month, "day": df.day})
    df = df[["species_name", "plant_id", "avg_moisture", "date", "botanist_email"]]
    df = df[df["date"].between(start_date, end_date)]
    mask = df["plant_id"].isin(_plant_id_list)
    df = df[mask]

    graph = alt.Chart(
        df,
        title=f"Average Plant Moisture: {start_date} - {end_date}"
        ).mark_line(point=True).encode(
        x=alt.X("date"),
        y=alt.Y("avg_moisture"),
        color="plant_id:N",
        tooltip=[alt.Tooltip("plant_id", title="Plant ID"),
                 alt.Tooltip("species_name", title="Species"),
                 alt.Tooltip("avg_moisture", title="Average Moisture"),
                 alt.Tooltip("botanist_email", title="Botanist Email")]).interactive()

    return graph


@st.cache_data
def historic_plant_waterings(df: pd.DataFrame, start_date: str,
                             end_date: str, _plant_id_list: list[str]) -> alt.Chart:
    """
    Produces a bar chart of the count of plant waterings over time
    in a specific date range for selected plant id's.
    """
    df["date"] = pd.to_datetime(
        {"year": df.year, "month": df.month, "day": df.day})
    df = df[["species_name", "plant_id",
             "times_watered", "date", "botanist_email"]]
    df = df[df["date"].between(start_date, end_date)]
    mask = df["plant_id"].isin(_plant_id_list)
    df = df[mask]

    graph = alt.Chart(
        df,
        title=f"Number of Times Plants were Watered: {start_date} - {end_date}"
        ).mark_bar().encode(
        x=alt.X("date"),
        y=alt.Y("sum(times_watered):Q"),
        xOffset="plant_id:N",
        color=alt.Color("plant_id:N"),
        tooltip=[alt.Tooltip("plant_id", title="Plant ID"),
                 alt.Tooltip("species_name", title="Species"),
                 alt.Tooltip("times_watered", title="Number of Times Watered"),
                 alt.Tooltip("botanist_email", title="Botanist Email")]
    ).interactive()

    return graph
