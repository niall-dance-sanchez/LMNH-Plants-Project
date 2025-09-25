"""Load plant data from RDS into S3."""
from os import getenv
from dotenv import load_dotenv
import pandas as pd
import awswrangler as wr
import boto3

from extract import get_db_connection, extract_day_of_data
from summarise import create_summary


def upload_summary_to_s3(df: pd.DataFrame, path: str, boto_sess):
    """Upload summary data to S3 bucket."""
    wr.s3.to_parquet(
        df=df,
        path=path,
        dataset=False,
        mode="append",
        boto3_session=boto_sess
    )

if __name__ == "__main__":
    load_dotenv()

    boto_session = boto3.Session(
        aws_access_key_id=getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=getenv("AWS_REGION")
    )

    conn = get_db_connection()

    # extract
    with conn.cursor() as cur:
        rows = extract_day_of_data(conn)
        plant_data = [dict(zip([col[0] for col in cur.description], row)) for row in rows]

    # transform
    plant_df = create_summary(plant_data)

    BUCKET = "c19-ajldka-lmnh-plants"
    S3_PATH = f"s3://{BUCKET}/input/plants_summary.parquet"
    # load
    upload_summary_to_s3(plant_df, S3_PATH, boto_session)
