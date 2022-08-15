from appconfig import Config, ConfigError


def test_config_from_env():
    config = Config.from_env()
    assert config == Config(
        totalmobile_url="",
        totalmobile_instance="",
        totalmobile_client_id="",
        totalmobile_client_secret="",
        totalmobile_jobs_queue_id="",
        totalmobile_job_cloud_function="",
        gcloud_project="",
        region="",
        blaise_api_url="",
        blaise_server_park="",
        cloud_function_sa="",
        bus_api_url="",
        bus_client_id=""
    )
