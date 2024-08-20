from datetime import datetime

from models.create.blaise.questionnaire_uac_model import UacChunks
from tests.helpers.lms_case_model_helper import get_lms_populated_case_model


def test_create_case_description_for_interviewer_returns_a_correctly_formatted_description():
    # Arrange
    questionnaire_case = get_lms_populated_case_model(
        questionnaire_name="LMS2201_AA1",
        case_id="12345",
        data_model_name="LMS2201_AA1",
        wave_com_dte=datetime(2022, 1, 31),
        wave=4,
        uac_chunks=UacChunks(uac1="3456", uac2="3453", uac3="4546"),
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == (
        "UAC: 3456 3453 4546\n"
        "Due Date: 31/01/2022\n"
        "Study: LMS2201_AA1\n"
        "Case ID: 12345\n"
        "Wave: 4"
    )


def test_create_case_description_for_interviewer_returns_a_correctly_formatted_description_when_four_uac_chunks_are_provided():
    # Arrange
    questionnaire_case = get_lms_populated_case_model(
        questionnaire_name="LMS2201_AA1",
        case_id="12345",
        data_model_name="LMS2201_AA1",
        wave_com_dte=datetime(2022, 1, 31),
        wave=4,
        uac_chunks=UacChunks(uac1="1234", uac2="4567", uac3="7890", uac4="0987"),
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == (
        "UAC: 1234 4567 7890 0987\n"
        "Due Date: 31/01/2022\n"
        "Study: LMS2201_AA1\n"
        "Case ID: 12345\n"
        "Wave: 4"
    )


def test_ccreate_case_description_for_interviewer_returns_a_correctly_formatted_description_when_all_values_are_empty():
    # Arrange
    questionnaire_case = get_lms_populated_case_model(
        questionnaire_name="LMS2201_AA1",
        case_id="1234",
        data_model_name="",
        wave_com_dte=None,
        wave="",
        uac_chunks=None,
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == (
        "UAC: \n" "Due Date: \n" "Study: LMS2201_AA1\n" "Case ID: 1234\n" "Wave: "
    )
