from collections import defaultdict
from typing import Dict, List

from client.optimise import GetJobsResponse
from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel


class Job:
    reference: str
    case_id: str
    visit_complete: bool

    def __init__(self, reference: str, case_id: str, visit_complete: bool):
        self.reference = reference
        self.case_id = case_id
        self.visit_complete = visit_complete


class TotalmobileGetJobsResponseModel:
    questionnaire_jobs: Dict[str, List[Job]]

    def __init__(self, jobs: GetJobsResponse):
        questionnaire_jobs = defaultdict(list)

        for job in jobs:
            visit_complete = job["visitComplete"]
            job_reference = job["identity"]["reference"]

            reference_model = TotalmobileReferenceModel.from_reference(job_reference)

            job_instance = Job(job_reference, reference_model.case_id, visit_complete)
            questionnaire_jobs[reference_model.questionnaire_name].append(job_instance)

        self.questionnaire_jobs = dict(questionnaire_jobs)

    def questionnaires_with_incomplete_jobs(self) -> Dict[str, List[Job]]:
        questionnaire_jobs = {}

        for questionnaire_name in self.questionnaire_jobs.keys():
            if all(
                job.visit_complete
                for job in self.questionnaire_jobs[questionnaire_name]
            ):
                continue

            questionnaire_jobs[questionnaire_name] = self.questionnaire_jobs[
                questionnaire_name
            ]

        return questionnaire_jobs
