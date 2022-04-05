expected_messages = [
    'This is a basic placeholder per BLAIS5-3071',
    'We gots data!',
    'This is completely arbitrary data',
    'The reference number is: SLC-12345-678-910',
    'There are no solid requirements for this feature. You shall not pass!'
]


def test_submit_form_result_request_returns_200():
    # TODO
    pass


def test_update_visit_status_request_returns_200(capsys, client, upload_visit_status_request_sample):
    client.post("/ons/totalmobile-incoming/UpdateVisitStatusRequest", json=upload_visit_status_request_sample)
    actual_messages, err = capsys.readouterr()
    assert expected_messages == actual_messages.splitlines()


def test_complete_visit_request_returns_200(capsys, client, complete_visit_request_sample):
    client.post("/ons/totalmobile-incoming/UpdateVisitStatusRequest", json=complete_visit_request_sample)
    actual_messages, err = capsys.readouterr()
    assert expected_messages == actual_messages.splitlines()
