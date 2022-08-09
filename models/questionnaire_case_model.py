from dataclasses import dataclass, fields
from typing import Dict, Type, TypeVar
from models.uac_model import UacChunks, UacModel
from datetime import date

T = TypeVar('T')


@dataclass
class QuestionnaireCaseModel:
    case_id: str
    data_model_name: str
    survey_type: str
    wave: str
    address_line_1: str
    address_line_2: str
    address_line_3: str
    county: str
    town: str
    postcode: str
    telephone_number_1: str
    telephone_number_2: str
    appointment_telephone_number: str
    outcome_code: str
    latitude: str
    longitude: str
    priority: str
    field_region: str
    field_team: str
    wave_com_dte: date
    uac_chunks: UacChunks

    def populate_uac_data(self, uac_model: UacModel):
        self.uac_chunks = uac_model.uac_chunks

    def is_fully_populated(self) -> bool:
        for field in fields(QuestionnaireCaseModel):
            if getattr(self, field.name) is None or getattr(self, field.name) == "":
                return False
        return True

    def to_dict(self) -> Dict[str, str]:
        return []

    @classmethod
    def import_case(cls: Type[T], case_data_dictionary: Dict[str, str]) -> T:
        return QuestionnaireCaseModel(
            case_id=case_data_dictionary.get("qiD.Serial_Number"),
            data_model_name=case_data_dictionary.get("dataModelName"),
            survey_type=case_data_dictionary.get("qDataBag.TLA"),
            wave=case_data_dictionary.get("qDataBag.Wave"),
            address_line_1=case_data_dictionary.get("qDataBag.Prem1"),
            address_line_2=case_data_dictionary.get("qDataBag.Prem2"),
            address_line_3=case_data_dictionary.get("qDataBag.Prem3"),
            county=case_data_dictionary.get("qDataBag.District"),
            town=case_data_dictionary.get("qDataBag.PostTown"),
            postcode=case_data_dictionary.get("qDataBag.PostCode"),
            telephone_number_1=case_data_dictionary.get("qDataBag.TelNo"),
            telephone_number_2=case_data_dictionary.get("qDataBag.TelNo2"),
            appointment_telephone_number=case_data_dictionary.get("telNoAppt"),
            outcome_code=case_data_dictionary.get("hOut"),
            latitude=case_data_dictionary.get("qDataBag.UPRN_Latitude"),
            longitude=case_data_dictionary.get("qDataBag.UPRN_Longitude"),
            priority=case_data_dictionary.get("qDataBag.Priority"),
            field_region=case_data_dictionary.get("qDataBag.FieldRegion"),
            field_team=case_data_dictionary.get("qDataBag.FieldTeam"),
            wave_com_dte=case_data_dictionary.get("qDataBag.WaveComDTE"),
            uac_chunks=UacChunks(uac1='', uac2='', uac3='')
        )
