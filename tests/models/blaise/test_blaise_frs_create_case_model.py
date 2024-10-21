from enums.blaise_fields import BlaiseFields
from models.create.blaise.blaise_frs_create_case_model import BlaiseFRSCreateCaseModel


def test_create_case_description_for_interviewer_returns_a_correctly_formatted_description():
    # Arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCreateCaseModel(questionnaire_name, {})

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == ""


def test_create_case_description_for_interviewer_returns_divided_address_if_indicator_is_1():
    # Arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCreateCaseModel(
        questionnaire_name, {BlaiseFields.divided_address_indicator: "1"}
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == f"Warning - Divided Address\nStart date: 01-01-2022"


def test_create_case_description_for_interviewer_returns_divided_address_if_indicator_is_0():
    # Arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCreateCaseModel(
        questionnaire_name, {BlaiseFields.divided_address_indicator: "0"}
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == f"Start date: 01-01-2022"


def test_create_case_description_for_interviewer_returns_divided_address_if_indicator_is_not_1_or_0():
    # Arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCreateCaseModel(
        questionnaire_name, {BlaiseFields.divided_address_indicator: "foo"}
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == ""


def test_create_case_overview_for_interviewer_returns_the_expected_additional_properties():
    # arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCreateCaseModel(
        questionnaire_name,
        {
            BlaiseFields.rand: "30",
            BlaiseFields.field_region: "Region 2",
            BlaiseFields.field_team: "A Team",
            BlaiseFields.postcode: "AB01 2CD",
        },
    )

    # act
    additional_properties = questionnaire_case.create_case_overview_for_interviewer()

    # assert
    assert additional_properties == {
        "tla": "FRS",
        "rand": "30",
        "fieldRegion": "Region 2",
        "fieldTeam": "A Team",
        "postCode": "AB01 2CD",
    }
