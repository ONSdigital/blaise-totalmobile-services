from google.cloud import datastore


class DatastoreService:
    def __init__(self):
        self._datastore_client = datastore.Client()
        pass

    def get_totalmobile_release_date_records(self) -> list:
        query = self._datastore_client.query(kind="TmReleaseDate")
        return list(query.fetch())
