from typing import List, Dict

from app.exceptions.custom_exceptions import BadReferenceError, MissingReferenceError


class TotalmobileReferenceService:

    @staticmethod
    def create_reference(questionnaire_name: str, case_id: str) -> str:
        return f"{questionnaire_name.replace('_', '-')}.{case_id}"

    @staticmethod
    def get_questionnaire_name_from_reference(reference: str) -> str:
        reference_fields = TotalmobileReferenceService.get_fields_from_reference(reference)

        return reference_fields[0]

    @staticmethod
    def get_case_id_from_reference(reference: str) -> str:
        reference_fields = TotalmobileReferenceService.get_fields_from_reference(reference)

        return reference_fields[1]

    @staticmethod
    def get_fields_from_reference(reference: str) -> List[str]:
        reference_fields = reference.split(".", 2)

        if len(reference_fields) != 2:
            raise BadReferenceError()

        if reference_fields[0] == "" or reference_fields[1] == "":
            raise BadReferenceError()

        return reference_fields

    @staticmethod
    def get_reference_from_incoming_request(incoming_request: Dict[str, str]):

        if (
                "Result" not in incoming_request
                or "Association" not in incoming_request["Result"]
                or "Reference" not in incoming_request["Result"]["Association"]
                or incoming_request["Result"]["Association"]["Reference"] == ""
        ):
            raise MissingReferenceError()

        return incoming_request["Result"]["Association"]["Reference"]
