from google.cloud import datastore


class DatastoreHelper:
    @staticmethod
    def totalmobile_release_date_entity_builder(key, questionnaire, tmreleasedate):
        entity = datastore.Entity(datastore.Key("TmReleaseDate", key, project="test"))
        entity["questionnaire"] = questionnaire
        entity["tmreleasedate"] = tmreleasedate
        return entity
