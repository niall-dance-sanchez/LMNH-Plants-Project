"""A script with functions that summarise the plant data into key metrics."""

import pandas as pd


def create_summary(data: list[dict]) -> pd.DataFrame:

    df = pd.DataFrame(data)

    df.groupby(["plant_id"]).aggregate()
