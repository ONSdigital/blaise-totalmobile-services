from dataclasses import dataclass
from typing import Type, TypeVar, Dict

from services.totalmobile_reference_service import TotalmobileReferenceService

T = TypeVar('T')


@dataclass
class TotalMobileIncomingCaseModel:
    questionnaire_name: str
    case_id: str
    outcome_code: str

    @classmethod
    def import_case(cls: Type[T], incoming_request: Dict[str, str]) -> T:
        reference = TotalmobileReferenceService.get_reference_from_incoming_request(incoming_request)

        total_mobile_case = TotalMobileIncomingCaseModel(
            questionnaire_name=TotalmobileReferenceService.get_questionnaire_name_from_reference(reference),
            case_id=TotalmobileReferenceService.get_case_id_from_reference(reference),
            outcome_code=""
        )

        return total_mobile_case
