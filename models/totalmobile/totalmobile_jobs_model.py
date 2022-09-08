from dataclasses import dataclass
from typing import List, TypeVar, Type, Dict

from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel

T = TypeVar("T", bound="TotalmobileJobsModel")


@dataclass
class Job:
    reference: str
    case_id: str


@dataclass
class TotalmobileJobsModel:
    questionnaire_jobs: Dict[str, List[Job]]

    @classmethod
    def import_job_references(cls: Type[T], job_references: List[str]) -> T:
        cls.questionnaire_jobs = {}
        reference_models = cls.map_reference_models_from_list_of_job_references(job_references)

        for reference_model in reference_models:
            if reference_model.questionnaire_name in cls.questionnaire_jobs.keys():
                cls.questionnaire_jobs[reference_model.questionnaire_name]\
                    .append(cls.map_job_from_reference_model(reference_model))
            else:
                cls.questionnaire_jobs[reference_model.questionnaire_name] = [cls.map_job_from_reference_model(reference_model)]

        return cls.questionnaire_jobs

    @staticmethod
    def map_reference_models_from_list_of_job_references(job_references: list[str]) -> list[TotalmobileReferenceModel]:
        reference_models = []
        for job_reference in job_references:
            reference_models.append(TotalmobileReferenceModel.from_reference(job_reference))

        return reference_models

    @staticmethod
    def map_job_from_reference_model(reference_model: TotalmobileReferenceModel) -> Job:
        return Job(reference=reference_model.create_reference(), case_id=reference_model.case_id)




