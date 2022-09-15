from datetime import datetime

import pytest

from models.blaise.uac_model import UacChunks
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    AdditionalProperty,
    Address,
    AddressCoordinates,
    AddressDetails,
    ContactDetails,
    DueDate,
    Reference,
    Skill,
    TotalMobileOutgoingCreateJobPayloadModel,
)
from tests.helpers import get_blaise_case_model_helper


def test_import_case_returns_a_populated_model():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        case_id="90001",
        data_model_name="LM2007",
        wave="1",
        address_line_1="12 Blaise Street",
        address_line_2="Blaise Hill",
        address_line_3="Blaiseville",
        county="Gwent",
        town="Newport",
        postcode="FML134D",
        telephone_number_1="07900990901",
        telephone_number_2="07900990902",
        appointment_telephone_number="07900990903",
        outcome_code=301,
        latitude="10020202",
        longitude="34949494",
        priority="1",
        field_region="Gwent",
        field_team="B-Team",
        wave_com_dte=datetime(2023, 1, 31),
        uac_chunks=UacChunks(uac1="3456", uac2="3453", uac3="4546"),
    )

    # act
    result = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )

    # assert
    assert result.identity.reference == "LMS2101-AA1.90001"
    assert result.description == (
        "UAC: 3456 3453 4546\n"
        "Due Date: 31/01/2023\n"
        "Study: LMS2101_AA1\n"
        "Case ID: 90001"
    )
    assert result.origin == "ONS"
    assert result.duration == 15
    assert result.workType == "LMS"
    assert result.skills[0].identity.reference == "LMS"
    assert result.dueDate.end == datetime(2023, 1, 31)
    assert result.location.addressDetail.addressLine1 == "12 Blaise Street"
    assert result.location.addressDetail.addressLine2 == "Blaise Hill"
    assert result.location.addressDetail.addressLine3 == "Blaiseville"
    assert result.location.addressDetail.addressLine4 == "Gwent"
    assert result.location.addressDetail.addressLine5 == "Newport"
    assert result.location.addressDetail.postCode == "FML134D"
    assert result.location.addressDetail.coordinates.latitude == "10020202"
    assert result.location.addressDetail.coordinates.longitude == "34949494"
    assert result.contact.name == "FML134D"

    assert result.attributes[0].name == "Region"
    assert result.attributes[0].value == "Gwent"

    assert result.attributes[1].name == "Team"
    assert result.attributes[1].value == "B-Team"

    assert result.additionalProperties[0].name == "surveyName"
    assert result.additionalProperties[0].value == "LM2007"

    assert result.additionalProperties[1].name == "tla"
    assert result.additionalProperties[1].value == "LMS"

    assert result.additionalProperties[2].name == "wave"
    assert result.additionalProperties[2].value == "1"

    assert result.additionalProperties[3].name == "priority"
    assert result.additionalProperties[3].value == "1"

    assert result.additionalProperties[4].name == "fieldRegion"
    assert result.additionalProperties[4].value == "Gwent"

    assert result.additionalProperties[5].name == "fieldTeam"
    assert result.additionalProperties[5].value == "B-Team"

    assert result.additionalProperties[6].name == "uac1"
    assert result.additionalProperties[6].value == "3456"

    assert result.additionalProperties[7].name == "uac2"
    assert result.additionalProperties[7].value == "3453"

    assert result.additionalProperties[8].name == "uac3"
    assert result.additionalProperties[8].value == "4546"


def test_import_case_returns_a_model_with_no_uac_additional_properties_if_no_uacs_are_set():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        uac_chunks=None
    )

    # act
    result = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )

    # assert
    for additional_property in result.additionalProperties:
        assert additional_property.name.startswith("uac") is False


@pytest.mark.parametrize(
    "latitude, longitude",
    [
        ("", "10020202"),
        ("10020202", ""),
        (None, "10020202"),
        ("10020202", None),
        ("", ""),
        (None, None),
    ],
)
def test_import_case_does_not_populate_lat_and_lon_if_both_are_not_supplied(
    latitude: str, longitude: str
):
    # arrange
    questionnaire_name = "LMS2101_AA1"

    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        latitude=latitude, longitude=longitude
    )

    # act
    result = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )

    # assert
    assert result.location.addressDetail.coordinates.latitude is None
    assert result.location.addressDetail.coordinates.longitude is None


def test_to_payload_returns_a_correctly_formatted_payload():
    totalmobile_case = TotalMobileOutgoingCreateJobPayloadModel(
        identity=Reference("LMS2101-AA1.90001"),
        description="Study: LMS2101_AA1\nCase ID: 90001",
        origin="ONS",
        duration=15,
        workType="LMS",
        skills=[Skill(identity=Reference("LMS"))],
        dueDate=DueDate(end=datetime(2023, 1, 31)),
        location=AddressDetails(
            address="12 Blaise Street, Blaise Hill, Blaiseville, Newport, FML134D",
            addressDetail=Address(
                addressLine1="12 Blaise Street",
                addressLine2="Blaise Hill",
                addressLine3="Blaiseville",
                addressLine4="Gwent",
                addressLine5="Newport",
                postCode="FML134D",
                coordinates=AddressCoordinates(
                    latitude="10020202", longitude="34949494"
                ),
            ),
        ),
        contact=ContactDetails(name="FML134D"),
        attributes=[
            AdditionalProperty(name="Region", value="Gwent"),
            AdditionalProperty(name="Team", value="B-Team"),
        ],
        additionalProperties=[
            AdditionalProperty(name="surveyName", value="LM2007"),
            AdditionalProperty(name="tla", value="LMS"),
            AdditionalProperty(name="wave", value="1"),
            AdditionalProperty(name="priority", value="1"),
            AdditionalProperty(name="fieldRegion", value="Gwent"),
            AdditionalProperty(name="fieldTeam", value="B-Team"),
            AdditionalProperty(name="uac1", value="3456"),
            AdditionalProperty(name="uac2", value="3453"),
            AdditionalProperty(name="uac3", value="4546"),
        ],
    )

    # act
    result = totalmobile_case.to_payload()

    # assert
    assert result == {
        "identity": {
            "reference": "LMS2101-AA1.90001",
        },
        "description": "Study: LMS2101_AA1\nCase ID: 90001",
        "origin": "ONS",
        "duration": 15,
        "workType": "LMS",
        "skills": [
            {
                "identity": {
                    "reference": "LMS",
                },
            },
        ],
        "dueDate": {
            "end": "2023-01-31",
        },
        "location": {
            "address": "12 Blaise Street, Blaise Hill, Blaiseville, Newport, FML134D",
            "addressDetail": {
                "addressLine1": "12 Blaise Street",
                "addressLine2": "Blaise Hill",
                "addressLine3": "Blaiseville",
                "addressLine4": "Gwent",
                "addressLine5": "Newport",
                "postCode": "FML134D",
                "coordinates": {
                    "latitude": "10020202",
                    "longitude": "34949494",
                },
            },
        },
        "contact": {
            "name": "FML134D",
        },
        "attributes": [
            {"name": "Region", "value": "Gwent"},
            {"name": "Team", "value": "B-Team"},
        ],
        "additionalProperties": [
            {"name": "surveyName", "value": "LM2007"},
            {"name": "tla", "value": "LMS"},
            {"name": "wave", "value": "1"},
            {"name": "priority", "value": "1"},
            {"name": "fieldRegion", "value": "Gwent"},
            {"name": "fieldTeam", "value": "B-Team"},
            {"name": "uac1", "value": "3456"},
            {"name": "uac2", "value": "3453"},
            {"name": "uac3", "value": "4546"},
        ],
    }


def test_to_payload_sends_an_empty_string_to_totalmobile_if_the_due_date_is_missing():
    questionnaire_name = "LMS2101_AA1"

    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        wave_com_dte=None
    )

    case = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )
    result = case.to_payload()

    assert result["dueDate"]["end"] == ""


def test_create_description_returns_a_correctly_formatted_description():
    # Arrange
    questionnaire_name = "LMS2201_AA1"
    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        case_id="12345",
        data_model_name="LMS2201_AA1",
        wave_com_dte=datetime(2022, 1, 31),
        uac_chunks=UacChunks(uac1="1234", uac2="1235", uac3="1236"),
    )

    # Act
    case = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )

    # Assert
    assert case.description == (
        "UAC: 1234 1235 1236\n"
        "Due Date: 31/01/2022\n"
        "Study: LMS2201_AA1\n"
        "Case ID: 12345"
    )


def test_create_description_returns_a_correctly_formatted_description_when_all_values_are_empty():
    # Arrange
    questionnaire_name = "LMS2201_AA1"
    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        case_id="1234", data_model_name="", wave_com_dte=None, uac_chunks=None
    )

    # Act
    case = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )

    # Assert
    assert case.description == (
        "UAC: \n" "Due Date: \n" "Study: LMS2201_AA1\n" "Case ID: 1234"
    )


def test_concatenate_address_returns_a_concatenated_address_as_a_string_when_all_fields_are_populated():
    # Arrange
    questionnaire_name = "LMS2201_AA1"
    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        case_id="1234",
        address_line_1="123 Blaise Street",
        address_line_2="Blaisville",
        address_line_3="Upper Blaise",
        town="Blaisingdom",
        postcode="BS1 1BS",
    )

    # Act
    case = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )

    # Assert
    assert (
        case.location.address
        == "123 Blaise Street, Blaisville, Upper Blaise, Blaisingdom, BS1 1BS"
    )


def test_concatenate_address_returns_a_concatenated_address_as_a_string_when_not_all_fields_are_populated():
    # Arrange
    questionnaire_name = "LMS2201_AA1"
    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        case_id="1234",
        address_line_1="123 Blaise Street",
        address_line_2="",
        address_line_3=None,
        town="Blaisingdom",
        postcode="BS1 1BS",
    )

    # Act
    case = TotalMobileOutgoingCreateJobPayloadModel.import_case(
        questionnaire_name, questionnaire_case
    )

    # Assert
    assert case.location.address == "123 Blaise Street, Blaisingdom, BS1 1BS"
