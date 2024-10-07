from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Type, TypeVar

from app.exceptions.custom_exceptions import InvalidTotalmobileFRSRequestException
from models.base_model import BaseModel
from models.common.totalmobile.totalmobile_reference_frs_unallocation_model import (
    IncomingRequest
)
from models.common.totalmobile.totalmobile_reference_frs_unallocation_model import TotalmobileReferenceUnallocationFRSModel

T = TypeVar("T", bound="TotalMobileIncomingFRSUnallocationRequestModel")


@dataclass
class TotalMobileIncomingFRSUnallocationRequestModel(BaseModel):
    questionnaire_name: str
    case_id: str
    interviewer_name: str

    @classmethod
    def import_request(cls: Type[T], incoming_request: IncomingRequest) -> T:
        if not (
            cls.dictionary_keys_exist(incoming_request, "identity", "reference") 
            and cls.dictionary_keys_exist(incoming_request, "identity", "user", "name")
            ):
            logging.error("The Totalmobile payload appears to be malformed")
            raise InvalidTotalmobileFRSRequestException
        
        reference_model = TotalmobileReferenceUnallocationFRSModel.from_request(incoming_request)

        total_mobile_case = cls(
            questionnaire_name=reference_model.questionnaire_name,
            case_id=reference_model.case_id,
            interviewer_name = reference_model.interviewer_name
        )

        return total_mobile_case
