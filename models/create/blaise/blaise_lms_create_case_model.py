from typing import Dict, List, Optional

from enums.blaise_fields import BlaiseFields
from models.create.blaise.blaise_create_case_model import BlaiseCreateCaseModel
from models.create.blaise.questionnaire_uac_model import UacChunks


class BlaiseLMSCreateCaseModel(BlaiseCreateCaseModel):
    def __init__(
        self,
        questionnaire_name: str,
        case_data: Dict[str, str],
        uac_chunks: Optional[UacChunks],
    ):
        super().__init__(questionnaire_name, case_data, uac_chunks)

    def create_case_overview_for_interviewer(self) -> dict[str, str]:
        return {
            "surveyName": f"{self.data_model_name}",
            "tla": f"{self.tla}",
            "wave": f"{self.wave}",
            "priority": f"{self.priority}",
            "fieldRegion": f"{self.field_region}",
            "fieldTeam": f"{self.field_team}",
            "postCode": f"{self.postcode}",
            "localAuth": f"{self.local_auth}",
        }

    def create_case_description_for_interviewer(self) -> str:
        uac_string = (
            "" if self.uac_chunks is None else self.uac_chunks.formatted_chunks()
        )
        due_date_string = (
            "" if self.wave_com_dte is None else self.wave_com_dte.strftime("%d/%m/%Y")
        )
        return (
            f"UAC: {uac_string}\n"
            f"Due Date: {due_date_string}\n"
            f"Study: {self.questionnaire_name}\n"
            f"Case ID: {self.case_id}\n"
            f"Wave: {self.wave if self.wave is not None else ''}"
        )

    @staticmethod
    def required_fields() -> List:
        return [
            BlaiseFields.case_id,
            BlaiseFields.data_model_name,
            BlaiseFields.tla,
            BlaiseFields.wave,
            BlaiseFields.address_line_1,
            BlaiseFields.address_line_2,
            BlaiseFields.address_line_3,
            BlaiseFields.county,
            BlaiseFields.town,
            BlaiseFields.postcode,
            BlaiseFields.telephone_number_1,
            BlaiseFields.telephone_number_2,
            BlaiseFields.appointment_telephone_number,
            BlaiseFields.outcome_code,
            BlaiseFields.reference,
            BlaiseFields.latitude,
            BlaiseFields.longitude,
            BlaiseFields.priority,
            BlaiseFields.field_case,
            BlaiseFields.field_region,
            BlaiseFields.field_team,
            BlaiseFields.wave_com_dte,
            BlaiseFields.call_history,
            BlaiseFields.rotational_knock_to_nudge_indicator,
            BlaiseFields.rotational_outcome_code,
        ]
