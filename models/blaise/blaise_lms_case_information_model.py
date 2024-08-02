from dataclasses import dataclass
from typing import List, Optional, Type, TypeVar

from models.blaise.blaise_case_information_base_model import BlaiseCaseInformationBaseModel

@dataclass
class ContactDetails:
    telephone_number_1: Optional[str]
    telephone_number_2: Optional[str]
    appointment_telephone_number: Optional[str]


@dataclass()
class BlaiseLMSCaseInformationModel(BlaiseCaseInformationBaseModel):
    contact_details: ContactDetails
    outcome_code: int
    has_call_history: bool
    rotational_knock_to_nudge_indicator: Optional[str]
    rotational_outcome_code: int

    @property
    def has_uac(self) -> bool:
        return True

    @staticmethod
    def required_fields() -> List:
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
