# Useful Scripts to Help Developer Productivity

These scripts can be run directly from Python. However, to run them you may need to do a bit of setup.

Download a service account JSON key:
```
gcloud iam service-accounts keys create keys.json --iam-account ons-blaise-v2-dev-sandbox123@appspot.gserviceaccount.com
```

Temporary set your local GOOGLE_APPLICATION_CREDENTIALS environment variable to this JSON file:
```
Unix: export GOOGLE_APPLICATION_CREDENTIALS=keys.json
Windows: set GOOGLE_APPLICATION_CREDENTIALS=keys.json
```

Temporary set any local environment variables the script requires:
```
Unix: export TOTALMOBILE_URL=blah
Windows: set TOTALMOBILE_URL=blah
```

Install dependencies:
```shell
poetry install
```

Ensure your Python path is set to the root of the repository:
```shell
Unix: PYTHONPATH=. poetry run python scripts/my_funky_script.sh
Windows: set PYTHONPATH=. & poetry run python scripts/my_funky_script.sh
```
