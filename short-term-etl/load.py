"""Uses helper scripts to complete the load stage of the short-term ETL."""


import pyodbc

from insert_transactional_data import insert_transactional_data
from load_master_data import load_master_data


def load_cleaned_data(data: list[dict], con: pyodbc.Connection) -> None:
    """Completes the Load stage of the ETL using two helper scripts."""
    # Insert any new detected master data
    load_master_data(data=data, conn=con)
    # Insert the reading transaction data
    insert_transactional_data(data=data, con=con)
