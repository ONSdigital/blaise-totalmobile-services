Totalmobile provide a "dynamic HTTP adapter", essentially this allows us to setup predefined endpoints for receiving data updates from Totalmobile. We can then use these data updates to update the Blaise data. The endpoints have basic authenication, the username and password (hashed) are set as environment variables. The dynamic HTTP adapter can be configured from the Totalmobile UI.

### Endpoints 

Endpoints can be found in app/endpoints.py and are as follows:

* "/ons/totalmobile-incoming/SubmitFormResultRequest"
* "/ons/totalmobile-incoming/UpdateVisitStatusRequest"
* "/ons/totalmobile-incoming/CompleteVisitRequest"

Now commonly referred to as "Update", "Submit" and "Complete".

These are the endpoints to which Totalmobile's event-driven processes will post JSON payloads.

### Payloads

Sample payloads can be found in test/conftest.py under:

* def submit_form_result_request_sample()
* def upload_visit_status_request_sample()
* def complete_visit_request_sample()

Field interviewer name has been replaced with jane.doe and some GUIDs and IDs were replaced.

### IDs

The unique identifier for the endpoint payloads are as follows:

* Update - ["Identity"]["Reference"]
* Complete - ["Identity"]["Reference"]
* Submit - ["Result"]["Association"]["Reference"]

These IDs are the job reference we set when sending data to Totalmobile and is should be constructed from the questionnaire name and case ID. This is how we will link the data back to the Blaise data.
