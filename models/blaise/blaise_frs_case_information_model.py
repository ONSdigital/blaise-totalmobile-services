from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Type, TypeVar

from models.blaise.blaise_case_information_base_model import (
    Address,
    AddressCoordinates,
    AddressDetails,
    BlaiseCaseInformationBaseModel,
)

V = TypeVar("V", bound="BlaiseFRSCaseInformationModel")


@dataclass
class BlaiseFRSCaseInformationModel(BlaiseCaseInformationBaseModel):
    @property
    def has_uac(self) -> bool:
        return False

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
            "qDataBag.UPRN",
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",
            "qDataBag.Priority",
            "qDataBag.FieldCase",
            "qDataBag.FieldRegion",
            "qDataBag.FieldTeam",
            "qDataBag.DivAddInd",
        ]
