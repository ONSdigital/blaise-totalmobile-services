import pytest

from appconfig import Config, ConfigError


def test_config_validate():
    config = Config(
        "foo",
        "bar",
        "fwibble",
        "fish",
        "queue-id",
        "cloud-function",
        "blaise-sandbox",
        "region",
        "rest_api_url",
        "gusty",
        "cloud_function_sa",
        "bus_url",
        "bus_client_id"
    )
    config.validate()


def test_config_validate_err():
    config = Config(
        "",
        "",
        "fwibble",
        "fish",
        "queue-id",
        "cloud-function",
        "blaise-sandbox",
        "region",
        "rest_api_url",
        "gusty",
        "cloud_function_sa",
        "bus_url",
        "bus_client_id"
    )
    with pytest.raises(ConfigError) as err:
        config.validate()
    assert (
        str(err.value)
        == "Config fields not set: ['totalmobile_url', 'totalmobile_instance']"
    )


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
        bus_url="",
        bus_client_id=""
    )
