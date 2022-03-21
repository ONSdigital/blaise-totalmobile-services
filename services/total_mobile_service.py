from data_sources.sqlalchemy import db
from data_sources.sqlalchemy.models import TotalMobile


def update_visit_status_request_service(reference):
    try:
        insert_record(reference, "UPDATED")
        print(f"Successfully logged update visit status request: {select_row(reference)}")
    except Exception as err:
        print(f"Failed to update visit status: {err}")
        return err, 500
    return "", 200


def submit_form_result_request_service(reference):
    try:
        update_record(reference, "SUBMITTED")
        print(f"Successfully logged submit form result request: {select_row(reference)}")
    except Exception as err:
        print(f"Failed to submit form result: {err}")
        return err, 500
    return "", 200


def complete_visit_request_service(reference):
    try:
        update_record(reference, "COMPLETED")
        print(f"Successfully logged complete visit request: {select_row(reference)}")
    except Exception as err:
        print(f"Failed to submit form result: {err}")
        return err, 500
    return "", 200


def insert_record(reference, status):
    record = TotalMobile(reference=reference, status=status)
    db.session.add(record)
    db.session.commit()


def update_record(reference, status):
    record = select_row(reference)
    record.status = status
    db.session.commit()


def select_row(reference):
    return db.session.query(TotalMobile).filter(TotalMobile.reference == reference).one()
