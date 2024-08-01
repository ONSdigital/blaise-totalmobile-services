from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Type, TypeVar

from models.blaise.case_information_base_model import CaseInformationBaseModel

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
class BlaiseFRSCaseInformationModel(CaseInformationBaseModel):

    @classmethod
    def import_frs_case(
        cls: Type[V], questionnaire_name: str, case_data_dictionary: Dict[str, str]
    ) -> V:
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
            priority=case_data_dictionary.get("qDataBag.Priority"),
            field_case=case_data_dictionary.get("qDataBag.FieldCase"),
            field_region=case_data_dictionary.get("qDataBag.FieldRegion"),
            field_team=case_data_dictionary.get("qDataBag.FieldTeam"),
            wave_com_dte=wave_com_dte
        )

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
            "qDataBag.UPRN",
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",
            "qDataBag.Priority",
            "qDataBag.FieldCase",
            "qDataBag.FieldRegion",
            "qDataBag.FieldTeam",
        ]
