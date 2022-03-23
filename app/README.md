# app

A python POC for ingesting data from totalmobile. 

* Endpoints ingest JSON payloads (see test/conftest.py for samples)
* Handlers parse data and extract the job reference
* Services persist job reference and custom status to a temporary database (data_sources/sqlalchemy) 
* Empty string or an error message, and a status code is returned

### Endpoints

Endpoints can be found in app/endpoints.py and are as follows:

* "/ons/totalmobile-incoming/UpdateVisitStatusRequest"
* "/ons/totalmobile-incoming/SubmitFormResultRequest"
* "/ons/totalmobile-incoming/CompleteVisitRequest"

(Now commonly referred to as "Update", "Submit" and "Complete")

These are the endpoints to which TotalMobile's event-driven process will post JSON payloads.

### Payloads

Sample payloads can be found in test/conftest.py under:

* def upload_visit_status_request_sample()
* def submit_form_result_request_sample()
* def complete_visit_request_sample()

Field interviewer name has been replaced with jane.doe and some GUIDs and IDs were replaced.

### IDs

The only common ID found across all sample payloads was "reference". For the Update and Complete endpoints/payloads reference can be found under JSON["Identity"]["Reference"] whereas for the Submit endpoint it can be found under JSON["Result"]["Association"]["Reference"].

I'm making the wild assumption this reference is the job-reference and, given the choice, this should be constructed from the instrument name and case id.  We need to easily identify cases.

## Running

Execute test/app/test_endpoints with pytest or test/app/services/test_total_mobile_service.py

## Future

The following files are part of a POC and were designed to be discarded. When discarding ensure the following files are removed as necessary:

* app/
* data_sources/
* test/app/

as well as the sample payloads in conftest.py as previously mentioned.

If however these files will be expanded on the following work needs to be completed:

* Securely expose endpoints externally
* Authorise user credentials from request
* Improve logging
* Expand tests to include unhappy paths