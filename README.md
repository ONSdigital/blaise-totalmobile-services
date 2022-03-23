# blaise-totalmobile-client

A python client for interacting with totalmobile

## Running

Setup a `.env` file:

```.env
TOTALMOBILE_URL=
TOTALMOBILE_INSTANCE=
TOTALMOBILE_CLIENT_ID=
TOTALMOBILE_CLIENT_SECRET=
BUS_URL=
BUS_CLIENT_ID=
INSTRUMENT_NAME=
```

Generate a GCP creds file:
```sh
gcloud iam services-accounts keys create keys.json --iam-account ons-blaise-v2-dev-sandbox123@appspot.gserviceaccount.com
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
