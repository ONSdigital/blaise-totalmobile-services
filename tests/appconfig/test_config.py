from appconfig import Config

import pytest
import os

@pytest.fixture
def set_env_variables():
    os.environ['totalmobile_url'] = 'https://ons-dev.totalmobile-cloud.com'
    os.environ['totalmobile_instance'] = 'Test'
    os.environ['totalmobile_client_id'] = 'ons.d.api'
    os.environ['totalmobile_client_secret'] = 'ZfeeAV6DnvqN@!'
    os.environ['create_totalmobile_jobs_task_queue_id'] = ''
    os.environ['gcloud_project'] = ''
    os.environ['region'] = ''
    os.environ['blaise_api_url'] = ''
    os.environ['blaise_server_park'] = ''
    os.environ['cloud_function_sa'] = ''
    os.environ['bus_api_url'] = ''
    os.environ['bus_client_id'] = ''

def test_config_from_env(set_env_variables):
    config = Config.from_env()
    assert config == Config(
        totalmobile_url="https://ons-dev.totalmobile-cloud.com",
        totalmobile_instance="Test",
        totalmobile_client_id="ons.d.api",
        totalmobile_client_secret="ZfeeAV6DnvqN@!",
        create_totalmobile_jobs_task_queue_id="",
        gcloud_project="",
        region="",
        blaise_api_url="",
        blaise_server_park="",
        cloud_function_sa="",
        bus_api_url="",
        bus_client_id="",
    )
