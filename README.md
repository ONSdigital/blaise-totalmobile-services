# blaise-totalmobile-client

A python client for interacting with totalmobile

## Running

Setup a `.env` file:

```.env
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
```

Generate a GCP creds file:
```sh
gcloud iam service-accounts keys create keys.json --iam-account ons-blaise-v2-dev-sandbox123@appspot.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=keys.json
```

Open a tunnel to our Blaise RESTful API in your GCP project:

gcloud compute start-iap-tunnel restapi-1 80 --local-host-port=localhost:90 --zone europe-west2-a

```sh
poetry install
poetry run python cli.py
```

Deploy test cloud function

```sh
gcloud config set project "ons-blaise-v2-dev-sandbox123"
gcloud functions deploy TestTMCreateJob \
  --source=. \
  --region=europe-west2 \
  --runtime=python39 \
  --services-account="ons-blaise-v2-dev-sandbox123@appspot.gserviceaccount.com" \
  --trigger-http \
  --set-env-vars='TOTALMOBILE_URL=<totalmobile_url>,TOTALMOBILE_INSTANCE=<totalmobile_instance>,TOTALMOBILE_CLIENT_ID=<totalmobile_client_id>,TOTALMOBILE_CLIENT_SECRET=<totalmobile_client_id>'
```

## Poetry problems

Dependencies (like the blaise-restapi) not updating properly after running ```poetry update blaise-restapi``` ???

This worked for me:

* cd into the folder where pyproject.toml is
* Run ```poetry env list``` (this will show you the venv for the project)
* Then run ```poetry env remove whatever-WhATeVs-py3.9``` to delete it (where ```whatever-WhATeVs-py3.9``` is the venv displayed from the above command) 
* Running ```poetry install``` <i>should</i> install all the deps listed in pyproject.toml.
