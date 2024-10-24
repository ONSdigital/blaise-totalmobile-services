import calendar
import re
from datetime import datetime
from typing import Any


class FRSCaseModel:
    def __init__(
        self,
        user: str,
        questionnaire_name: str,
        guid: str,
        case_id: str,
        custom_use: str,
        location: str,
        inPosession: str,
        prem1: str,
        prem2: str,
        town: str,
        postcode: str,
    ) -> None:
        self.user = user
        self.questionnaire_name = questionnaire_name
        self.guid = guid
        self.case_id = case_id
        self.custom_use = custom_use
        self.location = location
        self.inPossession = inPosession
        self.prem1 = prem1
        self.prem2 = prem2
        self.town = town
        self.postcode = postcode

        self.full_date = self.get_full_date()
        self.year = self.get_year()
        self.month = self.get_month_name()
        self.eleventh_day_of_next_month = self.calculate_eleventh_day_of_next_month()
        self.tla = self.get_tla()

        self.key_names = self.format_key_names()
        self.key_values = self.format_key_values()
        self.data_fields = self.format_data_fields()

    def format_data_fields(self) -> dict[str, Any]:
        return {
            "mainSurveyID": f"{self.guid}",
            "surveyDisplayName": f"{self.questionnaire_name}",
            "id": f"{self.case_id}",
            "cmA_ForWhom": f"{self.user}",
            "cmA_EndDate": f"{self.eleventh_day_of_next_month}",
            "cmA_CustomUse": f"{self.custom_use}",
            "cmA_Location": f"{self.location}",
            "cmA_InPossession": f"{self.inPossession}",
            "cmA_ContactData": f"PII.TLA\tFRS\tPII.Month\t{self.get_month_name()}\tPII.Year\t{self.get_year()}\tPII.Prem1\t{self.prem1}\tPII.Prem2\t{self.prem2}\tPII.Town\t{self.town}\tPII.Postcode\t{self.postcode}",
        }

    def format_key_values(self) -> list[str]:
        return [self.guid, self.case_id]

    @staticmethod
    def format_key_names() -> list[str]:
        return ["MainSurveyID", "ID"]

    def get_full_date(self):
        pattern = r"([A-Za-z]+)(\d{2})(\d{2})"
        match = re.match(pattern, self.questionnaire_name)
        if match:
            return match.group(2) + match.group(3)

    def get_year(self):
        pattern = r"([A-Za-z]+)(\d{2})(\d{2})"
        match = re.match(pattern, self.questionnaire_name)
        if match:
            return "20" + match.group(2)

    def get_month_name(self):
        pattern = r"([A-Za-z]+)(\d{2})(\d{2})"
        match = re.match(pattern, self.questionnaire_name)
        if match:
            return datetime.strptime(match.group(3), "%m").strftime("%B")

    def get_tla(self):
        pattern = r"^[a-zA-Z]{3}"
        match = re.match(pattern, self.questionnaire_name)
        return match.group(0)[:3] if match else None

    def calculate_eleventh_day_of_next_month(self):
        month_number = list(calendar.month_name).index(self.month)
        return datetime(int(self.year), month_number + 1, 11).strftime("%d-%m-%Y")
