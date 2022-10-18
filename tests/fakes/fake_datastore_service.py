from datetime import datetime
from typing import List

from tests.helpers.datastore_helper import DatastoreHelper


class FakeDatastoreService:
    def __init__(self):
        self._datastore_records: List = []

    def add_record(self, questionnaire_name: str, release_date: datetime):
        record = DatastoreHelper.totalmobile_release_date_entity_builder(
            len(self._datastore_records)+1, questionnaire_name, release_date
        )
        self._datastore_records.append(record)

    def get_totalmobile_release_date_records(self) -> list:
        return self._datastore_records
