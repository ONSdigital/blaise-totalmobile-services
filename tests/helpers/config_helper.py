from appconfig import Config


def get_default_config():
    return Config(
        totalmobile_url="totalmobile_url",
        totalmobile_instance="totalmobile_instance",
        totalmobile_client_id="totalmobile_client_id",
        totalmobile_client_secret="totalmobile_client_secret",
        totalmobile_jobs_queue_id="totalmobile_jobs_queue_id",
        totalmobile_job_cloud_function="totalmobile_job_cloud_function",
        gcloud_project="gcloud_project",
        region="region",
        blaise_api_url="blaise_api_url",
        blaise_server_park="gusty",
        cloud_function_sa="cloud_function_sa",
        bus_api_url="bus_api_url",
        bus_client_id="bus_client_id",
    )
