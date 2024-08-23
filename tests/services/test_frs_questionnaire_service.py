from datetime import datetime
from unittest.mock import Mock

import pytest

from models.create.blaise.blaiise_frs_case_model import BlaiseFRSCaseModel
from services.create.questionnaires.frs_questionnaire_service import (
    FRSQuestionnaireService,
)
from tests.helpers.datastore_helper import DatastoreHelper


def get_case(
    case_id: str,
) -> BlaiseFRSCaseModel:
    return BlaiseFRSCaseModel(
        "FRS2101",
        {
            "qiD.Serial_Number": case_id,
            "qDataBag.FieldRegion": "Region 1",
            "hOut": "110",
            "qDataBag.TelNo": "07900990901",
            "qDataBag.TelNo2": "07900990902",
            "telNoAppt": "07900990903",
            "qDataBag.FieldTeam": "B-Team",
            "dataModelName": "LM2007",
            "qDataBag.Prem1": "12 Blaise Street",
            "qDataBag.Prem2": "Blaise Hill",
            "qDataBag.Prem3": "Blaiseville",
            "qDataBag.District": "Gwent",
            "qDataBag.PostTown": "Newport",
            "qDataBag.PostCode": "cf99rsd",
            "qDataBag.UPRN_Latitude": "10020202",
            "qDataBag.UPRN_Longitude": "34949494",
            "qDataBag.priority": "1",
            "qDataBag.Rand": "1",
        },
    )


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def mock_mapper_service():
    return Mock()


@pytest.fixture()
def mock_eligible_case_service():
    return Mock()


@pytest.fixture()
def mock_datastore_service():
    return Mock()


@pytest.fixture()
def service(
    mock_blaise_service,
    mock_mapper_service,
    mock_eligible_case_service,
    mock_datastore_service,
) -> FRSQuestionnaireService:
    return FRSQuestionnaireService(
        blaise_service=mock_blaise_service,
        eligible_case_service=mock_eligible_case_service,
        datastore_service=mock_datastore_service,
    )


def test_get_eligible_cases_calls_the_services_with_the_correct_parameters(
    mock_blaise_service,
    mock_mapper_service,
    mock_eligible_case_service,
    service: FRSQuestionnaireService,
):
    questionnaire_cases = [
        get_case(case_id="20001"),  # eligible
        get_case(case_id="20002"),  # not eligible
    ]

    eligible_cases = [questionnaire_cases[0]]

    mock_mapper_service.map_frs_case_information_models.return_value = (
        questionnaire_cases
    )
    mock_eligible_case_service.get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "FRS2101"
    required_fields = BlaiseFRSCaseModel.required_fields()

    # act
    service.get_eligible_cases(questionnaire_name)

    # assert
    mock_blaise_service.get_cases.assert_called_with(
        questionnaire_name, required_fields
    )
    mock_eligible_case_service.get_eligible_cases.assert_called_with(
        questionnaire_cases
    )


def test_get_eligible_cases_returns_the_list_of_eligible_cases_from_the_eligible_case_service(
    mock_blaise_service,
    mock_mapper_service,
    mock_eligible_case_service,
    service: FRSQuestionnaireService,
):
    questionnaire_cases = [
        get_case(case_id="20001"),  # eligible
        get_case(case_id="20002"),  # not eligible
    ]
    eligible_cases = [questionnaire_cases[0]]

    mock_mapper_service.map_frs_case_information_models.return_value = (
        questionnaire_cases
    )
    mock_eligible_case_service.get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "FRS2101"

    # act
    result = service.get_eligible_cases(questionnaire_name)

    # assert
    assert result == eligible_cases


def test_get_cases_returns_a_list_of_fully_populated_cases(
    service: FRSQuestionnaireService, mock_blaise_service, mock_mapper_service
):
    questionnaire_cases = [
        get_case(case_id="20001"),  # eligible
        get_case(case_id="20002"),  # not eligible
    ]

    mock_mapper_service.map_frs_case_information_models.return_value = (
        questionnaire_cases
    )

    questionnaire_name = "FRS2101"

    # act
    result = service.get_cases(questionnaire_name)

    # assert
    assert result == questionnaire_cases


def test_get_case_returns_a_case(
    service: FRSQuestionnaireService,
    mock_blaise_service,
    mock_mapper_service,
):
    questionnaire_case = get_case(case_id="10010")

    mock_mapper_service.map_frs_case_information_model.return_value = questionnaire_case

    questionnaire_name = "FRS2101"
    case_id = "10010"

    # act
    result = service.get_case(questionnaire_name, case_id)

    # assert
    assert result == questionnaire_case


def test_get_questionnaires_with_totalmobile_release_date_of_today_only_returns_questionnaires_with_todays_date(
    mock_datastore_service,
    service: FRSQuestionnaireService,
):
    # arrange
    mock_datastore_entity_list = [
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "FRS2111", datetime.today()
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "FSR2000", datetime(2021, 12, 31)
        ),
    ]
    mock_datastore_service.get_totalmobile_release_date_records.return_value = (
        mock_datastore_entity_list
    )

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == ["FRS2111"]


def test_get_questionnaires_with_totalmobile_release_date_of_today_only_returns_frs_questionnaires_with_todays_date(
    mock_datastore_service,
    service: FRSQuestionnaireService,
):
    # arrange
    mock_datastore_entity_list = [
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "LMS2111Z", datetime.today()
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "LMS2000Z", datetime(2021, 12, 31)
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "FRS2111z", datetime.today()
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "frs2031", datetime.today()
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "FRS2000Z", datetime(2021, 12, 31)
        ),
    ]
    mock_datastore_service.get_totalmobile_release_date_records.return_value = (
        mock_datastore_entity_list
    )

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == ["FRS2111z", "frs2031"]


def test_get_questionnaires_with_totalmobile_release_date_of_today_returns_an_empty_list_when_there_are_no_release_dates_for_today(
    mock_datastore_service,
    service: FRSQuestionnaireService,
):
    # arrange
    mock_datastore_entity_list = [
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "FRS2111", datetime(2021, 12, 31)
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "FRS2000", datetime(2021, 12, 31)
        ),
    ]

    mock_datastore_service.get_totalmobile_release_date_records.return_value = (
        mock_datastore_entity_list
    )

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == []


def test_get_questionnaires_with_totalmobile_release_date_of_today_returns_an_empty_list_when_there_are_no_records_in_datastore(
    mock_datastore_service,
    service: FRSQuestionnaireService,
):
    # arrange
    mock_datastore_service.get_totalmobile_release_date_records.return_value = []

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == []
