from dataclasses import dataclass, fields
from datetime import datetime
from typing import Dict, Type, TypeVar, Optional
from models.base_model import BaseModel
from models.uac_model import UacChunks, UacModel

T = TypeVar('T')


@dataclass
class AddressCoordinates:
    latitude: str
    longitude: str


@dataclass
class Address:
    address_line_1: str
    address_line_2: str
    address_line_3: str
    county: str
    town: str
    postcode: str
    coordinates: AddressCoordinates


@dataclass
class AddressDetails:
    address: Address


@dataclass
class ContactDetails:
    telephone_number_1: str
    telephone_number_2: str
    appointment_telephone_number: str


@dataclass
class QuestionnaireCaseModel(BaseModel):
    questionnaire_name: str
    case_id: str
    data_model_name: str
    survey_type: str
    wave: str
    address_details: AddressDetails
    contact_details: ContactDetails
    outcome_code: int
    priority: str
    field_case: str
    field_region: str
    field_team: str
    wave_com_dte: Optional[datetime]
    uac_chunks: UacChunks

    def populate_uac_data(self, uac_model: UacModel):
        if uac_model is None:
            self.uac_chunks = None
            return

        self.uac_chunks = uac_model.uac_chunks

    @classmethod
    def import_case(cls: Type[T], questionnaire_name: str, case_data_dictionary: Dict[str, str]) -> T:
        wave_com_dte_str = case_data_dictionary.get("qDataBag.WaveComDTE")
        wave_com_dte = datetime.strptime(wave_com_dte_str, "%d-%m-%Y") if wave_com_dte_str != '' else None
        return QuestionnaireCaseModel(
            questionnaire_name=questionnaire_name,
            case_id=case_data_dictionary.get("qiD.Serial_Number"),
            data_model_name=case_data_dictionary.get("dataModelName"),
            survey_type=case_data_dictionary.get("qDataBag.TLA"),
            wave=case_data_dictionary.get("qDataBag.Wave"),
            address_details=AddressDetails(
                address=Address(
                    address_line_1=case_data_dictionary.get("qDataBag.Prem1"),
                    address_line_2=case_data_dictionary.get("qDataBag.Prem2"),
                    address_line_3=case_data_dictionary.get("qDataBag.Prem3"),
                    county=case_data_dictionary.get("qDataBag.District"),
                    town=case_data_dictionary.get("qDataBag.PostTown"),
                    postcode=case_data_dictionary.get("qDataBag.PostCode"),
                    coordinates=AddressCoordinates(
                        latitude=case_data_dictionary.get("qDataBag.UPRN_Latitude"),
                        longitude=case_data_dictionary.get("qDataBag.UPRN_Longitude"),
                    )
                )
            ),
            contact_details=ContactDetails(
                telephone_number_1=case_data_dictionary.get("qDataBag.TelNo"),
                telephone_number_2=case_data_dictionary.get("qDataBag.TelNo2"),
                appointment_telephone_number=case_data_dictionary.get("telNoAppt"),
            ),
            outcome_code=cls.convert_string_to_integer(case_data_dictionary.get("hOut", 0)),
            priority=case_data_dictionary.get("qDataBag.Priority"),
            field_case=case_data_dictionary.get("qDataBag.FieldCase"),
            field_region=case_data_dictionary.get("qDataBag.FieldRegion"),
            field_team=case_data_dictionary.get("qDataBag.FieldTeam"),
            wave_com_dte=wave_com_dte,
            uac_chunks=UacChunks(uac1="", uac2="", uac3="")
        )

    @staticmethod
    def convert_string_to_integer(value: str) -> int:
        if value == "":
            return 0
        return int(value)
