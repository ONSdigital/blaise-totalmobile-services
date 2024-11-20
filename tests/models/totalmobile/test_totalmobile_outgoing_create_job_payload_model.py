from datetime import datetime

from models.create.totalmobile.totalmobile_outgoing_create_job_payload_model import (
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
            reference="100012675377",
            address="12 Blaise Street, Blaise Hill, Blaiseville, Newport, FML134D",
            addressDetail=Address(
                addressLine1="12 Blaise Street, Blaise Hill",
                addressLine2="Blaiseville",
                addressLine3="Gwent",
                addressLine4="Newport",
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
            AdditionalProperty(name="LAUA", value="Loco"),
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
            "reference": "100012675377",
            "address": "12 Blaise Street, Blaise Hill, Blaiseville, Newport, FML134D",
            "addressDetail": {
                "addressLine1": "12 Blaise Street, Blaise Hill",
                "addressLine2": "Blaiseville",
                "addressLine3": "Gwent",
                "addressLine4": "Newport",
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
            {"name": "LAUA", "value": "Loco"},
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


def test_to_payload_returns_a_correctly_formatted_payload_when_four_uac_chunks_provided():
    totalmobile_case = TotalMobileOutgoingCreateJobPayloadModel(
        identity=Reference("LMS2101-AA1.90001"),
        description="Study: LMS2101_AA1\nCase ID: 90001",
        origin="ONS",
        duration=15,
        workType="LMS",
        skills=[Skill(identity=Reference("LMS"))],
        dueDate=DueDate(end=datetime(2023, 1, 31)),
        location=AddressDetails(
            reference="100012675377",
            address="12 Blaise Street, Blaise Hill, Blaiseville, Newport, FML134D",
            addressDetail=Address(
                addressLine1="12 Blaise Street, Blaise Hill",
                addressLine2="Blaiseville",
                addressLine3="Gwent",
                addressLine4="Newport",
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
            AdditionalProperty(name="uac1", value="1234"),
            AdditionalProperty(name="uac2", value="4567"),
            AdditionalProperty(name="uac3", value="7890"),
            AdditionalProperty(name="uac4", value="0987"),
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
            "reference": "100012675377",
            "address": "12 Blaise Street, Blaise Hill, Blaiseville, Newport, FML134D",
            "addressDetail": {
                "addressLine1": "12 Blaise Street, Blaise Hill",
                "addressLine2": "Blaiseville",
                "addressLine3": "Gwent",
                "addressLine4": "Newport",
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
            {"name": "uac1", "value": "1234"},
            {"name": "uac2", "value": "4567"},
            {"name": "uac3", "value": "7890"},
            {"name": "uac4", "value": "0987"},
        ],
    }
