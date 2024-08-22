from tests.helpers.frs_case_model_helper import get_frs_populated_case_model


def test_create_case_description_for_interviewer_returns_a_correctly_formatted_description():
    # Arrange
    questionnaire_case = get_frs_populated_case_model(
        questionnaire_name="FRS2201",
        case_id="12345",
        divided_address_indicator="0",
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == ""


def test_create_case_description_for_interviewer_returns_divided_address_if_indicator_is_1():
    # Arrange
    questionnaire_case = get_frs_populated_case_model(
        questionnaire_name="FRS2201",
        case_id="12345",
        divided_address_indicator="1",
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == "Warning Divided Address"


def test_create_case_overview_for_interviewer_returns_the_expected_additional_properties():
    # arrange
    questionnaire_case = get_frs_populated_case_model(
        data_model_name="FRS2407a",
        tla="FRS",
        priority="2",
        field_region="Region 2",
        field_team="A Team",
        postcode="AB01 2CD",
        rand="30",
    )

    # act
    additional_properties = questionnaire_case.create_case_overview_for_interviewer()

    # assert
    assert additional_properties == {
        "surveyName": "FRS2407a",
        "tla": "FRS",
        "priority": "2",
        "fieldRegion": "Region 2",
        "fieldTeam": "A Team",
        "postCode": "AB01 2CD",
        "rand": "30",
    }
