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

    assert result.serial_number == "90000000"
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

    assert result.serial_number == ""
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

    assert result.serial_number == ""    
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
        serial_number="10020",
        uac_chunks=UacChunks(
            uac1="8176",
            uac2="4726",
            uac3="3992"
        )
    )

    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.populate_uac_data(uac_model)

    assert case_model.uac_chunks.uac1 == "8176"
    assert case_model.uac_chunks.uac2 == "4726"
    assert case_model.uac_chunks.uac3 == "3992"


def test_is_fully_populated_returns_false_if_none_of_the_mandatory_fields_are_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.serial_number = ""   
    case_model.data_model_name = ""
    case_model.survey_type = ""
    case_model.wave = ""
    case_model.address_line_1 = ""
    case_model.address_line_2 = ""
    case_model.address_line_3 = ""
    case_model.county = ""
    case_model.town = ""      
    case_model.postcode = ""       
    case_model.telephone_number_1 = ""       
    case_model.telephone_number_2  = ""             
    case_model.appointment_telephone_number = ""        
    case_model.outcome_code  = ""             
    case_model.latitude  = ""                          
    case_model.longitude  = ""     
    case_model.priority  = ""     
    case_model.field_region  = ""     
    case_model.field_team  = ""      
    case_model.wave_com_dte  = ""           

    assert case_model.is_fully_populated() is False    

    
def test_is_fully_populated_returns_false_if_serial_number_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.serial_number = "" 
   
    assert case_model.is_fully_populated() is False


def test_is_fully_populated_returns_false_if_data_model_name_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.data_model_name = "" 

    assert case_model.is_fully_populated() is False    


def test_is_fully_populated_returns_false_if_survey_type_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.survey_type = ""   
    
    assert case_model.is_fully_populated() is False      


def test_is_fully_populated_returns_false_if_wave_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.wave = ""      
  
    assert case_model.is_fully_populated() is False     


def test_is_fully_populated_returns_false_if_address_line_1_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.address_line_1 = ""          
   
    assert case_model.is_fully_populated() is False         


def test_is_fully_populated_returns_false_if_address_line_2_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.address_line_2 = "" 

    assert case_model.is_fully_populated() is False   


def test_is_fully_populated_returns_false_if_address_line_3_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.address_line_3 = "" 

    assert case_model.is_fully_populated() is False       


def test_is_fully_populated_returns_false_if_county_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.county = "" 

    assert case_model.is_fully_populated() is False         


def test_is_fully_populated_returns_false_if_town_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.town = "" 

    assert case_model.is_fully_populated() is False     


def test_is_fully_populated_returns_false_if_postcode_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.postcode = "" 

    assert case_model.is_fully_populated() is False       


def test_is_fully_populated_returns_false_if_telephone_number_1_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.telephone_number_1 = "" 

    assert case_model.is_fully_populated() is False   


def test_is_fully_populated_returns_false_if_telephone_number_2_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.telephone_number_2 = "" 

    assert case_model.is_fully_populated() is False   


def test_is_fully_populated_returns_false_if_appointment_telephone_number_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.appointment_telephone_number = "" 

    assert case_model.is_fully_populated() is False            


def test_is_fully_populated_returns_false_if_outcome_code_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.outcome_code = "" 

    assert case_model.is_fully_populated() is False         


def test_is_fully_populated_returns_false_if_latitude_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.latitude = "" 

    assert case_model.is_fully_populated() is False     


def test_is_fully_populated_returns_false_if_longitude_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.longitude = "" 

    assert case_model.is_fully_populated() is False         


def test_is_fully_populated_returns_false_if_priority_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.priority = "" 

    assert case_model.is_fully_populated() is False         


def test_is_fully_populated_returns_false_if_field_region_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.field_region = "" 

    assert case_model.is_fully_populated() is False       


def test_is_fully_populated_returns_false_if_field_team_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.field_team = "" 

    assert case_model.is_fully_populated() is False         


def test_is_fully_populated_returns_false_if_wave_com_dte_field_is_not_populated():
    case_model = questionnaire_case_model_helper.get_populated_case_model()
    case_model.wave_com_dte = "" 

    assert case_model.is_fully_populated() is False          
           