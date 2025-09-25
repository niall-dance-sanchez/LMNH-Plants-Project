"""ETL script designed to be run inside an AWS Lambda function as a container."""

from extract import extract_all_plant_data
from transform import clean_data
from load import get_connection, load_cleaned_data


def lambda_handler(event, context):
    """Runs the short-term ETL process."""
    raw_data = extract_all_plant_data()
    cleaned_data = clean_data(data=raw_data)
    conn = get_connection()
    load_cleaned_data(data=cleaned_data, con=conn)
    conn.close()
