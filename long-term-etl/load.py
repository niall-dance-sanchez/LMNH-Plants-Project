"""Load plant data from RDS into S3."""
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv
import pandas as pd
import awswrangler as wr
import boto3

from extract import get_db_connection, extract_day_of_data
from summarise import create_summary

BUCKET = "c19-ajldka-lmnh-plants"


def get_s3_connection():
    """Connect to the plant data S3 bucket."""
    return boto3.Session(
        aws_access_key_id=getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=getenv("AWS_REGION")
    )


def create_previous_day_parquet_file_path(bucket: str):

    yesterday = datetime.now() - timedelta(days=1)
    year = yesterday.year
    month = f"{yesterday.month:02d}"
    day = f"{yesterday.day:02d}"

    return f"s3://{bucket}/input/year={year}/month={month}/day={day}/plants_summary.parquet"


def upload_summary_to_s3(df: pd.DataFrame, path: str, boto_session):
    """Upload summary data to S3 bucket."""

    wr.s3.to_parquet(
        df=df,
        path=path,
        dataset=False,
        boto3_session=boto_session
    )


def handler(event=None, context=None) -> dict:
    """Main Lambda handler function."""

    load_dotenv()

    boto_session = get_s3_connection()
    conn = get_db_connection()

    plant_data = extract_day_of_data(conn)
    plant_df = create_summary(plant_data)
    file_path = create_previous_day_parquet_file_path(BUCKET)

    upload_summary_to_s3(plant_df, file_path, boto_session)

    return {"statusCode": 200}
