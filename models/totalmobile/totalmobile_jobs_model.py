from typing import List, Dict

from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel


class Job:
    reference: str
    case_id: str

    def __init__(self, reference_model: TotalmobileReferenceModel):
        self.reference = reference_model.create_reference()
        self.case_id = reference_model.case_id


class TotalmobileJobsModel:
    questionnaire_jobs: Dict[str, List[Job]]

    def __init__(self, job_references: List[str]):
        self.questionnaire_jobs = {}
        reference_models = self.map_reference_models_from_list_of_job_references(job_references)

        for reference_model in reference_models:
            if reference_model.questionnaire_name in self.questionnaire_jobs.keys():
                self.questionnaire_jobs[reference_model.questionnaire_name]\
                    .append(Job(reference_model))
            else:
                self.questionnaire_jobs[reference_model.questionnaire_name] = [Job(reference_model)]

    @staticmethod
    def map_reference_models_from_list_of_job_references(job_references: list[str]) -> list[TotalmobileReferenceModel]:
        reference_models = []
        for job_reference in job_references:
            reference_models.append(TotalmobileReferenceModel.from_reference(job_reference))

        return reference_models
