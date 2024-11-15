from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Type, TypeVar

from app.exceptions.custom_exceptions import BadReferenceError
from client.optimise import GetJobsResponse
from models.common.totalmobile.totalmobile_reference_model import (
    TotalmobileReferenceModel,
)

T = TypeVar("T", bound="TotalmobileGetJobsResponseModel")

SURVEY_DUE_DATE_EXPIRY_OFFSETS: Dict[str, int] = {
    "DEFAULT": 0, 
    "LMS": -3, 
}

@dataclass
class Job:
    reference: str
    case_id: str
    visit_complete: bool
    past_field_period: bool
    allocated_resource_reference: Optional[str]
    work_type: str


class TotalmobileGetJobsResponseModel:
    questionnaire_jobs: Dict[str, List[Job]]

    @classmethod
    def from_get_jobs_response(cls: Type[T], jobs: GetJobsResponse) -> T:
        questionnaire_jobs = defaultdict(list)

        for job in jobs:
            visit_complete = job["visitComplete"]
            job_reference = job["identity"]["reference"]
            due_date = job["dueDate"]["end"]
            allocated_resource_reference = (
                job["allocatedResource"]["reference"]
                if job["allocatedResource"] is not None
                else None
            )
            work_type = job["workType"]

            past_field_period = cls.field_period_has_expired(due_date, work_type)

            try:
                reference_model = TotalmobileReferenceModel.from_reference(
                    job_reference
                )
                job_instance = Job(
                    job_reference,
                    reference_model.case_id,
                    visit_complete,
                    past_field_period,
                    allocated_resource_reference,
                    work_type,
                )
                questionnaire_jobs[reference_model.questionnaire_name].append(
                    job_instance
                )
            except BadReferenceError:
                pass  # The model logs a warning so we just carry on

        return cls(dict(questionnaire_jobs))

    def __init__(self, questionnaire_jobs: Dict[str, List[Job]]):
        self.questionnaire_jobs = questionnaire_jobs

    def questionnaires_with_incomplete_jobs(self) -> Dict[str, List[Job]]:
        questionnaire_jobs: dict[str, list[Any]] = {}

        for questionnaire_name in self.questionnaire_jobs.keys():
            if all(
                job.visit_complete
                for job in self.questionnaire_jobs[questionnaire_name]
            ):
                continue

            questionnaire_jobs[questionnaire_name] = []

            for job in self.questionnaire_jobs[questionnaire_name]:
                if not job.visit_complete:
                    questionnaire_jobs[questionnaire_name].append(job)

        return questionnaire_jobs

    def total_number_of_incomplete_jobs(self) -> int:
        total = 0
        questionnaires_with_incomplete_jobs = self.questionnaires_with_incomplete_jobs()
        for job_list in questionnaires_with_incomplete_jobs.values():
            total += len(job_list)

        return total

    @staticmethod
    def field_period_has_expired(due_date_string: Optional[str], survey_type: str) -> bool:
        if due_date_string is None:
            return False

        try:
            due_date = datetime.strptime(due_date_string, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return False

        expiry_offset = expiry_offset = SURVEY_DUE_DATE_EXPIRY_OFFSETS.get(survey_type, SURVEY_DUE_DATE_EXPIRY_OFFSETS["DEFAULT"])
        expiry_date = due_date + timedelta(days=expiry_offset)

        return datetime.now() > expiry_date
