import pytest

from models.questionnaire_case_model import QuestionnaireCaseModel
from models.uac_model import UacModel, UacChunks
from tests.helpers import questionnaire_case_model_helper


def test_import_case_data_returns_a_populated_model():
    case_data_dictionary = { 
            "qiD.Serial_Number": "90000000",
            "dataModelName" : "LM2007", 
            "qDataBag.TLA" : "LMS", 
            "qDataBag.Wave" : "1", 
            "qDataBag.Prem1" : "12 Blaise Street", 
            "qDataBag.Prem2" : "Blaise Hill", 
            "qDataBag.Prem3" : "Blaiseville", 
            "qDataBag.District" : "Gwent", 
            "qDataBag.PostTown" : "Newport", 
            "qDataBag.PostCode" : "FML134D", 
            "qDataBag.TelNo" : "07900990901", 
            "qDataBag.TelNo2" : "07900990902", 
            "telNoAppt" : "07900990903", 
            "hOut" : "301", 
            "qDataBag.UPRN_Latitude" : "10020202",
            "qDataBag.UPRN_Longitude" : "34949494", 
            "qDataBag.Priority" : "1", 
            "qDataBag.FieldRegion" : "gwent", 
            "qDataBag.FieldTeam": "B-Team", 
            "qDataBag.WaveComDTE": "WGAFF" 
    }     

    result = QuestionnaireCaseModel.import_case_data(case_data_dictionary)

    assert result.case_id == "90000000"
    assert result.data_model_name == "LM2007"
    assert result.survey_type == "LMS"
    assert result.wave == "1"
    assert result.address_line_1 == "12 Blaise Street"
    assert result.address_line_2 == "Blaise Hill"
    assert result.address_line_3 == "Blaiseville"
    assert result.county == "Gwent"
    assert result.town == "Newport"           
    assert result.postcode == "FML134D"           
    assert result.telephone_number_1 == "07900990901"           
    assert result.telephone_number_2 == "07900990902"           
    assert result.appointment_telephone_number == "07900990903"           
    assert result.outcome_code == "301"                
    assert result.latitude == "10020202"                        
    assert result.longitude == "34949494"    
    assert result.priority == "1"    
    assert result.field_region == "gwent"    
    assert result.field_team == "B-Team"    
    assert result.wave_com_dte == "WGAFF"                        


def test_import_case_data_returns_a_valid_object_when_a_blaise_field_is_incorrectly_typed():
    case_data_dictionary = { 
            "qdatabag.Serial_Number": "90000000",
            "dataModelName" : "LM2007", 
            "qDataBag.TLA" : "LMS", 
            "qDataBag.Wave" : "1", 
            "qDataBag.Prem1" : "12 Blaise Street", 
            "qDataBag.Prem2" : "Blaise Hill", 
            "qDataBag.Prem3" : "Blaiseville", 
            "qDataBag.District" : "Gwent", 
            "qDataBag.PostTown" : "Newport", 
            "qDataBag.PostCode" : "FML134D", 
            "qDataBag.TelNo" : "07900990901", 
            "qDataBag.TelNo2" : "07900990902", 
            "telNoAppt" : "07900990903", 
            "hOut" : "301", 
            "qDataBag.UPRN_Latitude" : "10020202",
            "qDataBag.UPRN_Longitude" : "34949494", 
            "qDataBag.Priority" : "1", 
            "qDataBag.FieldRegion" : "gwent", 
            "qDataBag.FieldTeam": "B-Team", 
            "qDataBag.WaveComDTE": "WGAFF" 
    } 

    result = QuestionnaireCaseModel.import_case_data(case_data_dictionary)

    assert result.case_id is None
    assert result.data_model_name == "LM2007"
    assert result.survey_type == "LMS"
    assert result.wave == "1"
    assert result.address_line_1 == "12 Blaise Street"
    assert result.address_line_2 == "Blaise Hill"
    assert result.address_line_3 == "Blaiseville"
    assert result.county == "Gwent"
    assert result.town == "Newport"           
    assert result.postcode == "FML134D"           
    assert result.telephone_number_1 == "07900990901"           
    assert result.telephone_number_2 == "07900990902"           
    assert result.appointment_telephone_number == "07900990903"           
    assert result.outcome_code == "301"                
    assert result.latitude == "10020202"                        
    assert result.longitude == "34949494"    
    assert result.priority == "1"    
    assert result.field_region == "gwent"    
    assert result.field_team == "B-Team"    
    assert result.wave_com_dte == "WGAFF"         


def test_import_case_data_returns_a_valid_object_when_an_optional_blaise_field_is_missing():
    case_data_dictionary = { 
            "dataModelName" : "LM2007", 
            "qDataBag.TLA" : "LMS", 
            "qDataBag.Wave" : "1", 
            "qDataBag.Prem1" : "12 Blaise Street", 
            "qDataBag.Prem2" : "Blaise Hill", 
            "qDataBag.Prem3" : "Blaiseville", 
            "qDataBag.District" : "Gwent", 
            "qDataBag.PostTown" : "Newport", 
            "qDataBag.PostCode" : "FML134D", 
            "qDataBag.TelNo" : "07900990901", 
            "qDataBag.TelNo2" : "07900990902", 
            "telNoAppt" : "07900990903", 
            "hOut" : "301", 
            "qDataBag.UPRN_Latitude" : "10020202",
            "qDataBag.UPRN_Longitude" : "34949494", 
            "qDataBag.Priority" : "1", 
            "qDataBag.FieldRegion" : "gwent", 
            "qDataBag.FieldTeam": "B-Team", 
            "qDataBag.WaveComDTE": "WGAFF" 
         }        

    result = QuestionnaireCaseModel.import_case_data(case_data_dictionary)

    assert result.case_id is None
    assert result.data_model_name == "LM2007"
    assert result.survey_type == "LMS"    
    assert result.wave == "1"
    assert result.address_line_1 == "12 Blaise Street"
    assert result.address_line_2 == "Blaise Hill"
    assert result.address_line_3 == "Blaiseville"
    assert result.county == "Gwent"
    assert result.town == "Newport"           
    assert result.postcode == "FML134D"           
    assert result.telephone_number_1 == "07900990901"           
    assert result.telephone_number_2 == "07900990902"           
    assert result.appointment_telephone_number == "07900990903"           
    assert result.outcome_code == "301"                
    assert result.latitude == "10020202"                        
    assert result.longitude == "34949494"    
    assert result.priority == "1"    
    assert result.field_region == "gwent"    
    assert result.field_team == "B-Team"    
    assert result.wave_com_dte == "WGAFF"         
    

def test_populate_uac_data_populates_uac_fields_if_supplied():
    uac_model = UacModel(
        case_id="10020",
        uac_chunks=UacChunks(
            uac1="8176",
            uac2="4726",
            uac3="3992"
        )
    )

    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.populate_uac_data(uac_model)

    assert case_model.uac_chunks.uac1 == "8176"
    assert case_model.uac_chunks.uac2 == "4726"
    assert case_model.uac_chunks.uac3 == "3992"


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_none_of_the_mandatory_fields_are_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.case_id = test_input
    case_model.data_model_name = test_input
    case_model.survey_type = test_input
    case_model.wave = test_input
    case_model.address_line_1 = test_input
    case_model.address_line_2 = test_input
    case_model.address_line_3 = test_input
    case_model.county = test_input
    case_model.town = test_input
    case_model.postcode = test_input
    case_model.telephone_number_1 = test_input
    case_model.telephone_number_2  = test_input
    case_model.appointment_telephone_number = test_input
    case_model.outcome_code  = test_input
    case_model.latitude  = test_input
    case_model.longitude  = test_input
    case_model.priority  = test_input
    case_model.field_region  = test_input
    case_model.field_team  = test_input
    case_model.wave_com_dte  = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_case_id_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.case_id = test_input
   
    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_data_model_name_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.data_model_name = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_survey_type_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.survey_type = test_input
    
    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_wave_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.wave = test_input
  
    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_address_line_1_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.address_line_1 = test_input
   
    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_address_line_2_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.address_line_2 = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_address_line_3_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.address_line_3 = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_county_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.county = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_town_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.town = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_postcode_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.postcode = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_telephone_number_1_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.telephone_number_1 = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_telephone_number_2_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.telephone_number_2 = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_appointment_telephone_number_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.appointment_telephone_number = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_outcome_code_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.outcome_code = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_latitude_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.latitude = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_longitude_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.longitude = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_priority_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.priority = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_field_region_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.field_region = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_field_team_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.field_team = test_input

    assert case_model.is_fully_populated() is expected_outcome


@pytest.mark.parametrize("test_input,expected_outcome", [("", False), (None, False)])
def test_is_fully_populated_returns_false_if_wave_com_dte_field_is_not_populated(test_input, expected_outcome):
    case_model = questionnaire_case_model_helper.populated_case_model()
    case_model.wave_com_dte = test_input

    assert case_model.is_fully_populated() is expected_outcome
           