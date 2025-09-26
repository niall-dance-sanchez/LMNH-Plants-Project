## About

Code that runs every minute to extract plant data from the API, transform it, and upload it to the RDS. After 24 hours of data is stored in the RDS, the code will remove the oldest minute of data stored for every new minute that is uploaded to ensure the RDS stores only the past 24 hours of data.

### `extract.py`

Contains code for calling to the LMNH plants API, and extracting data from it. The code is asynchronous, allowing for extremely quick data collection on a frequent basis, as needed by the project requirements.

### `transform.py`

Functions to transform the data gathered from the extract code into clean, validated data.

This script will throw an exception when an uncorrectable issue arises; such as, for example, a bad data type, or missing value.

### `load.py`

Contains Helper function to combine the loading of the master data (from all tables other than "reading") and transactional ("reading") data.

Relies on two helper scripts:

1. load_master_data.py
2. insert_transactional_data.py

#### `load_master_data.py`
This script detects any new master data (data not belonging to a reading itself), and updates the RDS target with that new data.

#### `insert_transactional_data.py`
This script loads the new reading data records.

`load.py` just ties these two scripts together to ensure that there is consistency in the destination DB.

## Usage

The functionality of this module is tied together by `run_etl.py`. This is designed to be ran as a Lambda function docker image, which is then pushed to an ECS.

A simple way to do this is to run

```bash
$ sh ./create_docker_image.sh
```

which will create and push the docker image to the required ECR without any interaction.

Alternatively, you can run:

```bash
$ docker buildx build --provenance=False --platform=linux/amd64 -t c19-ajldka-short-term-etl:latest .
```

Which will build the image as needed. You can then test the image locally. First start a new container process by running:

```bash
$ docker run -p 9000:8080 --env-file .env c19-ajldka-short-term-etl:latest
```

and then send a request to the local process:

```bash
$ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

If the process returns `Null`, then it is working correctly, you can then push it to an ECR using the shell script mentioned before.
