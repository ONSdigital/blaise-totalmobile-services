from models.questionnaire_case_model import QuestionnaireCaseModel

def test_from_json_returns_a_populated_model():
    mock_blaise_data = ('{ \
            "qiD.Serial_Number": "90000000", \
            "dataModelName" : "LM2007", \
            "qDataBag.TLA" : "LMS", \
            "qDataBag.Wave" : "1", \
            "qDataBag.Prem1" : "12 Blaise Street", \
            "qDataBag.Prem2" : "Blaise Hill", \
            "qDataBag.Prem3" : "Blaiseville", \
            "qDataBag.District" : "Gwent", \
            "qDataBag.PostTown" : "Newport", \
            "qDataBag.PostCode" : "FML134D", \
            "qDataBag.TelNo" : "07900990901", \
            "qDataBag.TelNo2" : "07900990902", \
            "telNoAppt" : "07900990903", \
            "hOut" : "301", \
            "qDataBag.UPRN_Latitude" : "10020202", \
            "qDataBag.UPRN_Longitude" : "34949494", \
            "qDataBag.Priority" : "1", \
            "qDataBag.FieldRegion" : "gwent", \
            "qDataBag.FieldTeam": "B-Team", \
            "qDataBag.WaveComDTE": "WGAFF" \
         }')

    result = QuestionnaireCaseModel.from_json(mock_blaise_data)
    assert result.serial_number == "90000000"
    assert result.data_model_name == "LM2007"
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


def test_from_json_returns_a_valid_object_when_a_blaise_field_is_incorrectly_typed():
    mock_blaise_data = ('{ \
            "qdatabag.Serial_Number": "90000000", \
            "dataModelName" : "LM2007", \
            "qDataBag.TLA" : "LMS", \
            "qDataBag.Wave" : "1", \
            "qDataBag.Prem1" : "12 Blaise Street", \
            "qDataBag.Prem2" : "Blaise Hill", \
            "qDataBag.Prem3" : "Blaiseville", \
            "qDataBag.District" : "Gwent", \
            "qDataBag.PostTown" : "Newport", \
            "qDataBag.PostCode" : "FML134D", \
            "qDataBag.TelNo" : "07900990901", \
            "qDataBag.TelNo2" : "07900990902", \
            "telNoAppt" : "07900990903", \
            "hOut" : "301", \
            "qDataBag.UPRN_Latitude" : "10020202", \
            "qDataBag.UPRN_Longitude" : "34949494", \
            "qDataBag.Priority" : "1", \
            "qDataBag.FieldRegion" : "gwent", \
            "qDataBag.FieldTeam": "B-Team", \
            "qDataBag.WaveComDTE": "WGAFF" \
         }')    

    result = QuestionnaireCaseModel.from_json(mock_blaise_data)
    assert result.serial_number == None


def test_from_json_returns_a_valid_object_when_an_optional_blaise_field_is_missing():
    mock_blaise_data = ('{ \
            "dataModelName" : "LM2007", \
            "qDataBag.TLA" : "LMS", \
            "qDataBag.Wave" : "1", \
            "qDataBag.Prem1" : "12 Blaise Street", \
            "qDataBag.Prem2" : "Blaise Hill", \
            "qDataBag.Prem3" : "Blaiseville", \
            "qDataBag.District" : "Gwent", \
            "qDataBag.PostTown" : "Newport", \
            "qDataBag.PostCode" : "FML134D", \
            "qDataBag.TelNo" : "07900990901", \
            "qDataBag.TelNo2" : "07900990902", \
            "telNoAppt" : "07900990903", \
            "hOut" : "301", \
            "qDataBag.UPRN_Latitude" : "10020202", \
            "qDataBag.UPRN_Longitude" : "34949494", \
            "qDataBag.Priority" : "1", \
            "qDataBag.FieldRegion" : "gwent", \
            "qDataBag.FieldTeam": "B-Team", \
            "qDataBag.WaveComDTE": "WGAFF" \
         }')

    result = QuestionnaireCaseModel.from_json(mock_blaise_data)
    assert result.serial_number == None    
    

def test_is_valid_returns_true_if_all_mandatory_fields_are_populated():
    mock_blaise_data = ('{ \
            "qiD.Serial_Number": "90000000", \
            "dataModelName" : "LM2007", \
            "qDataBag.TLA" : "LMS", \
            "qDataBag.Wave" : "1", \
            "qDataBag.Prem1" : "12 Blaise Street", \
            "qDataBag.Prem2" : "Blaise Hill", \
            "qDataBag.Prem3" : "Blaiseville", \
            "qDataBag.District" : "Gwent", \
            "qDataBag.PostTown" : "Newport", \
            "qDataBag.PostCode" : "FML134D", \
            "qDataBag.TelNo" : "07900990901", \
            "qDataBag.TelNo2" : "07900990902", \
            "telNoAppt" : "07900990903", \
            "hOut" : "301", \
            "qDataBag.UPRN_Latitude" : "10020202", \
            "qDataBag.UPRN_Longitude" : "34949494", \
            "qDataBag.Priority" : "1", \
            "qDataBag.FieldRegion" : "gwent", \
            "qDataBag.FieldTeam": "B-Team", \
            "qDataBag.WaveComDTE": "WGAFF" \
         }')
    case_model = QuestionnaireCaseModel.from_json(mock_blaise_data)

    print(case_model.serial_number)
    result = case_model.is_valid()
    assert result is True

    
def test_is_valid_returns_false_if_any_mandatory_field_is_not_populated():
    mock_blaise_data = ('{ \
            "dataModelName" : "LM2007", \
            "qDataBag.TLA" : "LMS", \
            "qDataBag.Wave" : "1", \
            "qDataBag.Prem1" : "12 Blaise Street", \
            "qDataBag.Prem2" : "Blaise Hill", \
            "qDataBag.Prem3" : "Blaiseville", \
            "qDataBag.District" : "Gwent", \
            "qDataBag.PostTown" : "Newport", \
            "qDataBag.PostCode" : "FML134D", \
            "qDataBag.TelNo" : "07900990901", \
            "qDataBag.TelNo2" : "07900990902", \
            "telNoAppt" : "07900990903", \
            "hOut" : "301", \
            "qDataBag.UPRN_Latitude" : "10020202", \
            "qDataBag.UPRN_Longitude" : "34949494", \
            "qDataBag.Priority" : "1", \
            "qDataBag.FieldRegion" : "gwent", \
            "qDataBag.FieldTeam": "B-Team", \
            "qDataBag.WaveComDTE": "WGAFF" \
         }')
    case_model = QuestionnaireCaseModel.from_json(mock_blaise_data)

    result = case_model.is_valid()
    assert result is False