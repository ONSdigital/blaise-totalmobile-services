from typing import Dict, List, Optional

from models.create.blaise.blaise_create_case_model import BlaiseCreateCaseModel


class BlaiseFRSCaseModel(BlaiseCreateCaseModel):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        super().__init__(questionnaire_name, case_data)

    @property
    def divided_address_indicator(self) -> Optional[str]:
        return self.case_data.get("qDataBag.DivAddInd")

    @property
    def rand(self) -> Optional[str]:
        return self.case_data.get("qDataBag.Rand")

    def create_case_overview_for_interviewer(self) -> dict[str, str]:
        return {
            "tla": f"{self.tla}",
            "rand": f"{self.rand}",
            "fieldRegion": f"{self.field_region}",
            "fieldTeam": f"{self.field_team}",
            "postCode": f"{self.postcode}",
        }

    def create_case_description_for_interviewer(
        self,
    ) -> str:
        if self.divided_address_indicator == "1":
            return "Warning Divided Address"
        return ""

    @staticmethod
    def required_fields() -> List:
        return [
            "qiD.Serial_Number",
            "dataModelName",
            "qDataBag.TLA",
            "qDataBag.Prem1",
            "qDataBag.Prem2",
            "qDataBag.Prem3",
            "qDataBag.District",
            "qDataBag.PostTown",
            "qDataBag.PostCode",
            "qDataBag.UPRN",
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",
            "qDataBag.Priority",
            "qDataBag.FieldCase",
            "qDataBag.FieldRegion",
            "qDataBag.FieldTeam",
            "qDataBag.DivAddInd",
            "qDataBag.Rand",
        ]
