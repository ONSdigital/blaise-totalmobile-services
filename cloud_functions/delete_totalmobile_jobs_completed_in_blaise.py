from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService


def delete_totalmobile_jobs_completed_in_blaise(
    delete_totalmobile_jobs_service: DeleteTotalmobileJobsService,
) -> str:
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()
    return "Done"
