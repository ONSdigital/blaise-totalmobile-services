from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Type, TypedDict, TypeVar

from app.exceptions.custom_exceptions import BadReferenceError, MissingReferenceError
from models.base_model import BaseModel

T = TypeVar("T", bound="TotalmobileReferenceFRSModel")


class IncomingRequestResult(TypedDict):
    identity: Dict[str, Any]


class IncomingRequest(TypedDict):
    visit: IncomingRequestResult


class TotalmobileReferenceFRSModel(BaseModel):
    questionnaire_guid: str
    questionnaire_name: str
    case_id: str
    interviewer_name: str
    interviewer_blaise_login: str

    def __init__(self, questionnaire_guid, questionnaire_name: str, case_id: str, interviewer_name: str, interviewer_blaise_login: str):
        self.questionnaire_guid = questionnaire_guid
        self.questionnaire_name = questionnaire_name
        self.case_id = case_id
        self.interviewer_name = interviewer_name
        self.interviewer_blaise_login = interviewer_blaise_login

    @classmethod
    def from_reference(cls: Type[T], reference: str) -> T:
        return cls.get_model_from_reference(reference)

    @classmethod
    def from_request(cls: Type[T], request: IncomingRequest) -> T:
        questionnaire_guid_reference = cls.get_questionnaire_guid_reference_from_incoming_request(request)
        questionnaire_case_reference = cls.get_questionnaire_case_reference_from_incoming_request(request)
        interviewer_name_reference = cls.get_interviewer_reference_from_incoming_request(request)
        interviewer_blaise_login_reference = cls.get_interviewer_login_reference_from_incoming_request(request)
        return cls.get_model_from_reference(questionnaire_guid_reference, questionnaire_case_reference, interviewer_name_reference,interviewer_blaise_login_reference)

    @classmethod
    def from_questionnaire_and_case_and_interviewer(
        cls: Type[T], questionnaire_guid: Optional[str], questionnaire_name: Optional[str], case_id: Optional[str], interviewer_name:Optional[str], interviewer_blaise_login:Optional[str]
    ) -> T:
        if (
            questionnaire_guid is None
            or questionnaire_guid == ""
            or questionnaire_name is None
            or questionnaire_name == ""
            or case_id is None
            or case_id == ""
            or interviewer_name is None
            or interviewer_name == ""
            or interviewer_blaise_login is None
            or interviewer_blaise_login == ""
        ):
            raise MissingReferenceError()

        return cls(questionnaire_guid=questionnaire_guid, questionnaire_name=questionnaire_name, case_id=case_id, interviewer_name=interviewer_name, interviewer_blaise_login=interviewer_blaise_login)

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
    def get_questionnaire_case_reference_from_incoming_request(incoming_request: IncomingRequest):
        reference = TotalmobileReferenceFRSModel.get_dictionary_keys_value_if_they_exist(
            incoming_request, "visit", "identity", "reference"
        )

        if reference is None:
            logging.error("Unique reference is missing from the Totalmobile payload")
            raise MissingReferenceError()

        return reference
    
    @staticmethod
    def get_questionnaire_guid_reference_from_incoming_request(incoming_request: IncomingRequest):
        guid_reference = TotalmobileReferenceFRSModel.get_dictionary_keys_value_if_they_exist(
            incoming_request, "visit", "identity", "guid"
        )

        if guid_reference is None:
            logging.error("Unique GUID reference is missing from the Totalmobile payload")
            raise MissingReferenceError()

        return guid_reference
    
    @staticmethod
    def get_interviewer_reference_from_incoming_request(incoming_request: IncomingRequest):
        reference = TotalmobileReferenceFRSModel.get_dictionary_keys_value_if_they_exist(
            incoming_request, "visit", "identity", "user", "name"
        )

        if reference is None:
            logging.error("Unique Interviewer reference is missing from the Totalmobile payload")
            raise MissingReferenceError()

        return reference
    
    @staticmethod
    def get_interviewer_login_reference_from_incoming_request(incoming_request: IncomingRequest):
        user_attributes = TotalmobileReferenceFRSModel.get_dictionary_keys_value_if_they_exist(
            incoming_request, "visit", "identity", "user", "userAttributes"
        )

        if user_attributes is None:
            logging.error("Interviewer Attributes reference is missing from the Totalmobile payload")
            raise MissingReferenceError()

        else:
            login_value = None
            for attribute in user_attributes:
                if attribute["Name"] == "BlaiseLogin":
                    login_value = attribute["Value"]
                    break 
        
        return login_value

    @staticmethod
    def get_model_from_reference(questionnaire_guid, questionnaire_case_reference: str, interviewer_name_reference: str, interviewer_login_reference : str):
        questionnaire_case_request_fields = TotalmobileReferenceFRSModel.get_fields_from_reference(questionnaire_case_reference)
        questionnaire_name = questionnaire_case_request_fields[0]
        case_id = questionnaire_case_request_fields[1]
        return TotalmobileReferenceFRSModel(
            questionnaire_guid=questionnaire_guid, questionnaire_name=questionnaire_name, case_id=case_id, interviewer_name=interviewer_name_reference,interviewer_blaise_login=interviewer_login_reference
        )
