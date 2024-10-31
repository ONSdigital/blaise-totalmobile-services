import logging
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
    def start_date(self) -> Optional[str]:
        return self.case_data.get(BlaiseFields.start_date)

    @property
    def rand(self) -> Optional[str]:
        return self.case_data.get(BlaiseFields.rand)

    def create_case_overview_for_interviewer(self) -> dict[str, str]:
        return {
            "tla": f"{self.tla}",
            "rand": f"{self.rand}",
            "fieldRegion": f"{self.field_region}",
            "fieldTeam": f"{self.field_team}",
            "postCode": f"{self.postcode}",
            "reference": f"{self.reference}",
        }

    def create_case_description_for_interviewer(
        self,
    ) -> str:
        try:
            datetime.strptime(f"{self.start_date}", "%d-%m-%Y")
            start_date = self.start_date
        except:
            logging.warning(
                f"Invalid Start date retrieved from data in Questionnaire {self.questionnaire_name}"
            )
            start_date = "Not Available"

        if self.divided_address_indicator == "1":
            return f"Warning - Divided Address\n" f"Start date: {start_date}"

        return f"Start date: {start_date}"

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
            BlaiseFields.field_region,
            BlaiseFields.field_team,
            BlaiseFields.wave_com_dte,
            BlaiseFields.divided_address_indicator,
            BlaiseFields.start_date,
            BlaiseFields.rand,
        ]
