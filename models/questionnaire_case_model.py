from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class QuestionnaireCaseModel:
    serial_number: Optional[str] = field(default=None, metadata=config(field_name="qiD.Serial_Number"))
    data_model_name: str = field(default=None, metadata=config(field_name="dataModelName"))
    survey_type: str = field(default=None, metadata=config(field_name="qDataBag.TLA"))
    wave: str = field(default=None, metadata=config(field_name="qDataBag.Wave"))
    address_line_1: str = field(default=None, metadata=config(field_name="qDataBag.Prem1"))
    address_line_2: str = field(default=None, metadata=config(field_name="qDataBag.Prem2"))
    address_line_3: str = field(default=None, metadata=config(field_name="qDataBag.Prem3"))
    county: str = field(default=None, metadata=config(field_name="qDataBag.District"))
    town: str = field(default=None, metadata=config(field_name="qDataBag.PostTown"))
    postcode: str = field(default=None, metadata=config(field_name="qDataBag.PostCode"))
    telephone_number_1: str = field(default=None, metadata=config(field_name="qDataBag.TelNo"))
    telephone_number_2: str = field(default=None, metadata=config(field_name="qDataBag.TelNo2"))
    appointment_telephone_number: str = field(default=None, metadata=config(field_name="telNoAppt"))
    outcome_code: str = field(default=None, metadata=config(field_name="hOut"))
    latitude: str = field(default=None, metadata=config(field_name="qDataBag.UPRN_Latitude"))
    longitude: str = field(default=None, metadata=config(field_name="qDataBag.UPRN_Longitude"))
    priority: str = field(default=None, metadata=config(field_name="qDataBag.Priority"))
    field_region: str = field(default=None, metadata=config(field_name="qDataBag.FieldRegion"))
    field_team: str = field(default=None, metadata=config(field_name="qDataBag.FieldTeam"))
    wave_com_dte: str = field(default=None, metadata=config(field_name="qDataBag.WaveComDTE"))

    def is_valid(cls) -> bool:
        if cls.serial_number is None:
            return False
        return True