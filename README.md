# Blaise Totalmobile Services

We integrate with Totalmobile for field workforce management. We send case details to Totalmobile and it manages the allocation of cases to field interviewers. Field interviewers will capture some data using a Totalmobile app on their smartphones, this data will be sent back to us so we can update the Blaise data.

This project contains several services for sending data to and receiving data from Totalmobile.

### Services

- Cloud Function () blah blah blah
- Cloud Function () blah blah blah
- Flask application with several endpoints for receiving data updates from Totalmobile. More details can be found in the [app readme](app/README.md).

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
BLAISE_API_URL=
BLAISE_SERVER_PARK=
BUS_URL=
BUS_CLIENT_ID=
INSTRUMENT_NAME=
CLOUD_FUNCTION_SA=
TOTALMOBILE_USER=
TOTALMOBILE_PASSWORD_HASH=
```

Generate Totalmobile password hash:
```sh
poetry run python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('blah'))"
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

Run unit tests:
```shell
poetry run python -m pytest
```

### Poetry problems

Dependencies (like the blaise-restapi) not updating properly after running ```poetry update blaise-restapi``` ???

This worked for me:

* cd into the folder where pyproject.toml is
* Run ```poetry env list``` (this will show you the venv for the project)
* Then run ```poetry env remove whatever-WhATeVs-py3.9``` to delete it (where ```whatever-WhATeVs-py3.9``` is the venv displayed from the above command) 
* Running ```poetry install``` <i>should</i> install all the deps listed in pyproject.toml.
