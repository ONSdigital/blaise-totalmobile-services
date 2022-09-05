from dataclasses import dataclass, fields
from datetime import datetime
from typing import Dict, Optional, Type, TypeVar

from models.base_model import BaseModel
from models.blaise.uac_model import UacChunks, UacModel

T = TypeVar("T", bound="BlaiseCaseInformationModel")


@dataclass
class AddressCoordinates:
    latitude: Optional[str]
    longitude: Optional[str]


@dataclass
class Address:
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    address_line_3: Optional[str]
    county: Optional[str]
    town: Optional[str]
    postcode: Optional[str]
    coordinates: AddressCoordinates


@dataclass
class AddressDetails:
    address: Address


@dataclass
class ContactDetails:
    telephone_number_1: Optional[str]
    telephone_number_2: Optional[str]
    appointment_telephone_number: Optional[str]


@dataclass
class BlaiseCaseInformationModel(BaseModel):
    questionnaire_name: str
    case_id: Optional[str]
    data_model_name: Optional[str]
    # survey_type: str
    wave: Optional[str]
    address_details: AddressDetails
    contact_details: ContactDetails
    outcome_code: int
    priority: Optional[str]
    field_case: Optional[str]
    field_region: Optional[str]
    field_team: Optional[str]
    wave_com_dte: Optional[datetime]
    uac_chunks: Optional[UacChunks]
    has_call_history: bool

    def populate_uac_data(self, uac_model: Optional[UacModel]):
        if uac_model is None:
            self.uac_chunks = None
            return

        self.uac_chunks = uac_model.uac_chunks

    @classmethod
    def import_case(
        cls: Type[T], questionnaire_name: str, case_data_dictionary: Dict[str, str]
    ) -> T:
        wave_com_dte_str = case_data_dictionary.get("qDataBag.WaveComDTE", "")
        wave_com_dte = (
            datetime.strptime(wave_com_dte_str, "%d-%m-%Y")
            if wave_com_dte_str != ""
            else None
        )
        return cls(
            questionnaire_name=questionnaire_name,
            case_id=case_data_dictionary.get("qiD.Serial_Number"),
            data_model_name=case_data_dictionary.get("dataModelName"),
            # survey_type=case_data_dictionary.get("qDataBag.TLA"),
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
                    ),
                )
            ),
            contact_details=ContactDetails(
                telephone_number_1=case_data_dictionary.get("qDataBag.TelNo"),
                telephone_number_2=case_data_dictionary.get("qDataBag.TelNo2"),
                appointment_telephone_number=case_data_dictionary.get("telNoAppt"),
            ),
            outcome_code=cls.convert_string_to_integer(
                case_data_dictionary.get("hOut", "0")
            ),
            priority=case_data_dictionary.get("qDataBag.Priority"),
            field_case=case_data_dictionary.get("qDataBag.FieldCase"),
            field_region=case_data_dictionary.get("qDataBag.FieldRegion"),
            field_team=case_data_dictionary.get("qDataBag.FieldTeam"),
            wave_com_dte=wave_com_dte,
            uac_chunks=UacChunks(uac1="", uac2="", uac3=""),
            has_call_history=cls.string_to_bool(
                case_data_dictionary.get("catiMana.CatiCall.RegsCalls[1].DialResult")
            ),
        )

    @staticmethod
    def convert_string_to_integer(value: str) -> int:
        if value == "":
            return 0
        return int(value)

    @staticmethod
    def string_to_bool(value: Optional[str]) -> bool:
        if value == "" or value is None:
            return False
        return True
