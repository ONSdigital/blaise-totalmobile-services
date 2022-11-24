from services.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.delete_totalmobile_job_service import DeleteTotalmobileJobService
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from services.logging_totalmobile_service import LoggingTotalmobileService
from services.totalmobile_service import TotalmobileService


def delete_totalmobile_jobs_completed_in_blaise(
    blaise_outcome_service: BlaiseCaseOutcomeService,
    totalmobile_service: TotalmobileService,
):
    logging_totalmobile_service = LoggingTotalmobileService(totalmobile_service)
    DeleteTotalmobileJobsService(
        totalmobile_service=logging_totalmobile_service,
        blaise_outcome_service=blaise_outcome_service,
        delete_totalmobile_job_service=DeleteTotalmobileJobService(
            logging_totalmobile_service
        ),
    ).delete_jobs_for_completed_cases()

    return "Done"
