from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel
from services.blaise_service import BlaiseService
from services.totalmobile_service import TotalmobileService


class DeleteTotalmobileJobsService:
    def __init__(self, totalmobile_service: TotalmobileService, blaise_service: BlaiseService):
        self.totalmobile_service = totalmobile_service
        self.blaise_service = blaise_service

    def delete_totalmobile_jobs_completed_in_blaise(self) -> None:
        job_references = self.get_incomplete_totalmobile_job_references("13013122-d69f-4d6b-gu1d-721f190c4479")
        totalmobile_reference_models = self.map_reference_models_from_list_of_job_references(job_references)

        questionnaire_name = totalmobile_reference_models[0].questionnaire_name

        completed_case_ids = self.get_completed_blaise_cases(questionnaire_name)

        if totalmobile_reference_models[0].case_id in completed_case_ids:
            self.totalmobile_service.delete_job(
                "13013122-d69f-4d6b-gu1d-721f190c4479", totalmobile_reference_models[0].create_reference(), "110"
            )

    def delete_totalmobile_job(self, world_id: str, job_reference: str, reason: str) -> None:
        self.totalmobile_service.delete_job(world_id, job_reference, reason)

    def get_incomplete_totalmobile_job_references(self, world_id: str) -> list[str]:
        jobs = self.totalmobile_service.get_jobs(world_id)
        return [job["identity"]["reference"] for job in jobs if not job["visitComplete"]]

    def map_reference_models_from_list_of_job_references(
            self, job_references: list[str]
    ) -> list[TotalmobileReferenceModel]:
        reference_models = []
        for job_reference in job_references:
            reference_models.append(TotalmobileReferenceModel.from_reference(job_reference))

        return reference_models

    def get_completed_blaise_cases(self, questionnaire_name):
        case_status_list = self.blaise_service.get_case_status_information(questionnaire_name)
        return [case["primaryKey"] for case in case_status_list if case["outcome"] == 110]
