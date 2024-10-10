Totalmobile provide a "dynamic HTTP adapter", essentially this allows us to setup predefined endpoints for receiving data updates from Totalmobile. We can then use these data updates to update the Blaise data. The endpoints have basic authenication, the username and password (hashed) are set as environment variables. The dynamic HTTP adapter can be configured from the Totalmobile UI.

### Endpoints 

Endpoints can be found in app/endpoints.py and are as follows:

* "/ons/totalmobile-incoming/SubmitFormResultRequest"
* "/ons/totalmobile-incoming/CreateVisitRequest"
* "/ons/totalmobile-incoming/ForceRecallVisitRequest"

The first endpoint is for LMS responses.
The other 2 endpoints (/createvisitrequest & /forcerecallvisitrequest) are for FRS Allocations and Unallocations. 

These are the endpoints to which Totalmobile's event-driven processes will post JSON payloads.

### Payloads

Sample payloads can be found in test/conftest.py under:

* def submit_form_result_request_sample()
* def create_visit_request_sample()
* def force_recall_visit_request_payload()

Field interviewer name has been replaced with jane.doe and some GUIDs and IDs were replaced.

### IDs

The unique identifier for the endpoint payloads are as follows:

* SubmitFormResultRequest - ["Result"]["Association"]["Reference"]
* CreateVisitRequest - ["Visit"]["Identity"]["Reference"]
* ForceRecallVisitRequest - ["Identity"]["Reference"]

These IDs are the job reference we set when sending data to Totalmobile and is should be constructed from the questionnaire name and case ID. This is how we will link the data back to the Blaise data.
