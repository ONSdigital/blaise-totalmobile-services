import logging
from typing import List, Dict, Tuple

from app.exceptions.custom_exceptions import BadReferenceError, MissingReferenceError


class TotalmobileReferenceModel:

    questionnaire_name: str
    case_id: str

    def __init__(self, *args: Tuple[any]):
        if len(args) == 1:
            self.initialize_properties_from_request(args)
        elif len(args) == 2:
            self.initialize_properties(args)
        else:
            raise BadReferenceError()

    def initialize_properties_from_request(self, args: tuple[any]):
        reference = self.get_reference_from_incoming_request(args[0])
        request_fields = self.get_fields_from_reference(reference)
        self.questionnaire_name = request_fields[0].replace('-', '_')
        self.case_id = request_fields[1]

    def initialize_properties(self, args: tuple[any]):
        if args[0] is None or args[0] == "" or args[1] is None or args[1] == "":
            raise MissingReferenceError()

        self.questionnaire_name = args[0]
        self.case_id = args[1]

    def create_reference(self) -> str:
        return f"{self.questionnaire_name.replace('_', '-')}.{self.case_id}"

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
            logging.error("Unique reference is missing from totalmobile payload")
            raise MissingReferenceError()

        return incoming_request["Result"]["Association"]["Reference"]
