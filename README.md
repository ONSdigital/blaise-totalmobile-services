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
gcloud iam service-accounts keys create keys.json --iam-account ons-blaise-v2-dev-sandbox123@appspot.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=keys.json
```

```sh
poetry install
poetry run python main.py
```
