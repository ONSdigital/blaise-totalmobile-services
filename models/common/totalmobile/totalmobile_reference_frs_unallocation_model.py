from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Type, TypedDict, TypeVar

from app.exceptions.custom_exceptions import BadReferenceError, MissingReferenceError
from models.base_model import BaseModel

T = TypeVar("T", bound="TotalmobileReferenceUnallocationFRSModel")


class IncomingRequestResult(TypedDict):
    identity: Dict[str, Any]


class IncomingRequest(TypedDict):
    visit: IncomingRequestResult


class TotalmobileReferenceUnallocationFRSModel(BaseModel):
    questionnaire_name: str
    case_id: str
    interviewer_name: str

    def __init__(self, questionnaire_name: str, case_id: str, interviewer_name: str):
        self.questionnaire_name = questionnaire_name
        self.case_id = case_id
        self.interviewer_name = interviewer_name

    @classmethod
    def from_request(cls: Type[T], request: IncomingRequest) -> T:
        questionnaire_case_reference = (
            cls.get_questionnaire_case_reference_from_incoming_request(request)
        )
        interviewer_name_reference = (
            cls.get_interviewer_reference_from_incoming_request(request)
        )
        return cls.get_model_from_reference(
            questionnaire_case_reference, interviewer_name_reference
        )

    @classmethod
    def from_questionnaire_and_case_and_interviewer(
        cls: Type[T],
        questionnaire_name: Optional[str],
        case_id: Optional[str],
        interviewer_name: Optional[str],
    ) -> T:
        if (
            questionnaire_name is None
            or questionnaire_name == ""
            or case_id is None
            or case_id == ""
            or interviewer_name is None
            or interviewer_name == ""
        ):
            raise MissingReferenceError()

        return cls(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
            interviewer_name=interviewer_name,
        )

    def create_frs_reference(self) -> str:
        return f"{self.questionnaire_name}.{self.case_id}"

    @staticmethod
    def get_fields_from_reference(reference: str) -> List[str]:
        reference_fields = reference.split(".", 2)

        if len(reference_fields) != 2:
            logging.error(
                f"Unique reference appeared to be malformed in the Totalmobile payload (reference='{reference}')"
            )
            raise BadReferenceError()

        if reference_fields[0] == "" or reference_fields[1] == "":
            logging.error(
                f"Unique reference appeared to be malformed in the Totalmobile payload (reference='{reference}')"
            )
            raise BadReferenceError()

        return reference_fields

    @staticmethod
    def get_questionnaire_case_reference_from_incoming_request(
        incoming_request: IncomingRequest,
    ):
        reference = TotalmobileReferenceUnallocationFRSModel.get_dictionary_keys_value_if_they_exist(
            incoming_request, "identity", "reference"
        )

        if reference is None:
            logging.error("Unique reference is missing from the Totalmobile payload")
            raise MissingReferenceError()

        return reference

    @staticmethod
    def get_interviewer_reference_from_incoming_request(
        incoming_request: IncomingRequest,
    ):
        user_attribute = TotalmobileReferenceUnallocationFRSModel.get_dictionary_keys_value_if_they_exist(
            incoming_request, "identity", "user", "name"
        )

        if user_attribute is None:
            logging.error(
                "Interviewer Name reference is missing from the Totalmobile payload"
            )
            raise MissingReferenceError()

        return user_attribute

    @staticmethod
    def get_model_from_reference(
        questionnaire_case_reference: str, interviewer_name_reference: str
    ):
        questionnaire_case_request_fields = (
            TotalmobileReferenceUnallocationFRSModel.get_fields_from_reference(
                questionnaire_case_reference
            )
        )
        questionnaire_name = questionnaire_case_request_fields[0]
        case_id = questionnaire_case_request_fields[1]
        return TotalmobileReferenceUnallocationFRSModel(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
            interviewer_name=interviewer_name_reference,
        )
