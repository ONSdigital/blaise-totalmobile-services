# Blaise Totalmobile Services

We integrate with Totalmobile for field workforce management.

This project contains several services for sending data to and receiving data from Totalmobile.

### Services

- Cloud Function () blah blah blah
- Cloud Function () blah blah blah
- Flask application blah blah blah

### Local Setup

Clone the project locally:
```shell
git clone https://github.com/ONSdigital/blaise-export-reporting-tool.git
```

Install poetry:
```shell
pip install poetry
```

Install dependencies:
```shell
poetry install
```

Authenticate with GCP:
```shell
gcloud auth login
```

Set your GCP project:
```shell
gcloud config set project ons-blaise-v2-dev-sandbox123
```

Open a tunnel to our Blaise RESTful API in your GCP project:
```shell
gcloud compute start-iap-tunnel restapi-1 80 --local-host-port=localhost:90 --zone europe-west2-a
```

Download a service account JSON key:
```
gcloud iam service-accounts keys create keys.json --iam-account ons-blaise-v2-dev-sandbox123@appspot.gserviceaccount.com
```

Temporary set your local GOOGLE_APPLICATION_CREDENTIALS environment variable to this JSON file:

```
Unix: export GOOGLE_APPLICATION_CREDENTIALS=keys.json
Windows: set GOOGLE_APPLICATION_CREDENTIALS=keys.json
```

Create an .env file in the root of the project and add the following environment variables:

```
TOTALMOBILE_URL=
TOTALMOBILE_INSTANCE=
TOTALMOBILE_CLIENT_ID=
TOTALMOBILE_CLIENT_SECRET=
BUS_URL=
BUS_CLIENT_ID=
INSTRUMENT_NAME=
CLOUD_FUNCTION_SA=
TOTALMOBILE_USER=
TOTALMOBILE_PASSWORD_HASH=
```

Run the Flask application:

```shell
poetry run python main.py
```

You should now be able to call the Flask application endpoints via localhost:5011. Examples:

blah blah blah

Run the blah Cloud Function:

```shell
poetry run python -c ""
```

Run the CLI:

```sh
poetry run python cli.py
```

Run Tests

```shell
poetry run python -m pytest
```