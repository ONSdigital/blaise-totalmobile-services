import logging

from datetime import datetime
from unittest import mock
from cloud_functions.check_questionnaire_release_date import check_questionnaire_release_date, get_questionnaires_with_todays_release_date, map_questionnaire_case_task_models, QuestionnaireCaseTaskModel, create_questionnaire_case_task_name
from google.cloud import datastore


def entity_builder(key, questionnaire, tmreleasedate):
    entity = datastore.Entity(
        datastore.Key("TmReleaseDate", key, project="test")
    )
    entity["questionnaire"] = questionnaire
    entity["tmreleasedate"] = tmreleasedate
    return entity


@mock.patch("cloud_functions.check_questionnaire_release_date.get_datastore_records")
def test_get_questionnaires_with_todays_release_date_only_returns_questionnaires_with_todays_date(mock_get_datastore_records):
    # arrange
    mock_datastore_entity = [
        entity_builder(
            1, "LMS2111Z", datetime.today()
        ),
        entity_builder(
            2, "LMS2000Z", datetime(2021, 12, 31)
        )
    ]
    mock_get_datastore_records.return_value = mock_datastore_entity

    # act
    result = get_questionnaires_with_todays_release_date()

    # assert
    assert result == ["LMS2111Z"]


@mock.patch("cloud_functions.check_questionnaire_release_date.get_datastore_records")
def test_get_questionnaires_with_todays_release_date_returns_an_empty_list_when_there_are_no_release_dates_for_today(mock_get_datastore_records):
    # arrange
    mock_datastore_entity = [
        entity_builder(
            1, "LMS2111Z", datetime(2021, 12, 31)
        ),
        entity_builder(
            2, "LMS2000Z", datetime(2021, 12, 31)
        )
    ]
    mock_get_datastore_records.return_value = mock_datastore_entity

    # act
    result = get_questionnaires_with_todays_release_date()

    # assert
    assert result == []


@mock.patch("cloud_functions.check_questionnaire_release_date.get_datastore_records")
def test_get_questionnaires_with_todays_release_date_returns_an_empty_list_when_there_are_no_records_in_datastore(mock_get_datastore_records):
    # arrange
    mock_get_datastore_records.return_value = []

    # act
    result = get_questionnaires_with_todays_release_date()

    # assert
    assert result == []


@mock.patch("cloud_functions.check_questionnaire_release_date.get_questionnaires_with_todays_release_date")
def test_check_questionnaire_returns_when_there_are_no_questionnaire_for_release(mock_get_questionnaires_with_todays_release_date, caplog):
    # arrange
    mock_get_questionnaires_with_todays_release_date.return_value = []

    # act
    result = check_questionnaire_release_date()

    # assert
    assert result == "There are no questionnaires for release today"
    assert ('root', logging.INFO, 'There are no questionnaires for release today') in caplog.record_tuples


def test_map_questionnaire_case_task_models_maps_the_correct_list_of_models():
    # arrange
    todays_questionnaires_for_release = ["LMS2111Z", "LMS2112T"]

    # act
    result = map_questionnaire_case_task_models(todays_questionnaires_for_release)

    # assert
    assert result == [QuestionnaireCaseTaskModel(questionnaire="LMS2111Z"), QuestionnaireCaseTaskModel(questionnaire="LMS2112T")]


def test_create_questionnaire_case_task_name_returns_unique_name_each_time_when_passed_the_same_model():
    # arrange
    model = QuestionnaireCaseTaskModel("LMS2101A")

    # act
    result1 = create_questionnaire_case_task_name(model)
    result2 = create_questionnaire_case_task_name(model)

    # assert
    assert result1 != result2
