import pytest

from app.services.total_mobile_service import (
    insert_record,
    record_exists,
    update_record,
)
from data_sources.sqlalchemy import db
from data_sources.sqlalchemy.models import TotalMobile

test_reference = "LMS-123-456"


def setup():
    db.create_all()
    record = TotalMobile(reference=test_reference, status="a_status")
    db.session.add(record)
    db.session.commit()


@pytest.mark.parametrize(
    "reference_id, expected",
    [
        ("foo", False),
        (test_reference, True),
        ("bar", False),
    ],
)
def test_record_exists(reference_id, expected):
    assert record_exists(reference_id) is expected


def test_update_record_happy_path():
    error_message, code = update_record(test_reference, "new_status")

    assert record_exists(test_reference)
    assert error_message == ""
    assert code == 200


def test_insert_record_happy_path():
    new_reference = "OPN-123-456"
    error_message, code = insert_record(new_reference, "shiny_new_status")

    assert record_exists(test_reference)
    assert error_message == ""
    assert code == 200


def teardown():
    db.drop_all()
