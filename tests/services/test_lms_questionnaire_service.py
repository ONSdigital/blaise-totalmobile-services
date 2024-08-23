from datetime import datetime
from typing import Dict, Optional
from unittest.mock import Mock

import pytest

from client.bus import Uac
from models.create.blaise.blaiise_lms_case_model import BlaiseLMSCaseModel
from models.create.blaise.questionnaire_uac_model import (
    QuestionnaireUacModel,
    UacChunks,
)
from services.create.questionnaires.lms_questionnaire_service import (
    LMSQuestionnaireService,
)
from tests.helpers.datastore_helper import DatastoreHelper


def get_case(case_id: str, uac_chunks: Optional[UacChunks]) -> BlaiseLMSCaseModel:
    return BlaiseLMSCaseModel(
        "LMS2101_AA1",
        {
            "qiD.Serial_Number": case_id,
            "qDataBag.FieldRegion": "Region 1",
            "hOut": "0",
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
            "qDataBag.WaveComDTE": "31-01-2023",
            "qDataBag.priority": "1",
        },
        uac_chunks=uac_chunks,
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
def mock_uac_service():
    return Mock()


@pytest.fixture()
def questionnaire_uac_model() -> QuestionnaireUacModel:
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8175",
                "uac2": "4725",
                "uac3": "3990",
                "uac4": "None",
            },
            "full_uac": "817647263991",
        }
    }

    questionnaire_uac_model = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)
    return questionnaire_uac_model


@pytest.fixture()
def service(
    mock_blaise_service,
    mock_mapper_service,
    mock_eligible_case_service,
    mock_datastore_service,
    mock_uac_service,
) -> LMSQuestionnaireService:
    return LMSQuestionnaireService(
        blaise_service=mock_blaise_service,
        eligible_case_service=mock_eligible_case_service,
        datastore_service=mock_datastore_service,
        uac_service=mock_uac_service,
    )


def test_get_eligible_cases_calls_the_services_with_the_correct_parameters(
    mock_blaise_service,
    mock_mapper_service,
    mock_eligible_case_service,
    service: LMSQuestionnaireService,
):
    questionnaire_cases = [
        get_case(case_id="20001", uac_chunks=None),
        get_case(case_id="20003", uac_chunks=None),
    ]

    eligible_cases = [questionnaire_cases[0]]

    mock_mapper_service.map_lms_case_information_models.return_value = (
        questionnaire_cases
    )
    mock_eligible_case_service.get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "LMS2101_AA1"
    required_fields = BlaiseLMSCaseModel.required_fields()

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
    mock_mapper_service,
    mock_eligible_case_service,
    service: LMSQuestionnaireService,
):
    questionnaire_cases = [
        get_case(case_id="20001", uac_chunks=None),
        get_case(case_id="20003", uac_chunks=None),
    ]

    eligible_cases = [questionnaire_cases[0]]

    mock_mapper_service.map_lms_case_information_models.return_value = (
        questionnaire_cases
    )
    mock_eligible_case_service.get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "LMS2101_AA1"

    # act
    result = service.get_eligible_cases(questionnaire_name)

    # assert
    assert result == eligible_cases


def test_get_cases_returns_a_list_of_fully_populated_cases(
    service: LMSQuestionnaireService,
    mock_mapper_service,
):
    questionnaire_cases = [
        get_case(case_id="20001", uac_chunks=None),
        get_case(case_id="20003", uac_chunks=None),
    ]

    mock_mapper_service.map_lms_case_information_models.return_value = (
        questionnaire_cases
    )

    questionnaire_name = "LMS2101_AA1"

    # act
    result = service.get_cases(questionnaire_name)

    # assert
    assert result == questionnaire_cases


def test_get_case_returns_a_case(
    service: LMSQuestionnaireService,
    mock_mapper_service,
):
    questionnaire_case = get_case(case_id="10010", uac_chunks=None)

    mock_mapper_service.map_lms_case_information_model.return_value = questionnaire_case

    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"

    # act
    result = service.get_case(questionnaire_name, case_id)

    # assert
    assert result == questionnaire_case


def test_get_case_returns_a_case_calls_the_correct_services(
    service: LMSQuestionnaireService,
    mock_blaise_service,
    mock_mapper_service,
    mock_uac_service,
):
    questionnaire_case = get_case(case_id="10010", uac_chunks=None)
    data_fields = {
        "hOut": "110",
        "dMktnName": "John Smith",
        "qDataBag.TelNo": "01234 567890",
        "qDataBag.TelNo2": "07734 567890",
    }

    mock_blaise_service.get_case.return_value = data_fields

    mock_mapper_service.map_lms_case_information_model.return_value = questionnaire_case

    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"

    # act
    service.get_case(questionnaire_name, case_id)

    # assert
    mock_uac_service.get_questionnaire_uac_model.assert_not_called()
    mock_mapper_service.map_lms_case_information_model.assert_called_with(
        questionnaire_name, data_fields, None
    )


def test_get_case_returns_a_case_calls_the_correct_services_when_include_uac_is_true(
    service: LMSQuestionnaireService,
    mock_blaise_service,
    mock_mapper_service,
    mock_uac_service,
):
    questionnaire_case = get_case(case_id="10010", uac_chunks=None)

    data_fields = {
        "hOut": "110",
        "dMktnName": "John Smith",
        "qDataBag.TelNo": "01234 567890",
        "qDataBag.TelNo2": "07734 567890",
    }

    mock_blaise_service.get_case.return_value = data_fields

    mock_uac_service.get_questionnaire_uac_model.return_value = questionnaire_uac_model

    mock_mapper_service.map_lms_case_information_model.return_value = questionnaire_case

    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"

    # act
    service.get_case(questionnaire_name, case_id, True)

    # assert
    mock_uac_service.get_questionnaire_uac_model.assert_called_with(questionnaire_name)
    mock_mapper_service.map_lms_case_information_model.assert_called_with(
        questionnaire_name, data_fields, questionnaire_uac_model
    )


def test_get_questionnaire_uac_model_returns_an_expected_uac_model(
    service: LMSQuestionnaireService,
    questionnaire_uac_model,
    mock_uac_service,
):
    mock_uac_service.get_questionnaire_uac_model.return_value = questionnaire_uac_model

    questionnaire_name = "LMS2101_AA1"

    # act
    result = service.get_questionnaire_uac_model(questionnaire_name)

    # assert
    assert result == questionnaire_uac_model


def test_get_questionnaires_with_totalmobile_release_date_of_today_only_returns_questionnaires_with_todays_date(
    mock_datastore_service,
    service: LMSQuestionnaireService,
):
    # arrange
    mock_datastore_entity_list = [
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "LMS2111Z", datetime.today()
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "LMS2000Z", datetime(2021, 12, 31)
        ),
    ]
    mock_datastore_service.get_totalmobile_release_date_records.return_value = (
        mock_datastore_entity_list
    )

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == ["LMS2111Z"]


def test_get_questionnaires_with_totalmobile_release_date_of_today_only_returns_lms_questionnaires_with_todays_date(
    mock_datastore_service,
    service: LMSQuestionnaireService,
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
            2, "lms2031_aa1", datetime.today()
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "FRS2111z", datetime.today()
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
    assert result == ["LMS2111Z", "lms2031_aa1"]


def test_get_questionnaires_with_totalmobile_release_date_of_today_returns_an_empty_list_when_there_are_no_release_dates_for_today(
    mock_datastore_service,
    service: LMSQuestionnaireService,
):
    # arrange
    mock_datastore_entity_list = [
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "LMS2111Z", datetime(2021, 12, 31)
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "LMS2000Z", datetime(2021, 12, 31)
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
    service: LMSQuestionnaireService,
):
    # arrange
    mock_datastore_service.get_totalmobile_release_date_records.return_value = []

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == []
