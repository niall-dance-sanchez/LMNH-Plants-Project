# About

This repo contains tools for deploying a plant monitoring system for the Liverpool Museum of Natural History. The code allows the museum to monitor the health of the plants over time and has contact details for each botanist so they can be alerted to any significant changes of a plant's condition. Live data of the previous 24 hours is uploaded to an RDS, while summary data of each day is stored long-term in an S3 bucket. Streamlit is used to host dashboards with visualisations displaying data about the plants' health.

# Directory Guide

## dashboard

Code that manages the dashboard structure and visualisations. 

## diagrams

Diagrams of the project architecture, database ERD and dashboard wireframe. 

## long-term-etl

Code that runs daily at midnight to summarise the data from the RDS and upload it to long-term storage (AWS S3 Bucket). The data is summarised and converted to .parquet files which are then queried by a combination of AWS Glue Crawler and Athena to create visualisations on the dashboard.

## short-term-etl

Code that runs every minute to extract plant data from the API, transform it, and upload it to the RDS. After 24 hours of data is stored in the RDS, the code will remove the oldest minute of data stored for every new minute that is uploaded to ensure the RDS stores only the past 24 hours of data.

## terraform

Launches all of the AWS infrastructure required for the project. A remote backend is used so that infrastructure can be managed easily from different machines. 