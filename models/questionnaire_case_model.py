import json

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class CaseModel:
    serial_number: str | None = field(metadata=config(field_name="qiD.Serial_Number"))
    # data_model_name: str = field(metadata=config(field_name="qiD.Serial_Number"))
    # survey_type: str
    # wave: str
    # address_line_1: str
    # address_line_2: str
    # address_line_3: str
    # county: str
    # town: str
    # postcode: str
    # telephone_number_1: str
    # telephone_number_2: str
    # appointment_telephone_number: str
    # outcome_code: str
    # latitude: str
    # longitude: str
    # priority: str
    # field_region: str
    # field_team: str
    # wave_com_dte: str

    # def __init__(self):
    #     self.serial_number == ""

    @classmethod
    def from_json(cls, blaise_data) -> "CaseModel":
        return self.from_json(blaise_data)

