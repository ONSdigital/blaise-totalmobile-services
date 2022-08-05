from dataclasses import dataclass, fields
from dataclass_wizard import JSONWizard, json_field
from typing import Dict, Optional, Type, TypeVar
from models.uac_model import UacChunks, UacModel
import json

T = TypeVar('T')


@dataclass
class CaseModel(JSONWizard):
    case_id: str = json_field('qiD.Serial_Number', all=True, default='')
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
    uac_chunks: Optional[UacChunks] = json_field('uac_chunks', all=True, default=UacChunks(uac1='', uac2='', uac3=''))

    def populate_uac_data(self, uac_model: UacModel):
        self.uac_chunks = uac_model.uac_chunks

    def is_fully_populated(self) -> bool:
        for field in fields(CaseModel):
            if field.name == 'uac_chunks': continue
            if getattr(self, field.name) == "": return False
        return True

    def to_dict(self) -> Dict[str, str]:
        return json.loads(self.to_json())

    @classmethod
    def import_case_data(cls: Type[T], case_data_dictionary: Dict[str, str]) -> T:
        return CaseModel.from_json(json.dumps(case_data_dictionary))
