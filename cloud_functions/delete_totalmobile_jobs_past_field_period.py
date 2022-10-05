from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService


def delete_totalmobile_jobs_past_field_period(
    delete_totalmobile_jobs_service: DeleteTotalmobileJobsService,
) -> str:
    delete_totalmobile_jobs_service.delete_jobs_past_field_period()
    return "Done"
