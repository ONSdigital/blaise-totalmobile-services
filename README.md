# Blaise Totalmobile Services ![bts](.github/bts.png)

We integrate with Totalmobile for field workforce management. We send case details to Totalmobile and it manages the allocation of cases to field interviewers. Field interviewers will capture some data using a Totalmobile app on their smartphones, this data will be sent back to us so we can update the Blaise data.

This project contains several services for sending data to and receiving data from Totalmobile.

### Services

- Cloud Function (create_totalmobile_job) to create jobs in Totalmobile.
- Cloud Function (create_questionnaire_case_tasks) to get all cases for a questionnaire, apply business logic to filter out cases, then send the case details to Totalmobile as "jobs" via the create_totalmobile_job Cloud Function via Cloud Tasks.
- Cloud Function (check_questionnaire_release_date) to check if a Totalmobile release date has been set for a questionnaire in [DQS](https://github.com/ONSdigital/blaise-deploy-questionnaire-service), if the Totalmobile release date is for today it sends the questionnaire to the create_questionnaire_case_tasks Cloud Function.
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

Generate Totalmobile password hash:
```sh
poetry run python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('blah'))"
```

Create an .env file in the root of the project and add the following environment variables:

| Variable | Description | Example |
| --- | --- | --- |
| GCLOUD_PROJECT | The GCP project the application will use. | ons-blaise-v2-dev-sandbox123 |
| REGION | The GCP region the application will be deployed to. | europe-west2 |
| BLAISE_API_URL | The RESTful API URL the application will use to get and update questionnaire data. | http://localhost:90 |
| BLAISE_SERVER_PARK | The Blaise Server Park name we will be getting the Blaise data from. | gusty |
| GOOGLE_APPLICATION_CREDENTIALS | Google application credentials to access Datastore. | keys.json |
| TOTALMOBILE_URL | The Totalmobile instance URL. | https://ons-dev.totalmobile-cloud.com |
| TOTALMOBILE_INSTANCE | The Totalmobile instance type. | Test |
| TOTALMOBILE_CLIENT_ID | The client ID to authenicate with Totalmobile. | blah |
| TOTALMOBILE_CLIENT_SECRET | The client secret to authenicate with Totalmobile. | blah |
| TOTALMOBILE_JOB_CLOUD_FUNCTION | The name of the Cloud Function for creating jobs in Totalmobile. | create-totalmobile-job |
| TOTALMOBILE_JOBS_QUEUE_ID | The Cloud Tasks queue ID for sending jobs to Totalmobile. | projects/ons-blaise-v2-dev-sandbox123/locations/europe-west2/queues/totalmobile-jobs |
| TOTALMOBILE_USER | The username for Totalmobile to authenicate with us. | blah |
| TOTALMOBILE_PASSWORD_HASH | The hashed password for Totalmobile to authenicate with us. | pbkdf2:sha256:260000$Y1Pew7gJMYbRhfNR$9b97ee1d4a735047051c83bff275532d4d1322f1fc186739189b00fa7cc9a51b |
| CLOUD_FUNCTION_SA | The GCP service account the cloud functions will use. | totalmobile-sa@ons-blaise-v2-dev-sandbox123.iam.gserviceaccount.com |

```
GCLOUD_PROJECT=ons-blaise-v2-dev-sandbox123
REGION=europe-west2
BLAISE_API_URL=http://localhost:90
BLAISE_SERVER_PARK=gusty
TOTALMOBILE_URL=https://ons-dev.totalmobile-cloud.com
TOTALMOBILE_INSTANCE=Test
TOTALMOBILE_CLIENT_ID=blah
TOTALMOBILE_CLIENT_SECRET=blah
TOTALMOBILE_JOB_CLOUD_FUNCTION=create-totalmobile-job
TOTALMOBILE_JOBS_QUEUE_ID=projects/ons-blaise-v2-dev-sandbox123/locations/europe-west2/queues/totalmobile-jobs
TOTALMOBILE_USER=blah
TOTALMOBILE_PASSWORD_HASH=pbkdf2:sha256:260000$Y1Pew7gJMYbRhfNR$9b97ee1d4a735047051c83bff275532d4d1322f1fc186739189b00fa7cc9a51b
CLOUD_FUNCTION_SA=totalmobile-sa@ons-blaise-v2-dev-sandbox123.iam.gserviceaccount.com
```

Run the Flask application:
```shell
poetry run python main.py
```

You should now be able to call the Flask application endpoints via localhost:5011. See the [app readme](app/README.md) for more details.

Run the "create_totalmobile_job" Cloud Function:
```shell
poetry run python -c "import flask; from main import create_totalmobile_job; create_totalmobile_job(flask.Request.from_values(json={'questionnaire': 'DST2101_AA1', 'world_id': '7e4beb99-ed79-4179-ab39-ab6600ebd65e', 'case': {'qiD.Serial_Number': '100100', 'dataModelName': 'DST2101_AA1', 'qDataBag.TLA': 'DST', 'qDataBag.Wave': '1', 'qDataBag.Prem1': 'Ye Olde Fighting Cocks', 'qDataBag.Prem2': '16 Abbey Mill Lane', 'qDataBag.Prem3': '', 'qDataBag.District': '', 'qDataBag.PostTown': 'St Albans', 'qDataBag.PostCode': 'AL3 4HE', 'qDataBag.TelNo': '', 'qDataBag.TelNo2': '', 'telNoAppt': '', 'hOut': '', 'qDataBag.UPRN_Latitude': '51.748930', 'qDataBag.UPRN_Longitude': '-0.346820', 'qDataBag.Priority': '1', 'qDataBag.FieldRegion': '', 'qDataBag.FieldTeam': 'The A Team', 'qDataBag.WaveComDTE': '2020-11-17'}}))"
```

Run the "create_questionnaire_case_tasks" Cloud Function:
```shell
poetry run python -c "import flask; from main import create_questionnaire_case_tasks; create_questionnaire_case_tasks(flask.Request.from_values(json={'questionnaire': 'DST2111Z'}))"
```

Run the "check_questionnaire_release_date" Cloud Function:
```shell
poetry run python -c "from main import check_questionnaire_release_date; check_questionnaire_release_date(None, None)"
```

Run unit tests:
```shell
poetry run python -m pytest
```

### Poetry Problems

Dependencies (like the blaise-restapi) not updating properly after running ```poetry update blaise-restapi``` ???

This worked for me:

* cd into the folder where pyproject.toml is
* Run ```poetry env list``` (this will show you the venv for the project)
* Then run ```poetry env remove whatever-WhATeVs-py3.9``` to delete it (where ```whatever-WhATeVs-py3.9``` is the venv displayed from the above command) 
* Running ```poetry install``` <i>should</i> install all the deps listed in pyproject.toml.
