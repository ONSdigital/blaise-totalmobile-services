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


class TotalmobileJobsModel:
    questionnaire_jobs: Dict[str, List[Job]]

    def __init__(self, jobs: GetJobsResponse):
        self.questionnaire_jobs = {}

        for job in jobs:
            visit_complete = True if job["visitComplete"] == "True" else False
            job_reference = job["identity"]["reference"]

            reference_model = TotalmobileReferenceModel.from_reference(job_reference)

            if reference_model.questionnaire_name in self.questionnaire_jobs.keys():
                self.questionnaire_jobs[reference_model.questionnaire_name].append(
                    Job(job_reference, reference_model.case_id, visit_complete)
                )
            else:
                self.questionnaire_jobs[reference_model.questionnaire_name] = [
                    Job(job_reference, reference_model.case_id, visit_complete)
                ]
