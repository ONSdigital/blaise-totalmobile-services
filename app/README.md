# Blaise Totalmobile Services - Flask App

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

## App Local Setup

After following the Local Setup instructions in the [README](../README.md), continue the following to run the app locally.

1. **Enable debug mode locally**  
   In `main.py`, replace ```app.run_tasks(host="0.0.0.0", port=5011)``` with ```app.run(debug=True, host="0.0.0.0", port=5011)```
2. **Disable authentication for local testing**  
In `app/endpoints.py`, comment out any `@auth.login_required` lines where necessary.  

> **Note:** Do not commit these changes.

3. **Run the application**  
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
