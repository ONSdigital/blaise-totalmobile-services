from models.create.cma.blaise_cma_frs_create_case_model import FRSCaseModel


def test_format_data_fields_returns_a_correctly_formatted_data_fields_for_frs_case():
    # Arrange
    user = "User1"
    questionnaire_name = "FRS2410A"
    guid = "a0e2f264-14e4-4151-b12d-bb3331674624"
    case_id = "100100"
    custom_use = ""
    location = ""
    inPosession = ""
    prem1 = "prem1"
    prem2 = "prem2"
    town = "town"
    postcode = "NP10 8XG"

    frs_case_for_cma_launcher = FRSCaseModel(
        user,
        questionnaire_name,
        guid,
        case_id,
        custom_use,
        location,
        inPosession,
        prem1,
        prem2,
        town,
        postcode,
    )

    # Act
    formatted_data_fields = frs_case_for_cma_launcher.format_data_fields()

    # Assert
    assert formatted_data_fields == {
        "mainSurveyID": guid,
        "surveyDisplayName": questionnaire_name,
        "id": case_id,
        "cmA_ForWhom": user,
        "cmA_EndDate": "11-11-2024",
        "cmA_CustomUse": "",
        "cmA_Location": "",
        "cmA_InPossession": "",
        "cmA_ContactData": f"PII.TLA\tFRS\tPII.Month\tOctober\tPII.Year\t2024\tPII.Prem1\tprem1\tPII.Prem2\tprem2\tPII.Town\ttown\tPII.Postcode\tNP10 8XG",
    }
