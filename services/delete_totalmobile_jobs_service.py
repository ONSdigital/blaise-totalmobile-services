from services.blaise_service import BlaiseService
from services.totalmobile_service import TotalmobileService


class DeleteTotalmobileJobsService:
    world_id: str

    def __init__(
        self, totalmobile_service: TotalmobileService, blaise_service: BlaiseService
    ):
        self.totalmobile_service = totalmobile_service
        self.blaise_service = blaise_service
        self.world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    def delete_totalmobile_jobs_completed_in_blaise(self) -> None:
        totalmobile_jobs_model = self.totalmobile_service.get_jobs_model(self.world_id)

        for questionnaire_name in totalmobile_jobs_model.questionnaire_jobs.keys():
            completed_case_ids = self.get_completed_blaise_cases(questionnaire_name)

            for job in totalmobile_jobs_model.questionnaire_jobs[questionnaire_name]:
                if job.visit_complete is False and job.case_id in completed_case_ids:
                    self.totalmobile_service.delete_job(
                        self.world_id, job.reference, "110"
                    )

    def get_completed_blaise_cases(self, questionnaire_name) -> list[str]:
        case_status_list = self.blaise_service.get_case_status_information(
            questionnaire_name
        )
        return [
            case["primaryKey"] for case in case_status_list if case["outcome"] == 110
        ]
