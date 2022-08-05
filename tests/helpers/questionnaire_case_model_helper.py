from models.case_model import QuestionnaireCaseModel

def get_populated_case_model():
    return QuestionnaireCaseModel(
        case_id = "90000000",
        data_model_name = "LM2007",
        survey_type = "LMS",
        wave = "1",
        address_line_1 = "12 Blaise Street",
        address_line_2 = "Blaise Hill",
        address_line_3 = "Blaiseville",
        county = "Gwent",
        town = "Newport",          
        postcode = "FML134D",          
        telephone_number_1 = "07900990901",           
        telephone_number_2 = "07900990902",           
        appointment_telephone_number = "07900990903",           
        outcome_code = "301",                
        latitude = "10020202",                        
        longitude = "34949494",    
        priority = "1",    
        field_region = "gwent",    
        field_team = "B-Team",    
        wave_com_dte = "WGAFF")