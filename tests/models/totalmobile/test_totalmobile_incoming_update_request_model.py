import pytest

from app.exceptions.custom_exceptions import MissingReferenceError, BadReferenceError
from models.totalmobile.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel
from tests.helpers import incoming_request_helper


def test_incoming_request_maps_correctly():
    # arrange
    request = {
   "Result":{
      "User":{
         "ID":1191,
         "IDSpecified":True,
         "Name":"richmond.rice",
         "DeviceID":"NOKIA8.35G9b080ab9-33a4-4824-b882-6019732b9dfa",
         "UserAttributes":[
            {
               "Name":"Skill",
               "Value":"LMS"
            }
         ]
      },
      "Date":"2022-08-23T15:16:46.817",
      "Form":{
         "Reference":"LMS-Contact Made No Visit",
         "Version":10
      },
      "Association":{
         "WorkType":"LMS",
         "Reference":"LMS2208-EJ1.801032",
         "PropertyReference":"zz00zzons",
         "ClientReference":""
      },
      "Responses":[
         {
            "Instance":0,
            "Responses":[
               {
                  "Value":"300-10",
                  "Description":None,
                  "Element":{
                     "Reference":"Secondary_Outcome",
                     "Text":"Contact Made Detail",
                     "EnrichContentSpecified":False
                  }
               },
               {
                  "Value":"300",
                  "Description":None,
                  "Element":{
                     "Reference":"Primary_Outcome",
                     "Text":"Primary Outcome (Hidden)",
                     "EnrichContentSpecified":False
                  }
               }
            ],
            "Element":{
               "Reference":"LMS_CMNV",
               "Text":"Contact Made No Visits",
               "EnrichContentSpecified":False
            }
         },
         {
            "Instance":0,
            "Responses":[
               {
                  "Value":"x",
                  "Description":None,
                  "Element":{
                     "Reference":"Contact_Name",
                     "Text":"Name:",
                     "EnrichContentSpecified":False
                  }
               },
               {
                  "Value":"0",
                  "Description":None,
                  "Element":{
                     "Reference":"Contact_Tel1",
                     "Text":"Tel no 1:",
                     "EnrichContentSpecified":False
                  }
               },
               {
                  "Value":"0",
                  "Description":None,
                  "Element":{
                     "Reference":"Contact_Tel2",
                     "Text":"Tel no 2:",
                     "EnrichContentSpecified":False
                  }
               }
            ],
            "Element":{
               "Reference":"LMS_CD",
               "Text":"Contact Details",
               "EnrichContentSpecified":False
            }
         }
      ],
      "ResultGuid":"aa320618-6139-454c-aca4-4ccfa025d97c"
   }
}
    # act
    result = TotalMobileIncomingUpdateRequestModel.import_request(request)

    # assert
    assert result.questionnaire_name == "LMS2208_EJ1"
    assert result.case_id == "801032"


def test_import_case_returns_a_populated_model():
    # arrange
    reference = "LMS2101_AA1.90001"
    outcome_code = 300
    contact_name= "Duncan Bell"
    home_phone_number = "01234567890"
    mobile_phone_number = "07123123123"

    update_case_request = incoming_request_helper.get_populated_update_case_request(
        reference=reference,
        outcome_code=outcome_code,
        contact_name=contact_name,
        home_phone_number=home_phone_number,
        mobile_phone_number=mobile_phone_number)

    # act
    result = TotalMobileIncomingUpdateRequestModel.import_request(update_case_request)

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id == "90001"
    assert result.outcome_code == outcome_code
    assert result.contact_name == contact_name
    assert result.home_phone_number == home_phone_number
    assert result.mobile_phone_number == mobile_phone_number


def test_import_case_raises_a_missing_reference_error_if_the_request_does_not_have_expected_root_element():
    # arrange

    update_case_request = {}

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingUpdateRequestModel.import_request(update_case_request)


def test_import_case_raises_a_missing_reference_error_if_the_request_does_not_have_expected_association_element():
    # arrange

    update_case_request = incoming_request_helper.get_update_case_request_without_association_element()

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingUpdateRequestModel.import_request(update_case_request)


def test_import_case_raises_a_missing_reference_error_if_the_request_does_not_have_expected_reference_element():
    # arrange

    update_case_request = incoming_request_helper.get_update_case_request_without_reference_element()

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingUpdateRequestModel.import_request(update_case_request)


def test_import_case_raises_a_missing_reference_error_if_the_request_has_an_empty_reference():
    # arrange
    reference = ""
    update_case_request = incoming_request_helper.get_populated_update_case_request(reference=reference)

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingUpdateRequestModel.import_request(update_case_request)


@pytest.mark.parametrize("reference", [" ", "LMS2101_AA1-90001", "LMS2101_AA1:90001", "LMS2101_AA1.", ".90001"])
def test_import_case_raises_a_bad_reference_error_if_the_request_does_not_have_a_correctly_formatted_reference(reference):
    # arrange
    update_case_request = incoming_request_helper.get_populated_update_case_request(reference=reference)

    # assert
    with pytest.raises(BadReferenceError):
        TotalMobileIncomingUpdateRequestModel.import_request(update_case_request)
