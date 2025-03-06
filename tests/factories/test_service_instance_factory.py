import pytest

from factories.service_instance_factory import ServiceInstanceFactory
from services.create.questionnaires.frs_questionnaire_service import (
    FRSQuestionnaireService,
)
from services.create.questionnaires.lms_questionnaire_service import (
    LMSQuestionnaireService,
)


def test_create_questionnaire_service_returns_lms_questionnaire_service_when_given_an_lms_survey_type():
    # arrange
    service_instance_factory = ServiceInstanceFactory()

    # act
    result = service_instance_factory.create_questionnaire_service("LMS")

    # assert
    assert type(result) is LMSQuestionnaireService


def test_create_questionnaire_service_returns_frs_questionnaire_service_when_given_an_frs_survey_type():
    # arrange
    service_instance_factory = ServiceInstanceFactory()

    # act
    result = service_instance_factory.create_questionnaire_service("FRS")

    # assert
    assert type(result) is FRSQuestionnaireService


@pytest.mark.parametrize(
    "survey_type",
    [None, 0, "", "Bendyschnapps Cabbagepatch"],
)
def test_create_questionnaire_service_raises_an_exception_when_survey_type_not_found(
    survey_type,
):
    # arrange
    service_instance_factory = ServiceInstanceFactory()

    # act & assert
    with pytest.raises(Exception):
        service_instance_factory.create_questionnaire_service(survey_type)
