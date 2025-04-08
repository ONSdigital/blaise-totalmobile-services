Totalmobile provide a "dynamic HTTP adapter", essentially this allows us to setup predefined endpoints for receiving data updates from Totalmobile. We can then use these data updates to update the Blaise data. The endpoints have basic authenication, the username and password (hashed) are set as environment variables. The dynamic HTTP adapter can be configured from the Totalmobile UI.

## Endpoints 

Endpoints can be found in app/endpoints.py and are as follows:

* "/ons/totalmobile-incoming/SubmitFormResultRequest"
* "/ons/totalmobile-incoming/CreateVisitRequest"
* "/ons/totalmobile-incoming/ForceRecallVisitRequest"

The first endpoint is for LMS responses.
The other 2 endpoints (/createvisitrequest & /forcerecallvisitrequest) are for FRS Allocations and Unallocations. 

These are the endpoints to which Totalmobile's event-driven processes will post JSON payloads.

## Payloads

Sample payloads can be found in test/conftest.py under:

* def submit_form_result_request_sample()
* def create_visit_request_sample()
* def force_recall_visit_request_payload()

Field interviewer name has been replaced with jane.doe and some GUIDs and IDs were replaced.

## IDs

The unique identifier for the endpoint payloads are as follows:

* SubmitFormResultRequest - ["Result"]["Association"]["Reference"]
* CreateVisitRequest - ["Visit"]["Identity"]["Reference"]
* ForceRecallVisitRequest - ["Identity"]["Reference"]

These IDs are the job reference we set when sending data to Totalmobile and is should be constructed from the questionnaire name and case ID. This is how we will link the data back to the Blaise data.

# BTS Endpoints Local Setup Guide

## Prerequisites

Before starting, make sure you have:

- A sandbox environment  
- A LMS or FRS questionnaire installed  
- Cases loaded into the questionnaire  
- [Postman](https://www.postman.com/downloads/) installed  
- (For CMA testing) A Field Interviewer user in Blaise  

---

## Setup

1. **Set your GCP project**  
   Use the following command to set your GCP project to the relevant sandbox.  
   Example: `ons-blaise-v2-dev-sandbox123`

2. **Open a tunnel to the Blaise REST API**  
   Start an IAP tunnel to the REST API on your GCP project.  
   Use port 90 and ensure the zone is set to `europe-west2-a`.

3. Create an .env file in the root of the project and add the following environment variables:

| Variable | Description | Example                                                                                                |
| --- | --- |--------------------------------------------------------------------------------------------------------|
| GCLOUD_PROJECT | The GCP project the application will use. | ons-blaise-v2-dev-sandbox123                                                                           |
| REGION | The GCP region the application will be deployed to. | europe-west2                                                                                           |
| BLAISE_API_URL | The RESTful API URL the application will use to get and update questionnaire data. | http://localhost:90                                                                                    |
| BLAISE_SERVER_PARK | The Blaise Server Park name we will be getting the Blaise data from. | gusty                                                                                                  |
| CMA_SERVER_PARK | The CMA Server Park name we will be getting the CMA Launcher data from. | cma                                                                                                  |
| CREATE_TOTALMOBILE_JOBS_TASK_QUEUE_ID | The Cloud Tasks queue ID for creating jobs to Totalmobile. | projects/ons-blaise-v2-dev-sandbox123/locations/europe-west2/queues/totalmobile-jobs                   |
| TOTALMOBILE_URL | The Totalmobile instance URL. | https://ons-dev.totalmobile-cloud.com                                                                  |
| TOTALMOBILE_INSTANCE | The Totalmobile instance type. | test                                                                                                   |
| TOTALMOBILE_CLIENT_ID | The client ID to authenicate with Totalmobile. | test                                                                                                   |
| TOTALMOBILE_CLIENT_SECRET | The client secret to authenicate with Totalmobile. | test                                                                                                   |
| TOTALMOBILE_INCOMING_USER | The username for Totalmobile to authenicate with us. | test                                                                                                   |
| TOTALMOBILE_INCOMING_PASSWORD_HASH | The hashed password for Totalmobile to authenicate with us. | pbkdf2:sha256:260000$Y1Pew7gJMYbRhfNR$9b97ee1d4a735047051c83bff275532d4d1322f1fc186739189b00fa7cc9a51b |
| CLOUD_FUNCTION_SA | The GCP service account the cloud functions will use. | totalmobile-sa@ons-blaise-v2-dev-sandbox123.iam.gserviceaccount.com                                    |

```
GCLOUD_PROJECT=ons-blaise-v2-dev-sandbox123
REGION=europe-west2
BLAISE_API_URL=http://localhost:90
BLAISE_SERVER_PARK=gusty
CMA_SERVER_PARK=cma
CREATE_TOTALMOBILE_JOBS_TASK_QUEUE_ID=projects/ons-blaise-v2-dev-sandbox123/locations/europe-west2/queues/totalmobile-jobs
TOTALMOBILE_URL=https://ons-dev.totalmobile-cloud.com
TOTALMOBILE_INSTANCE=Test
TOTALMOBILE_CLIENT_ID=blah
TOTALMOBILE_CLIENT_SECRET=blah
TOTALMOBILE_INCOMING_USER=blah
TOTALMOBILE_INCOMING_PASSWORD_HASH=pbkdf2:sha256:260000$Y1Pew7gJMYbRhfNR$9b97ee1d4a735047051c83bff275532d4d1322f1fc186739189b00fa7cc9a51b
CLOUD_FUNCTION_SA=totalmobile-sa@ons-blaise-v2-dev-sandbox123.iam.gserviceaccount.com
```
5. **Enable debug mode locally**  
   In `main.py`, replace ```app.run_tasks(host="0.0.0.0", port=5011)``` with ```app.run(debug=True, host="0.0.0.0", port=5011)```
6. **Disable authentication for local testing**  
In `app/endpoints.py`, comment out any `@auth.login_required` lines where necessary.  

> **Note:** Do not commit these changes.

7. **Run the application**  
Run `main.py` and note the address shown next to "Running on".  
You will use this to send test requests from Postman.

---

## Using Postman

1. Open Postman and create a new request.  
- **Method**: `POST`  
- **URL**: Use the address shown in the terminal after running `main.py`, and append the endpoint path, for example:  
  ```
  http://127.0.0.1:5011/bts/createvisitrequest
  ```

2. In the **Body** tab:
- Set it to `raw`
- Choose `JSON` format

3. Copy a sample payload from `test/conftest.py` and paste it into the body.  
- Update the `user` and `reference` fields  
- The `reference` should follow the format:  
  ```
  <QUESTIONNAIRE_NAME>.<CASE_ID>
  ```
  Example: `FRS001.12345`

---

## Finding Valid Case IDs

1. Jump on the REST API box in your GCP project.
2. Open a browser on the instance and navigate to ```http://localhost/swagger``` 
3. Use the ```GET /api/v2/serverparks/{serverParkName}/questionnaires/{questionnaireName}/cases/ids``` endpoint to fetch a list of valid case IDs for your questionnaire. 


