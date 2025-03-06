from unittest.mock import MagicMock

import pytest

from factories.service_instance_factory import ServiceInstanceFactory
from services.blaise_service import RealBlaiseService
from services.cloud_task_service import CloudTaskService
from services.create.create_totalmobile_jobs_service import CreateTotalmobileJobsService
from services.create.datastore_service import DatastoreService
from services.create.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_1 import (
    CaseFilterWave1,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_2 import (
    CaseFilterWave2,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_3 import (
    CaseFilterWave3,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_4 import (
    CaseFilterWave4,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_5 import (
    CaseFilterWave5,
)
from services.create.questionnaires.eligibility.frs_eligible_case_service import (
    FRSEligibleCaseService,
)
from services.create.questionnaires.eligibility.lms_eligible_case_service import (
    LMSEligibleCaseService,
)
from services.create.questionnaires.frs_questionnaire_service import (
    FRSQuestionnaireService,
)
from services.create.questionnaires.lms_questionnaire_service import (
    LMSQuestionnaireService,
)
from services.create.uac.uac_service import UacService
from services.delete.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.delete.delete_cma_case_service import DeleteCMACaseService
from services.totalmobile_service import RealTotalmobileService, TotalmobileService
from services.update.frs_update_case_service import FRSUpdateCaseService
from services.update.lms_update_case_service import LMSUpdateCaseService
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService


@pytest.fixture
def service_instance_factory():
    return ServiceInstanceFactory()


@pytest.fixture
def mock_blaise_service():
    return MagicMock(spec=RealBlaiseService)


@pytest.fixture
def mocker_blaise_service(mocker, service_instance_factory):
    return mocker.patch.object(
        service_instance_factory, "create_blaise_service", return_value="mock_blaise"
    )


@pytest.fixture
def mocker_datastore_service(mocker, service_instance_factory):
    return mocker.patch.object(
        service_instance_factory,
        "create_datastore_service",
        return_value="mock_datastore",
    )


@pytest.fixture
def mocker_eligible_case_service(mocker, service_instance_factory):
    return mocker.patch.object(
        service_instance_factory,
        "create_eligible_lms_case_service",
        return_value="mock_eligible_case",
    )


@pytest.fixture
def mocker_uac_service(mocker, service_instance_factory):
    return mocker.patch.object(
        service_instance_factory, "create_uac_service", return_value="mock_uac"
    )


def test_create_blaise_service_returns_real_blaise_service(service_instance_factory):
    # act
    result = service_instance_factory.create_blaise_service()

    # assert
    assert isinstance(result, RealBlaiseService)
    assert not isinstance(result, FakeBlaiseService)


def test_create_datastore_service_returns_datastore_service(service_instance_factory):
    # act & assert
    assert isinstance(
        service_instance_factory.create_datastore_service(), DatastoreService
    )


def test_create_eligible_lms_case_service_returns_lms_eligible_case_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_eligible_lms_case_service(),
        LMSEligibleCaseService,
    )


def test_create_eligible_lms_case_service_contains_correct_filters(
    service_instance_factory,
):
    # arrange
    expected_filters = [
        CaseFilterWave1,
        CaseFilterWave2,
        CaseFilterWave3,
        CaseFilterWave4,
        CaseFilterWave5,
    ]

    # act
    result = service_instance_factory.create_eligible_lms_case_service()

    # assert
    assert len(result._wave_filters) == len(expected_filters)
    assert all(
        isinstance(filter, expected_class)
        for filter, expected_class in zip(result._wave_filters, expected_filters)
    )


def test_create_eligible_frs_case_service_returns_frs_eligible_case_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_eligible_frs_case_service(),
        FRSEligibleCaseService,
    )


def test_create_update_case_service_returns_lms_update_case_service_when_given_an_lms_survey_type(
    service_instance_factory, mock_blaise_service
):
    # act & assert
    assert isinstance(
        service_instance_factory.create_update_case_service("LMS", mock_blaise_service),
        LMSUpdateCaseService,
    )


def test_create_update_case_service_returns_frs_update_case_service_when_given_an_frs_survey_type(
    service_instance_factory, mock_blaise_service
):
    # act & assert
    assert isinstance(
        service_instance_factory.create_update_case_service("FRS", mock_blaise_service),
        FRSUpdateCaseService,
    )


@pytest.mark.parametrize(
    "survey_type",
    [None, 0, "", "Bendyschnapps Cabbagepatch"],
)
def test_create_update_case_service_raises_an_exception_when_survey_type_not_found(
    survey_type, service_instance_factory, mock_blaise_service
):
    # act & assert
    with pytest.raises(Exception):
        service_instance_factory.create_update_case_service(
            survey_type, mock_blaise_service
        )


def test_create_questionnaire_service_returns_lms_questionnaire_service_when_given_an_lms_survey_type(
    service_instance_factory,
):
    # act & assert
    assert isinstance(
        service_instance_factory.create_questionnaire_service("LMS"),
        LMSQuestionnaireService,
    )


def test_create_questionnaire_service_returns_frs_questionnaire_service_when_given_an_frs_survey_type(
    service_instance_factory,
):
    # act & assert
    assert isinstance(
        service_instance_factory.create_questionnaire_service("FRS"),
        FRSQuestionnaireService,
    )


@pytest.mark.parametrize(
    "survey_type",
    [None, 0, "", "Bendyschnapps Cabbagepatch"],
)
def test_create_questionnaire_service_raises_an_exception_when_survey_type_not_found(
    survey_type, service_instance_factory
):
    # act & assert
    with pytest.raises(Exception):
        service_instance_factory.create_questionnaire_service(survey_type)


def test_create_lms_questionnaire_service_returns_lms_questionnaire_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_lms_questionnaire_service(),
        LMSQuestionnaireService,
    )


def test_create_lms_questionnaire_service_contains_correct_dependencies(
    service_instance_factory,
    mocker_blaise_service,
    mocker_eligible_case_service,
    mocker_datastore_service,
    mocker_uac_service,
):
    # act
    service = service_instance_factory.create_lms_questionnaire_service()

    # assert
    assert service._blaise_service == "mock_blaise"
    mocker_blaise_service.assert_called_once()

    assert service._eligible_case_service == "mock_eligible_case"
    mocker_eligible_case_service.assert_called_once()

    assert service._datastore_service == "mock_datastore"
    mocker_datastore_service.assert_called_once()

    assert service._uac_service == "mock_uac"
    mocker_uac_service.assert_called_once()


def test_create_frs_questionnaire_service_returns_frs_questionnaire_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_frs_questionnaire_service(),
        FRSQuestionnaireService,
    )


def test_create_frs_questionnaire_service_contains_correct_dependencies(
    service_instance_factory,
    mocker_blaise_service,
    mocker_eligible_case_service,
    mocker_datastore_service,
):
    # act
    service = service_instance_factory.create_lms_questionnaire_service()

    # assert
    assert service._blaise_service == "mock_blaise"
    mocker_blaise_service.assert_called_once()

    assert service._eligible_case_service == "mock_eligible_case"
    mocker_eligible_case_service.assert_called_once()

    assert service._datastore_service == "mock_datastore"
    mocker_datastore_service.assert_called_once()


def test_create_totalmobile_mapper_service_returns_totalmobile_create_job_mapper_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_totalmobile_mapper_service(),
        TotalmobileCreateJobMapperService,
    )


def test_create_totalmobile_service_returns_real_totalmobile_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_totalmobile_service(), RealTotalmobileService
    )
    assert not isinstance(
        service_instance_factory.create_totalmobile_service(), FakeTotalmobileService
    )


def test_create_totalmobile_service_initialises_optimise_client_with_the_expected_configuration_values(
    mocker, service_instance_factory
):
    # arrange
    mock_optimise_client = mocker.patch(
        "factories.service_instance_factory.OptimiseClient", autospec=True
    )

    # act
    service = service_instance_factory.create_totalmobile_service()

    # assert
    mock_optimise_client.assert_called_once_with(
        service_instance_factory._config.totalmobile_url,
        service_instance_factory._config.totalmobile_instance,
        service_instance_factory._config.totalmobile_client_id,
        service_instance_factory._config.totalmobile_client_secret,
    )

    assert service._optimise_client == mock_optimise_client.return_value


def test_create_totalmobile_service_initialises_messaging_client_with_the_expected_configuration_values(
    mocker, service_instance_factory
):
    # arrange
    mock_messaging_client = mocker.patch(
        "factories.service_instance_factory.MessagingClient", autospec=True
    )

    # act
    service = service_instance_factory.create_totalmobile_service()

    # assert
    mock_messaging_client.assert_called_once_with(
        service_instance_factory._config.totalmobile_url,
        service_instance_factory._config.totalmobile_instance,
        service_instance_factory._config.totalmobile_client_id,
        service_instance_factory._config.totalmobile_client_secret,
    )

    assert service._messaging_client == mock_messaging_client.return_value


def test_create_totalmobile_service_calls_mapper_service(
    mocker, service_instance_factory
):
    # arrange
    mock_mapper_service = mocker.patch.object(
        service_instance_factory,
        "create_totalmobile_mapper_service",
        return_value="mock_mapper_service",
    )

    # act
    service = service_instance_factory.create_totalmobile_service()

    # assert
    assert service._mapper == "mock_mapper_service"
    mock_mapper_service.assert_called_once()


def test_create_uac_service_returns_uac_service(service_instance_factory):
    assert isinstance(service_instance_factory.create_uac_service(), UacService)


def test_create_uac_service_initialise_uac_service_with_the_expected_config(
    service_instance_factory, mocker
):
    # arrange
    mock_uac_service = mocker.patch(
        "factories.service_instance_factory.UacService", autospec=True
    )

    # act
    service = service_instance_factory.create_uac_service()

    # assert
    mock_uac_service.assert_called_once_with(
        service_instance_factory._config,
    )
    assert service == mock_uac_service.return_value


def test_create_cloud_task_service_returns_cloud_task_service(service_instance_factory):
    assert isinstance(
        service_instance_factory.create_cloud_task_service(), CloudTaskService
    )


def test_create_cloud_task_service_initialises_cloud_task_service_with_expected_dependencies(
    service_instance_factory, mocker
):
    # arrange
    mock_cloud_task_service = mocker.patch(
        "factories.service_instance_factory.CloudTaskService", autospec=True
    )

    # act
    result = service_instance_factory.create_cloud_task_service()

    # assert
    mock_cloud_task_service.assert_called_once_with(
        config=service_instance_factory._config,
        task_queue_id=service_instance_factory._config.create_totalmobile_jobs_task_queue_id,
    )
    assert result == mock_cloud_task_service.return_value


@pytest.mark.parametrize(
    "survey_type",
    ["LMS", "FRS"],
)
def test_create_totalmobile_jobs_service_returns_create_totalmobile_jobs_service(
    service_instance_factory, survey_type
):
    assert isinstance(
        service_instance_factory.create_totalmobile_jobs_service(
            survey_type=survey_type
        ),
        CreateTotalmobileJobsService,
    )


@pytest.mark.parametrize(
    "survey_type",
    ["LMS", "FRS"],
)
def test_create_totalmobile_jobs_service_calls_create_totalmobile_jobs_service_with_the_expected_dependencies(
    survey_type, service_instance_factory, mocker
):
    # arrange
    mock_totalmobile_service = mocker.patch.object(
        service_instance_factory,
        "create_totalmobile_service",
        return_value="mock_totalmobile",
    )
    mock_questionnaire_service = mocker.patch.object(
        service_instance_factory,
        "create_questionnaire_service",
        return_value="mock_questionnaire",
    )
    mock_cloud_task_service = mocker.patch.object(
        service_instance_factory,
        "create_cloud_task_service",
        return_value="mock_cloud_task",
    )

    # act
    result = service_instance_factory.create_totalmobile_jobs_service(survey_type)

    # assert
    assert result._totalmobile_service == "mock_totalmobile"
    mock_totalmobile_service.assert_called_once()

    assert result._questionnaire_service == "mock_questionnaire"
    mock_questionnaire_service.assert_called_once_with(survey_type)

    assert result._cloud_task_service == "mock_cloud_task"
    mock_cloud_task_service.assert_called_once()


def test_create_blaise_outcome_service_returns_blaise_case_outcome_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_blaise_outcome_service(),
        BlaiseCaseOutcomeService,
    )


def test_create_blaise_outcome_service_calls_blaise_case_outcome_service_with_the_expected_dependencies(
    service_instance_factory, mocker
):
    # arrange
    mock_create_blaise_service = mocker.patch.object(
        service_instance_factory,
        "create_blaise_service",
        return_value="mock_create_blaise_service",
    )

    # act
    result = service_instance_factory.create_blaise_outcome_service()

    # assert
    assert result._blaise_service == "mock_create_blaise_service"
    mock_create_blaise_service.assert_called_once()


def test_create_delete_cma_case_service_returns_delete_cma_case_service(
    service_instance_factory,
):
    assert isinstance(
        service_instance_factory.create_delete_cma_case_service(), DeleteCMACaseService
    )
