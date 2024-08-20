from datetime import datetime

from google.cloud import datastore


class DatastoreService:
    def get_totalmobile_release_date_records(self) -> list:
        datastore_client = datastore.Client()
        query = datastore_client.query(kind="TmReleaseDate")
        return list(query.fetch())
