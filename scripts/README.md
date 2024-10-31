# Scripts

These scripts are to support developers with various tasks when working with the Totalmobile API. They can be run directly using Python but some setup is required.

## Setup

Download a GCP service account JSON key:
```
gcloud iam service-accounts keys create keys.json --iam-account ons-blaise-v2-dev-sandbox123@appspot.gserviceaccount.com
```

Set temporary environment variables for GCP authenticating using this JSON key and connection details for the Totalmobile API:

Unix
```bash
export GOOGLE_APPLICATION_CREDENTIALS=keys.json
export TOTALMOBILE_URL=blah
export TOTALMOBILE_CLIENT_ID=blah
export TOTALMOBILE_CLIENT_SECRET=blah
export TOTALMOBILE_INSTANCE=blah
```

Windows
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=keys.json
set TOTALMOBILE_URL=blah
set TOTALMOBILE_CLIENT_ID=blah
set TOTALMOBILE_CLIENT_SECRET=blah
set TOTALMOBILE_INSTANCE=blah
```

Replace placeholder values accordingly.

Install dependencies:
```shell
poetry install
```

Set Python path and run desired script:

Unix
```bash
PYTHONPATH=. poetry run python scripts/my_funky_script.sh
```

Windows
```cmd
set PYTHONPATH=. & poetry run python scripts\my_funky_script.sh
```
