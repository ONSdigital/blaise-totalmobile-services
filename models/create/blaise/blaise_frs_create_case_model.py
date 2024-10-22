import re
from datetime import datetime
from typing import Dict, List, Optional

from enums.blaise_fields import BlaiseFields
from models.create.blaise.blaise_create_case_model import BlaiseCreateCaseModel


class BlaiseFRSCreateCaseModel(BlaiseCreateCaseModel):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        super().__init__(questionnaire_name, case_data)

    @property
    def divided_address_indicator(self) -> Optional[str]:
        return self.case_data.get(BlaiseFields.divided_address_indicator)

    @property
    def rand(self) -> Optional[str]:
        return self.case_data.get(BlaiseFields.rand)

    def get_year(self):
        pattern = r"([A-Za-z]+)(\d{2})(\d{2})"
        match = re.match(pattern, self.questionnaire_name)
        if match:
            return "20" + match.group(2)

    def get_month(self):
        pattern = r"([A-Za-z]+)(\d{2})(\d{2})"
        match = re.match(pattern, self.questionnaire_name)
        return match.group(3)

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
        start_date_from_case = self.case_data.get(BlaiseFields.start_date)
        start_date = f"Start date: {start_date_from_case}"

        if self.divided_address_indicator == "1":
            return f"Warning - Divided Address\n{start_date}"

        if self.divided_address_indicator == "0":
            return start_date

        return ""

    @staticmethod
    def required_fields() -> List:
        return [
            BlaiseFields.case_id,
            BlaiseFields.tla,
            BlaiseFields.address_line_1,
            BlaiseFields.address_line_2,
            BlaiseFields.address_line_3,
            BlaiseFields.county,
            BlaiseFields.town,
            BlaiseFields.postcode,
            BlaiseFields.reference,
            BlaiseFields.latitude,
            BlaiseFields.longitude,
            BlaiseFields.priority,
            BlaiseFields.field_case,
            BlaiseFields.field_region,
            BlaiseFields.field_team,
            BlaiseFields.divided_address_indicator,
            BlaiseFields.start_date,
            BlaiseFields.rand,
        ]
