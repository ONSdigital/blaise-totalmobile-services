from abc import abstractmethod
from typing import Dict, Optional

from models.common.blaise.lms_blaise_case_model import LMSBlaiseCaseModel
from models.create.blaise.questionnaire_uac_model import UacChunks


class BlaiseCreateCaseModel(LMSBlaiseCaseModel):
    def __init__(
        self,
        questionnaire_name: str,
        case_data: Dict[str, str],
        uac_chunks: Optional[UacChunks] = None,
    ):
        self._uac_chunks = uac_chunks
        super().__init__(questionnaire_name, case_data)

    @property
    def uac_chunks(self) -> Optional[UacChunks]:
        return self._uac_chunks

    @abstractmethod
    def create_case_overview_for_interviewer(self) -> dict[str, str]:
        pass

    @abstractmethod
    def create_case_description_for_interviewer(self) -> str:
        pass
