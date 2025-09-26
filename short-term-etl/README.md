## About

Code that runs every minute to extract plant data from the API, transform it, and upload it to the RDS. After 24 hours of data is stored in the RDS, the code will remove the oldest minute of data stored for every new minute that is uploaded to ensure the RDS stores only the past 24 hours of data.

### extract.py

Functions for extracting all of the data from the API.

### transform.py

Functions to transform the data gathered from the extract code into clean, validated data.

### load.py

Contains Helper function to combine the loading of the master data (from all tables other than "reading") and transactional ("reading") data.

## Usage

1. 



