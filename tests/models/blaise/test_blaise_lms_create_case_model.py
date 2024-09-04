from enums.blaise_fields import BlaiseFields
from models.create.blaise.blaise_lms_create_case_model import BlaiseLMSCreateCaseModel
from models.create.blaise.questionnaire_uac_model import UacChunks
from tests.helpers.blaise_case_model_helper import BlaiseCaseModelHelper


def test_create_case_description_for_interviewer_returns_a_correctly_formatted_description():
    # Arrange
    questionnaire_name = "LMS2201_AA1"
    uac_chunks = UacChunks(uac1="3456", uac2="3453", uac3="4546")
    questionnaire_case = BlaiseLMSCreateCaseModel(
        questionnaire_name,
        {
            BlaiseFields.case_id: "12345",
            BlaiseFields.data_model_name: "LMS2201_AA1",
            BlaiseFields.wave_com_dte: "31-01-2022",
            BlaiseFields.wave: "4",
        },
        uac_chunks,
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
    questionnaire_name = "LMS2201_AA1"
    uac_chunks = UacChunks(uac1="3456", uac2="3453", uac3="4546", uac4="0987")
    questionnaire_case = BlaiseLMSCreateCaseModel(
        questionnaire_name,
        {
            BlaiseFields.case_id: "12345",
            BlaiseFields.data_model_name: "LMS2201_AA1",
            BlaiseFields.wave_com_dte: "31-01-2022",
            BlaiseFields.wave: "4",
        },
        uac_chunks,
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == (
        "UAC: 3456 3453 4546 0987\n"
        "Due Date: 31/01/2022\n"
        "Study: LMS2201_AA1\n"
        "Case ID: 12345\n"
        "Wave: 4"
    )


def test_ccreate_case_description_for_interviewer_returns_a_correctly_formatted_description_when_all_values_are_empty():
    # Arrange
    questionnaire_name = "LMS2201_AA1"
    questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
        questionnaire_name=questionnaire_name,
        case_id="1234",
        data_model_name="",
        wave_com_dte="",
        wave="",
        uac_chunks=None,
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == (
        "UAC: \n" "Due Date: \n" "Study: LMS2201_AA1\n" "Case ID: 1234\n" "Wave: "
    )
