import os
import sys

from appconfig import Config
from services.blaise_service import RealBlaiseService
from services.create.datastore_service import DatastoreService
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
from services.create.questionnaires.eligibility.lms_eligible_case_service import (
    LMSEligibleCaseService,
)
from services.create.questionnaires.lms_questionnaire_service import (
    LMSQuestionnaireService,
)
from services.create.uac.uac_service import UacService


def __check_for_env_var(name: str):
    value = os.environ.get(name, None)
    if value is None:
        print(f"Environment variable ${name} must be set.")
        exit(1)


if __name__ == "__main__":
    __check_for_env_var("BUS_API_URL")
    __check_for_env_var("BUS_CLIENT_ID")
    __check_for_env_var("BLAISE_API_URL")
    __check_for_env_var("BLAISE_SERVER_PARK")

    if len(sys.argv) != 2:
        repository_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        print(
            f"Usage: PYTHONPATH={repository_root} python {sys.argv[0]} QUESTIONNAIRE_NAME"
        )
        exit(1)

    questionnaire_name = sys.argv[1]

    config = Config.from_env()
    eligible_case_service = LMSEligibleCaseService(
        wave_filters=[
            CaseFilterWave1(),
            CaseFilterWave2(),
            CaseFilterWave3(),
            CaseFilterWave4(),
            CaseFilterWave5(),
        ]
    )
    questionnaire_service = LMSQuestionnaireService(
        blaise_service=RealBlaiseService(config),
        eligible_case_service=eligible_case_service,
        datastore_service=DatastoreService(),
        uac_service=UacService(config),
    )
    cases = questionnaire_service.get_cases(questionnaire_name)
    eligible_cases = eligible_case_service.get_eligible_cases(cases)

    eligible_count = 0
    ineligible_count = 0
    for case in cases:
        if case in eligible_cases:
            eligible = "eligible"
            eligible_count += 1
        else:
            eligible = "not-eligible"
            ineligible_count += 1

        print(f"{case.case_id} {eligible}")

    print()
    print(
        f"Total eligible = {eligible_count} / Total not-eligible = {ineligible_count}"
    )
