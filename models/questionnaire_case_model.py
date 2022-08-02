from dataclasses import dataclass, field, fields
from dataclasses_json import config, dataclass_json
from typing import Optional

@dataclass
class UacChunks:
    uac1: Optional[str] = field(default="", metadata=config(field_name="uac1"))
    uac2: Optional[str] = field(default="", metadata=config(field_name="uac2"))
    uac3: Optional[str] = field(default="", metadata=config(field_name="uac3"))

@dataclass_json
@dataclass
class QuestionnaireCaseModel:
    serial_number: Optional[str] = field(default="", metadata=config(field_name="qiD.Serial_Number"))
    data_model_name: Optional[str] = field(default="", metadata=config(field_name="dataModelName"))
    survey_type: Optional[str] = field(default="", metadata=config(field_name="qDataBag.TLA"))
    wave: Optional[str] = field(default="", metadata=config(field_name="qDataBag.Wave"))
    address_line_1: Optional[str] = field(default="", metadata=config(field_name="qDataBag.Prem1"))
    address_line_2: Optional[str] = field(default="", metadata=config(field_name="qDataBag.Prem2"))
    address_line_3: Optional[str] = field(default="", metadata=config(field_name="qDataBag.Prem3"))
    county: Optional[str] = field(default="", metadata=config(field_name="qDataBag.District"))
    town: Optional[str] = field(default="", metadata=config(field_name="qDataBag.PostTown"))
    postcode: Optional[str] = field(default="", metadata=config(field_name="qDataBag.PostCode"))
    telephone_number_1: Optional[str] = field(default="", metadata=config(field_name="qDataBag.TelNo"))
    telephone_number_2: Optional[str] = field(default="", metadata=config(field_name="qDataBag.TelNo2"))
    appointment_telephone_number: Optional[str] = field(default="", metadata=config(field_name="telNoAppt"))
    outcome_code: Optional[str] = field(default="", metadata=config(field_name="hOut"))
    latitude: Optional[str] = field(default="", metadata=config(field_name="qDataBag.UPRN_Latitude"))
    longitude: Optional[str] = field(default="", metadata=config(field_name="qDataBag.UPRN_Longitude"))
    priority: Optional[str] = field(default="", metadata=config(field_name="qDataBag.Priority"))
    field_region: Optional[str] = field(default="", metadata=config(field_name="qDataBag.FieldRegion"))
    field_team: Optional[str] = field(default="", metadata=config(field_name="qDataBag.FieldTeam"))
    wave_com_dte: Optional[str] = field(default="", metadata=config(field_name="qDataBag.WaveComDTE"))
    uac_chunks : Optional[UacChunks] = field(default=UacChunks("", "", ""), metadata=config(field_name="uac_chunks"))

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