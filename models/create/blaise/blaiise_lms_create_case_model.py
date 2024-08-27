from typing import Dict, List, Optional

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
            "qiD.Serial_Number",
            "dataModelName",
            "qDataBag.TLA",
            "qDataBag.Wave",
            "qDataBag.Prem1",
            "qDataBag.Prem2",
            "qDataBag.Prem3",
            "qDataBag.District",
            "qDataBag.PostTown",
            "qDataBag.PostCode",
            "qDataBag.TelNo",
            "qDataBag.TelNo2",
            "telNoAppt",
            "hOut",
            "qDataBag.UPRN",
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",
            "qDataBag.Priority",
            "qDataBag.FieldCase",
            "qDataBag.FieldRegion",
            "qDataBag.FieldTeam",
            "qDataBag.WaveComDTE",
            "catiMana.CatiCall.RegsCalls[1].DialResult",
            "qRotate.RDMktnIND",
            "qRotate.RHOut",
        ]
