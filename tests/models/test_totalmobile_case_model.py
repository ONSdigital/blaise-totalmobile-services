from models.totalmobile_case_model import TotalMobileCaseModel, Reference, Skill, AddressDetails, Address, \
    AddressCoordinates, ContactDetails, AdditionalProperty, DueDate
from models.uac_model import UacChunks
from tests.helpers import questionnaire_case_model_helper


def test_import_case_returns_a_populated_model():
    questionnaire_name = "LMS2101_AA1"

    questionnaire_case = questionnaire_case_model_helper.populated_case_model(
        case_id="90001",
        data_model_name="LM2007",
        survey_type="LMS",
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
        outcome_code="301",
        latitude="10020202",
        longitude="34949494",
        priority="1",
        field_region="gwent",
        field_team="B-Team",
        wave_com_dte="01-01-2023",
        uac_chunks=UacChunks(uac1="3456", uac2="3453", uac3="4546")
    )

    result = TotalMobileCaseModel.import_case(questionnaire_name, questionnaire_case)

    assert result.identity.reference == "LMS2101-AA1.90001"
    assert result.description == "Study: LMS2101_AA1\nCase ID: 90001"
    assert result.origin == "ONS"
    assert result.duration == 15
    assert result.workType == "LMS"
    assert result.skills[0].identity.reference == "LMS"
    assert result.dueDate.end == "01-01-2023"
    assert result.location.addressDetail.addressLine1 == "12 Blaise Street"
    assert result.location.addressDetail.addressLine2 == "Blaise Hill"
    assert result.location.addressDetail.addressLine3 == "Blaiseville"
    assert result.location.addressDetail.addressLine4 == "Gwent"
    assert result.location.addressDetail.addressLine5 == "Newport"
    assert result.location.addressDetail.postCode == "FML134D"
    assert result.location.addressDetail.coordinates.latitude == "10020202"
    assert result.location.addressDetail.coordinates.longitude == "34949494"
    assert result.contact.name == "FML134D"

    assert result.additionalProperties[0].name == "surveyName"
    assert result.additionalProperties[0].value == "LM2007"

    assert result.additionalProperties[1].name == "tla"
    assert result.additionalProperties[1].value == "LMS"

    assert result.additionalProperties[2].name == "wave"
    assert result.additionalProperties[2].value == "1"

    assert result.additionalProperties[3].name == "priority"
    assert result.additionalProperties[3].value == "1"

    assert result.additionalProperties[4].name == "fieldTeam"
    assert result.additionalProperties[4].value == "B-Team"

    assert result.additionalProperties[5].name == "uac1"
    assert result.additionalProperties[5].value == "3456"

    assert result.additionalProperties[6].name == "uac2"
    assert result.additionalProperties[6].value == "3453"

    assert result.additionalProperties[7].name == "uac3"
    assert result.additionalProperties[7].value == "4546"


def test_to_payload_returns_a_correctly_formatted_payload():

    totalmobile_case = TotalMobileCaseModel(
        identity=Reference("LMS2101-AA1.90001"),
        description="Study: LMS2101_AA1\nCase ID: 90001",
        origin="ONS",
        duration=15,
        workType="LMS",
        skills=[Skill(identity=Reference("LMS"))],
        dueDate=DueDate(end="01-01-2023"),
        location=AddressDetails(addressDetail=Address(
            addressLine1="12 Blaise Street",
            addressLine2="Blaise Hill",
            addressLine3="Blaiseville",
            addressLine4="Gwent",
            addressLine5="Newport",
            postCode="FML134D",
            coordinates=AddressCoordinates(
                latitude="10020202",
                longitude="34949494")
        )),
        contact=ContactDetails(name="FML134D"),
        additionalProperties=[
            AdditionalProperty(
                name="surveyName",
                value="LM2007"
            ),
            AdditionalProperty(
                name="tla",
                value="LMS"
            ),
            AdditionalProperty(
                name="wave",
                value="1"
            ),
            AdditionalProperty(
                name="priority",
                value="1"
            ),
            AdditionalProperty(
                name="fieldTeam",
                value="B-Team"
            ),
            AdditionalProperty(
                name="uac1",
                value="3456"
            ),
            AdditionalProperty(
                name="uac2",
                value="3453"
            ),
            AdditionalProperty(
                name="uac3",
                value="4546"
            )
        ])

    result = totalmobile_case.to_payload()
    print(result)

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
            "end": "01-01-2023",
        },
        "location": {
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
        "additionalProperties": [
            {
                "name": "surveyName",
                "value": "LM2007"
            },
            {
                "name": "tla",
                "value": "LMS"
            },
            {
                "name": "wave",
                "value":"1"
            },
            {
                "name": "priority",
                "value": "1"
            },
            {
                "name": "fieldTeam",
                "value": "B-Team"
            },
            {
                "name": "uac1",
                "value": "3456"
            },
            {
                "name": "uac2",
                "value": "3453"
            },
            {
                "name": "uac3",
                "value": "4546"
            },
        ],
    }
