from data_sources.sqlalchemy import db
from data_sources.sqlalchemy.models import TotalMobile


def persist_request_service(reference, status):
    if record_exists(reference):
        return update_record(reference, status)
    return insert_record(reference, status)


def record_exists(reference):
    return bool(TotalMobile.query.filter_by(reference=reference).first())


def insert_record(reference, status):
    try:
        record = TotalMobile(reference=reference, status=status)
        db.session.add(record)
        db.session.commit()
        print(f"Successfully inserted record: {record_details(reference)}")
        return "", 200
    except Exception as err:
        print(f"Could not insert record {reference}: {err}")
        return err, 500


def update_record(reference, status):
    try:
        record = record_details(reference)
        record.status = status
        db.session.commit()
        print(f"Successfully updated record: {record_details(reference)}")
        return "", 200
    except Exception as err:
        print(f"Could not update record {reference}: {err}")
        return err, 500


def record_details(reference):
    return (
        db.session.query(TotalMobile).filter(TotalMobile.reference == reference).one()
    )
