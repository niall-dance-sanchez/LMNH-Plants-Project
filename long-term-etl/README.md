## About

### extract.py

Functions for extracting all of the data from the RDS, which will be triggered at midnight to extract all the data from the previous day. 

### summarise.py

Function for summarising the extracted code into aggregate data for each plant to be used for long-term analysis.

### load.py

Handler function setup for the ETL process to be run as an AWS Lambda function. The code uses the functions from the extract and transform scripts, and then uploads it as a .parquet file in a directory partitioned by the day. 

## Usage

1. Set up AWS infrastructure in Terraform directory 
2. Go to the ECR and follow the docker upload commands, to upload the container image from this directory (dockerfile)
