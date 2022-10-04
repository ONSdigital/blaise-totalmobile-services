from google.cloud import datastore


class DatastoreService:
    @staticmethod
    def get_totalmobile_release_date_records() -> list:
        datastore_client = datastore.Client()
        query = datastore_client.query(kind="TmReleaseDate")
        return list(query.fetch())
