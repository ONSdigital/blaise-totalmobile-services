# Blaise Totalmobile Services - Cloud Functions

## Cloud Function Local Setup

After following the Local Setup instructions in the [README](../README.md), continue the following to run the Cloud Functions locally.

Run the "create_totalmobile_jobs_trigger" Cloud Function:
```shell
poetry run python -c "from main import create_totalmobile_jobs_trigger; create_totalmobile_jobs_trigger(None, None)"
```

Run the "create_totalmobile_jobs_processor" Cloud Function:
```shell
poetry run python -c "import flask; from main import create_totalmobile_jobs_processor; create_totalmobile_jobs_processor(flask.Request.from_values(json={'questionnaire': 'DST2101_AA1', 'world_id': '7e4beb99-ed79-4179-ab39-ab6600ebd65e', 'case': {'qiD.Serial_Number': '100100', 'dataModelName': 'DST2101_AA1', 'qDataBag.TLA': 'DST', 'qDataBag.Wave': '1', 'qDataBag.Prem1': 'Ye Olde Fighting Cocks', 'qDataBag.Prem2': '16 Abbey Mill Lane', 'qDataBag.Prem3': '', 'qDataBag.District': '', 'qDataBag.PostTown': 'St Albans', 'qDataBag.PostCode': 'AL3 4HE', 'qDataBag.TelNo': '', 'qDataBag.TelNo2': '', 'telNoAppt': '', 'hOut': '', 'qDataBag.UPRN_Latitude': '51.748930', 'qDataBag.UPRN_Longitude': '-0.346820', 'qDataBag.Priority': '1', 'qDataBag.FieldRegion': '', 'qDataBag.FieldTeam': 'The A Team', 'qDataBag.WaveComDTE': '2020-11-17'}}))"
```

Run the "delete_totalmobile_jobs_completed_in_blaise" Cloud Function:
```shell
poetry run python -c "from main import delete_totalmobile_jobs_completed_in_blaise; delete_totalmobile_jobs_completed_in_blaise(None, None)"
```