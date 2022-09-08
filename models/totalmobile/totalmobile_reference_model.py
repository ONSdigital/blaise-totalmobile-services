from __future__ import annotations

import logging
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    TypedDict,
    TypeVar,
)

from app.exceptions.custom_exceptions import BadReferenceError, MissingReferenceError
from models.base_model import BaseModel

T = TypeVar("T", bound="TotalmobileReferenceModel")


class IncomingRequestResult(TypedDict):
    responses: Dict[str, Any]


class IncomingRequest(TypedDict):
    result: IncomingRequestResult


class TotalmobileReferenceModel(BaseModel):
    questionnaire_name: str
    case_id: str

    def __init__(self, questionnaire_name: str, case_id: str):
        self.questionnaire_name = questionnaire_name
        self.case_id = case_id

    @classmethod
    def from_reference(cls: Type[T], reference: str) -> T:
        return cls.get_model_from_reference(reference)

    @classmethod
    def from_request(cls: Type[T], request: IncomingRequest) -> T:
        reference = cls.get_reference_from_incoming_request(request)
        return cls.get_model_from_reference(reference)

    @classmethod
    def from_questionnaire_and_case(
        cls: Type[T], questionnaire_name: Optional[str], case_id: Optional[str]
    ) -> T:
        if (
            questionnaire_name is None
            or questionnaire_name == ""
            or case_id is None
            or case_id == ""
        ):
            raise MissingReferenceError()

        return cls(questionnaire_name=questionnaire_name, case_id=case_id)

    def create_reference(self) -> str:
        return f"{self.questionnaire_name.replace('_', '-')}.{self.case_id}"

    @staticmethod
    def get_fields_from_reference(reference: str) -> List[str]:
        reference_fields = reference.split(".", 2)

        if len(reference_fields) != 2:
            logging.error(
                "Unique reference appeared to be malformed in the totalmobile payload"
            )
            raise BadReferenceError()

        if reference_fields[0] == "" or reference_fields[1] == "":
            logging.error(
                "Unique reference appeared to be malformed in the totalmobile payload"
            )
            raise BadReferenceError()

        return reference_fields

    @staticmethod
    def get_reference_from_incoming_request(incoming_request: IncomingRequest):
        reference = TotalmobileReferenceModel.get_dictionary_keys_value_if_they_exist(
            incoming_request, "result", "association", "reference"
        )

        if reference is None:
            logging.error("Unique reference is missing from totalmobile payload")
            raise MissingReferenceError()

        return reference

    @staticmethod
    def get_model_from_reference(reference: str):
        request_fields = TotalmobileReferenceModel.get_fields_from_reference(reference)
        questionnaire_name = request_fields[0].replace("-", "_")
        case_id = request_fields[1]
        return TotalmobileReferenceModel(questionnaire_name=questionnaire_name, case_id=case_id)
