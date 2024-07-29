from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Type, TypeVar

from models.base_model import BaseModel

T = TypeVar("T", bound="BlaiseCaseInformationModel")
V = TypeVar("V", bound="BlaiseFRSCaseInformationModel")


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
    reference: Optional[str]
    address: Address


@dataclass
class ContactDetails:
    telephone_number_1: Optional[str]
    telephone_number_2: Optional[str]
    appointment_telephone_number: Optional[str]


@dataclass
class BlaiseCaseInformationModel(BaseModel):
    questionnaire_name: str
    tla: str
    case_id: Optional[str]
    data_model_name: Optional[str]
    wave: Optional[int]
    wave_com_dte: Optional[datetime]
    address_details: AddressDetails
    contact_details: ContactDetails
    outcome_code: int
    priority: Optional[str]
    field_case: Optional[str]
    field_region: Optional[str]
    field_team: Optional[str]
    has_call_history: bool
    rotational_knock_to_nudge_indicator: Optional[str]
    rotational_outcome_code: int

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
        wave = case_data_dictionary.get("qDataBag.Wave")
        tla = questionnaire_name[0:3]

        return cls(
            questionnaire_name=questionnaire_name,
            tla=tla,
            case_id=case_data_dictionary.get("qiD.Serial_Number"),
            data_model_name=case_data_dictionary.get("dataModelName"),
            wave=int(wave) if wave else None,
            address_details=AddressDetails(
                reference=case_data_dictionary.get("qDataBag.UPRN", ""),
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
                ),
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
            has_call_history=cls.string_to_bool(
                case_data_dictionary.get("catiMana.CatiCall.RegsCalls[1].DialResult")
            ),
            rotational_knock_to_nudge_indicator=cls.convert_indicator_to_y_n_or_empty(
                case_data_dictionary.get("qRotate.RDMktnIND")
            ),
            rotational_outcome_code=cls.convert_string_to_integer(
                case_data_dictionary.get("qRotate.RHOut", "0")
            ),
        )

    @staticmethod
    def convert_indicator_to_y_n_or_empty(value: Optional[str]):
        if not value or value == "":
            return ""

        return "Y" if value == "1" else "N"

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

    @staticmethod
    def required_fields_from_blaise() -> List:
        return [
            "qiD.Serial_Number",
            "dataModelName",
            "qDataBag.TLA",
            "qDataBag.Wave",
            "qDataBag.Prem1",
            "qDataBag.Prem2",
            "qDataBag.Prem3",
            "qDataBag.District",
            "qDataBag.PostTown",
            "qDataBag.PostCode",
            "qDataBag.TelNo",
            "qDataBag.TelNo2",
            "telNoAppt",
            "hOut",
            "qDataBag.UPRN",
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",
            "qDataBag.Priority",
            "qDataBag.FieldCase",
            "qDataBag.FieldRegion",
            "qDataBag.FieldTeam",
            "qDataBag.WaveComDTE",
            "catiMana.CatiCall.RegsCalls[1].DialResult",
            "qRotate.RDMktnIND",
            "qRotate.RHOut",
        ]

@dataclass
class BlaiseFRSCaseInformationModel(BaseModel):
    questionnaire_name: str
    tla: str
    case_id: Optional[str]
    data_model_name: Optional[str]
    wave: Optional[int]   # TODO (required field for current route - optional value)
    wave_com_dte: Optional[datetime]  # TODO (required field for current route - optional value)
    address_details: AddressDetails
    # contact_details: ContactDetails   # TODO
    # outcome_code: int     # TODO
    priority: Optional[str]
    field_case: Optional[str]
    field_region: Optional[str]
    field_team: Optional[str]
    # has_call_history: bool        # TODO
    # rotational_knock_to_nudge_indicator: Optional[str]        # TODO
    # rotational_outcome_code: int      # TODO

    @classmethod
    def import_frs_case(
        cls: Type[V], questionnaire_name: str, case_data_dictionary: Dict[str, str]
    ) -> V:
        # wave_com_dte_str = case_data_dictionary.get("qDataBag.WaveComDTE", "")
        # wave_com_dte = (
        #     datetime.strptime(wave_com_dte_str, "%d-%m-%Y")
        #     if wave_com_dte_str != ""
        #     else None
        # )
        # wave = case_data_dictionary.get("qDataBag.Wave")
        tla = questionnaire_name[0:3]

        return cls(
            questionnaire_name=questionnaire_name,
            tla=tla,
            case_id=case_data_dictionary.get("qiD.Serial_Number"),
            data_model_name=case_data_dictionary.get("dataModelName"),
            # wave=int(wave) if wave else None,
            address_details=AddressDetails(
                reference=case_data_dictionary.get("qDataBag.UPRN", ""),
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
                ),
            ),
            # contact_details=ContactDetails(
            #     telephone_number_1=case_data_dictionary.get("qDataBag.TelNo"),
            #     telephone_number_2=case_data_dictionary.get("qDataBag.TelNo2"),
            #     appointment_telephone_number=case_data_dictionary.get("telNoAppt"),
            # ),
            # outcome_code=cls.convert_string_to_integer(
            #     case_data_dictionary.get("hOut", "0")
            # ),
            priority=case_data_dictionary.get("qDataBag.Priority"),
            field_case=case_data_dictionary.get("qDataBag.FieldCase"),
            field_region=case_data_dictionary.get("qDataBag.FieldRegion"),
            field_team=case_data_dictionary.get("qDataBag.FieldTeam"),
            # wave_com_dte=wave_com_dte,
            # has_call_history=cls.string_to_bool(
            #     case_data_dictionary.get("catiMana.CatiCall.RegsCalls[1].DialResult")
            # ),
            # rotational_knock_to_nudge_indicator=cls.convert_indicator_to_y_n_or_empty(
            #     case_data_dictionary.get("qRotate.RDMktnIND")
            # ),
            # rotational_outcome_code=cls.convert_string_to_integer(
            #     case_data_dictionary.get("qRotate.RHOut", "0")
            # ),
        )

    @staticmethod
    def convert_indicator_to_y_n_or_empty(value: Optional[str]):
        if not value or value == "":
            return ""

        return "Y" if value == "1" else "N"

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

    @staticmethod
    def required_fields_from_blaise() -> List:
        return [
            "qiD.Serial_Number",
            "dataModelName",
            "qDataBag.TLA",
            # "qDataBag.Wave",      # TODO
            "qDataBag.Prem1",
            "qDataBag.Prem2",
            "qDataBag.Prem3",
            "qDataBag.District",
            "qDataBag.PostTown",
            "qDataBag.PostCode",
            # "qDataBag.TelNo",     # TODO
            # "qDataBag.TelNo2",    # TODO
            # "telNoAppt",          # TODO
            # "hOut",               # TODO
            "qDataBag.UPRN",
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",
            "qDataBag.Priority",
            "qDataBag.FieldCase",
            "qDataBag.FieldRegion",
            "qDataBag.FieldTeam",
            # "qDataBag.WaveComDTE",    # TODO
            # "catiMana.CatiCall.RegsCalls[1].DialResult",  # TODO
            # "qRotate.RDMktnIND",      # TODO
            # "qRotate.RHOut",          # TODO
        ]
