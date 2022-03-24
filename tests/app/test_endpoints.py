from data_sources.sqlalchemy import db


def setup():
    db.create_all()


def teardown():
    db.drop_all()


def test_update_visit_status_request_returns_200(client, upload_visit_status_request_sample):
    response = client.post("/ons/totalmobile-incoming/UpdateVisitStatusRequest", json=upload_visit_status_request_sample)
    assert response.status_code == 200


def test_submit_form_result_request_returns_200(client, submit_form_result_request_sample):
    response = client.post("/ons/totalmobile-incoming/SubmitFormResultRequest", json=submit_form_result_request_sample)
    assert response.status_code == 200


def test_complete_visit_request_returns_200(client, complete_visit_request_sample):
    response = client.post("/ons/totalmobile-incoming/CompleteVisitRequest", json=complete_visit_request_sample)
    assert response.status_code == 200
