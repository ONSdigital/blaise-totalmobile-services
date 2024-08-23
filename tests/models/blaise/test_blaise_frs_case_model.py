from models.create.blaise.blaiise_frs_case_model import BlaiseFRSCaseModel


def test_create_case_description_for_interviewer_returns_a_correctly_formatted_description():
    # Arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, {})

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == ""


def test_create_case_description_for_interviewer_returns_divided_address_if_indicator_is_1():
    # Arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCaseModel(
        questionnaire_name, {"qDataBag.DivAddInd": "1"}
    )

    # Act
    description = questionnaire_case.create_case_description_for_interviewer()

    # Assert
    assert description == "Warning Divided Address"


def test_create_case_overview_for_interviewer_returns_the_expected_additional_properties():
    # arrange
    questionnaire_name = "FRS2201"
    questionnaire_case = BlaiseFRSCaseModel(
        questionnaire_name,
        {
            "qDataBag.Rand": "30",
            "qDataBag.FieldRegion": "Region 2",
            "qDataBag.FieldTeam": "A Team",
            "qDataBag.PostCode": "AB01 2CD",
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
