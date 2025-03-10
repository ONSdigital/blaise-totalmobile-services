from __future__ import annotations

import logging
from dataclasses import dataclass

from app.exceptions.custom_exceptions import InvalidTotalmobileFRSRequestException
from models.base_model import BaseModel
from models.common.totalmobile.totalmobile_reference_frs_model import (
    IncomingRequest,
    TotalmobileReferenceFRSModel,
)


@dataclass
class TotalMobileIncomingFRSRequestModel(BaseModel):
    questionnaire_name: str
    case_id: str
    prem1: str
    prem2: str
    town: str
    postcode: str
    interviewer_name: str
    interviewer_blaise_login: str

    @classmethod
    def import_request(
        cls, incoming_request: IncomingRequest
    ) -> TotalMobileIncomingFRSRequestModel:
        if not (
            cls.dictionary_keys_exist(
                incoming_request, "visit", "identity", "user", "name"
            )
            and cls.dictionary_keys_exist(
                incoming_request, "visit", "identity", "reference"
            )
        ):
            logging.error("The Totalmobile payload appears to be malformed")
            raise InvalidTotalmobileFRSRequestException

        reference_model = TotalmobileReferenceFRSModel.from_request(incoming_request)

        total_mobile_case = cls(
            questionnaire_name=reference_model.questionnaire_name,
            case_id=reference_model.case_id,
            prem1=reference_model.prem1,
            prem2=reference_model.prem2,
            town=reference_model.town,
            postcode=reference_model.postcode,
            interviewer_name=reference_model.interviewer_name,
            interviewer_blaise_login=reference_model.interviewer_blaise_login,
        )

        return total_mobile_case
