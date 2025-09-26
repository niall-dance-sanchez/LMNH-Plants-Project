"""File containing the functions to create graphs for the live plant data."""

import altair as alt
import pandas as pd
import streamlit as st


@st.cache_data
def create_sales_per_day(df: pd.DataFrame, plant_ids: list[int]) -> alt.Chart:
    """Produces a line chart of total sales over time."""

    return alt.Chart(df[df["plant_id"].isin(plant_ids)], title="Plant Temperature Readings").mark_line().encode(
        alt.X("recording_taken", title="Recording Taken",
              axis=alt.Axis(format='%H:%M')).scale(zero=False),
        alt.Y("temperature", title="Temperature (C)").scale(zero=False),
        color="plant_id:N",
        tooltip=[alt.Tooltip('plant_id', title="Plant ID"),
                 alt.Tooltip('species_name', title="Species"),
                 alt.Tooltip('temperature',
                             title="Temperature (C)", format='.2f'),
                 alt.Tooltip('recording_taken:T',
                             title='Recording Taken', format='%H:%M %d %b %Y'),
                 'botanist_email']
    ).properties(width=1000).interactive()


@st.cache_data
def create_sales_per_day(df: pd.DataFrame, plant_ids: list[int]) -> alt.Chart:
    """Produces a line chart of total sales over time."""

    return alt.Chart(df[df["plant_id"].isin(plant_ids)], title="Plant Soil Moisture Readings").mark_line().encode(
        alt.X("recording_taken", title="Recording Taken",
              axis=alt.Axis(format='%H:%M')).scale(zero=False),
        alt.Y("soil_moisture", title="Soil Moisture (%)").scale(zero=False),
        color="plant_id:N",
        tooltip=[alt.Tooltip('plant_id', title="Plant ID"),
                 alt.Tooltip('species_name', title="Species"),
                 alt.Tooltip('soil_moisture',
                             title="Soil Moisture (%)", format='.2f'),
                 alt.Tooltip('recording_taken:T',
                             title='Recording Taken', format='%H:%M %d %b %Y'),
                 'botanist_email']
    ).properties(width=1000).interactive()
