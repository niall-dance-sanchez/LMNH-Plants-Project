"""A script with functions that summarise the plant data into key metrics."""

import pandas as pd


def create_summary(data: list[dict]) -> pd.DataFrame:
    """Creates a dataframe with key summary statistics for each plant."""

    df = pd.DataFrame(data)

    return df.groupby(["plant_id", "species_name", "country_name", "city_name", "botanist_email"]).aggregate(
        avg_temp=pd.NamedAgg(column="temperature", aggfunc="mean"),
        min_temp=pd.NamedAgg(column="temperature", aggfunc="min"),
        max_temp=pd.NamedAgg(column="temperature", aggfunc="max"),
        std_temp=pd.NamedAgg(column="temperature", aggfunc="std"),
        avg_moisture=pd.NamedAgg(column="soil_moisture", aggfunc="mean"),
        min_moisture=pd.NamedAgg(column="soil_moisture", aggfunc="min"),
        max_moisture=pd.NamedAgg(column="soil_moisture", aggfunc="max"),
        std_moisture=pd.NamedAgg(column="soil_moisture", aggfunc="std"),
        times_watered=pd.NamedAgg(column="last_watered", aggfunc="nunique")
    ).reset_index()
