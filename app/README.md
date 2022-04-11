# app

A python POC for ingesting data from totalmobile. 

* Endpoints ingest JSON payloads (see test/conftest.py for samples)
* Handlers validate and extract data
* Services currently either print an arbitrary message or call blaise-api-python-client to persist data
* Nothing is returned

### Endpoints

Endpoints can be found in app/endpoints.py and are as follows:

* "/ons/totalmobile-incoming/SubmitFormResultRequest"
* "/ons/totalmobile-incoming/UpdateVisitStatusRequest"
* "/ons/totalmobile-incoming/CompleteVisitRequest"

(Now commonly referred to as "Submit", "Update" and "Complete")

These are the endpoints to which TotalMobile's event-driven process will post JSON payloads.

### Payloads

Sample payloads can be found in test/conftest.py under:

* def submit_form_result_request_sample()
* def upload_visit_status_request_sample()
* def complete_visit_request_sample()

Field interviewer name has been replaced with jane.doe and some GUIDs and IDs were replaced.

## Running

Run run.py. Hook it up to Postman using the localhost address printed in the terminal. 

Alternatively, execute test/app/test_endpoints with pytest. Setting debug points and debugging the tests will help you walk through the flow of data from endpoint to handler to service.

## Future

The following files are part of a POC and were designed to be discarded. When discarding ensure the following files are removed as necessary:

* run.py
* app/
* test/app/

as well as the sample payloads in conftest.py as previously mentioned.

If however these files will be expanded on the following work needs to be completed:

* Securely expose endpoints externally
* Authorise user credentials from request
* Improve logging and error handling (removing duff print statements as necessary)
* Expand tests to include unhappy paths