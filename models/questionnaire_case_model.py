from dataclasses import dataclass
from dataclass_wizard import JSONWizard, json_field
from typing import Dict, Optional, Type, TypeVar
import json

T = TypeVar('T')

@dataclass
class UacChunks:
    uac1: str = json_field('uac1', all=True, default='')
    uac2: str = json_field('uac2', all=True, default='')
    uac3: str = json_field('uac3', all=True, default='')

@dataclass
class QuestionnaireCaseModel(JSONWizard):
    serial_number: str = json_field('qiD.Serial_Number', all=True, default='')
    data_model_name: str = json_field('dataModelName', all=True, default='')
    survey_type: str = json_field('qDataBag.TLA', all=True, default='')
    wave: str = json_field('qDataBag.Wave', all=True, default='') 
    address_line_1: str = json_field('qDataBag.Prem1', all=True, default='')  
    address_line_2: str = json_field('qDataBag.Prem2', all=True, default='') 
    address_line_3: str = json_field('qDataBag.Prem3', all=True, default='')  
    county: str = json_field('qDataBag.District', all=True, default='')  
    town: str = json_field('qDataBag.PostTown', all=True, default='')  
    postcode: str = json_field('qDataBag.PostCode', all=True, default='') 
    telephone_number_1: str = json_field('qDataBag.TelNo', all=True, default='')  
    telephone_number_2: str = json_field('qDataBag.TelNo2', all=True, default='') 
    appointment_telephone_number: str = json_field('telNoAppt', all=True, default='') 
    outcome_code: str = json_field('hOut', all=True, default='') 
    latitude: str = json_field('qDataBag.UPRN_Latitude', all=True, default='') 
    longitude: str = json_field('qDataBag.UPRN_Longitude', all=True, default='') 
    priority: str = json_field('qDataBag.Priority', all=True, default='') 
    field_region: str = json_field('qDataBag.FieldRegion', all=True, default='') 
    field_team: str = json_field('qDataBag.FieldTeam', all=True, default='') 
    wave_com_dte: str = json_field('qDataBag.WaveComDTE', all=True, default='') 
    uac_chunks : Optional[UacChunks] = json_field('uac_chunks', all=True, default=UacChunks(uac1='', uac2='', uac3='')) 

    def is_valid(cls) -> bool:
        if cls.serial_number == "": return False
        if cls.data_model_name == "": return False
        if cls.survey_type == "": return False
        if cls.wave == "": return False
        if cls.address_line_1 == "": return False
        if cls.address_line_2 == "": return False
        if cls.address_line_3 == "": return False                                        
        if cls.county == "": return False
        if cls.town == "": return False
        if cls.postcode == "": return False
        if cls.telephone_number_1 == "": return False
        if cls.telephone_number_2 == "": return False                                 
        if cls.appointment_telephone_number == "": return False       
        if cls.outcome_code == "": return False       
        if cls.latitude == "": return False             
        if cls.longitude == "": return False        
        if cls.priority == "": return False           
        if cls.field_region == "": return False    
        if cls.field_team == "": return False    
        if cls.wave_com_dte == "": return False                                                                  

        return True

    def to_dict(cls) -> Dict[str, str]:
        return json.loads(cls.to_json())

    @classmethod
    def import_case_data_dictionary(cls: Type[T], case_data_dictionary:Dict[str, str]) -> T:
        return QuestionnaireCaseModel.from_json(json.dumps(case_data_dictionary))
