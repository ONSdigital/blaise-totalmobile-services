from services.create_totalmobile_jobs_service import CreateTotalmobileJobsService


def create_totalmobile_jobs_trigger(
    create_totalmobile_jobs_service: CreateTotalmobileJobsService,
) -> str:

    return create_totalmobile_jobs_service.create_totalmobile_jobs()
