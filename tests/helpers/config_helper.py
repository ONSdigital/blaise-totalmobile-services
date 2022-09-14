from appconfig import Config


def get_default_config():
    return Config(
        totalmobile_url="totalmobile_url",
        totalmobile_instance="totalmobile_instance",
        totalmobile_client_id="totalmobile_client_id",
        totalmobile_client_secret="totalmobile_client_secret",
        create_totalmobile_jobs_task_queue_id="create_totalmobile_jobs_task_queue_id",
        gcloud_project="gcloud_project",
        region="region",
        blaise_api_url="blaise_api_url",
        blaise_server_park="gusty",
        cloud_function_sa="cloud_function_sa",
        bus_api_url="bus_api_url",
        bus_client_id="bus_client_id",
    )
