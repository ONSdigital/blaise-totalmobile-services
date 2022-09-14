import logging

from models.totalmobile.totalmobile_jobs_response_model import (
    TotalmobileJobsResponseModel,
)
from services.blaise_service import BlaiseService
from services.totalmobile_service import TotalmobileService


class DeleteTotalmobileJobsService:
    def __init__(
        self, totalmobile_service: TotalmobileService, blaise_service: BlaiseService
    ):
        self.totalmobile_service = totalmobile_service
        self.blaise_service = blaise_service

    def delete_totalmobile_jobs_completed_in_blaise(self) -> None:
        world_id = self.get_world_id()
        totalmobile_jobs_model = self.totalmobile_service.get_jobs_model(world_id)

        for questionnaire_name in totalmobile_jobs_model.questionnaire_jobs.keys():
            if self.questionnaire_has_incomplete_cases(
                questionnaire_name, totalmobile_jobs_model
            ):
                continue

            completed_case_ids = self.get_completed_blaise_cases(questionnaire_name)

            for job in totalmobile_jobs_model.questionnaire_jobs[questionnaire_name]:
                if job.visit_complete is False and job.case_id in completed_case_ids:
                    self.totalmobile_service.delete_job(world_id, job.reference, "110")
                    logging.info(
                        f"Successfully removed job {job.reference} from Totalmobile"
                    )

    def get_completed_blaise_cases(self, questionnaire_name) -> list[str]:
        cases = self.blaise_service.get_cases(
            questionnaire_name
        )
        return [
            case.case_id for case in cases if case.outcome_code == 110
        ]

    @staticmethod
    def questionnaire_has_incomplete_cases(
        questionnaire_name: str, totalmobile_jobs_model: TotalmobileJobsResponseModel
    ) -> bool:
        return all(
            job.visit_complete
            for job in totalmobile_jobs_model.questionnaire_jobs[questionnaire_name]
        )

    def get_world_id(self):
        world_model = self.totalmobile_service.get_world_model()
        for world in world_model.worlds:
            if world.region == "Region 1":
                return world.id
