from appconfig import Config
from client.messaging import MessagingClient
from client.optimise import OptimiseClient
from services.blaise_service import RealBlaiseService
from services.cloud_task_service import CloudTaskService
from services.create.create_totalmobile_jobs_service import CreateTotalmobileJobsService
from services.create.datastore_service import DatastoreService
from services.create.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
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
from services.create.questionnaires.questionnaire_service_base import (
    QuestionnaireServiceBase,
)
from services.create.uac.uac_service import UacService
from services.create.uac.uac_service_base import UacServiceBase
from services.delete.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.totalmobile_service import RealTotalmobileService


class ServiceInstanceFactory:
    def __init__(
        self,
    ):
        self._config = Config.from_env()

    @property
    def config(self):
        return self._config

    def create_blaise_service(self) -> RealBlaiseService:
        return RealBlaiseService(self._config)

    @staticmethod
    def create_datastore_service() -> DatastoreService:
        return DatastoreService()

    @staticmethod
    def create_eligible_lms_case_service() -> LMSEligibleCaseService:
        return LMSEligibleCaseService(
            wave_filters=[
                CaseFilterWave1(),
                CaseFilterWave2(),
                CaseFilterWave3(),
                CaseFilterWave4(),
                CaseFilterWave5(),
            ]
        )

    @staticmethod
    def create_eligible_frs_case_service() -> FRSEligibleCaseService:
        return FRSEligibleCaseService()

    def create_questionnaire_service(
        self, survey_type: str
    ) -> QuestionnaireServiceBase:
        if survey_type == "LMS":
            return self.create_lms_questionnaire_service()
        if survey_type == "FRS":
            return self.create_frs_questionnaire_service()
        raise Exception

    def create_lms_questionnaire_service(self) -> LMSQuestionnaireService:
        return LMSQuestionnaireService(
            blaise_service=self.create_blaise_service(),
            eligible_case_service=self.create_eligible_lms_case_service(),
            datastore_service=self.create_datastore_service(),
            uac_service=self.create_uac_service(),
        )

    def create_frs_questionnaire_service(self) -> FRSQuestionnaireService:
        return FRSQuestionnaireService(
            blaise_service=self.create_blaise_service(),
            eligible_case_service=self.create_eligible_frs_case_service(),
            datastore_service=self.create_datastore_service(),
        )

    @staticmethod
    def create_totalmobile_mapper_service() -> TotalmobileCreateJobMapperService:
        return TotalmobileCreateJobMapperService(TotalmobilePayloadMapperService())

    def create_totalmobile_service(self) -> RealTotalmobileService:
        optimise_client = OptimiseClient(
            self._config.totalmobile_url,
            self._config.totalmobile_instance,
            self._config.totalmobile_client_id,
            self._config.totalmobile_client_secret,
        )
        messaging_client = MessagingClient(
            self._config.totalmobile_url,
            self._config.totalmobile_instance,
            self._config.totalmobile_client_id,
            self._config.totalmobile_client_secret,
        )
        return RealTotalmobileService(
            optimise_client=optimise_client,
            messaging_client=messaging_client,
            mapper_service=self.create_totalmobile_mapper_service(),
        )

    def create_uac_service(self) -> UacServiceBase:
        return UacService(config=self._config)

    def create_cloud_task_service(self) -> CloudTaskService:
        return CloudTaskService(
            config=self._config,
            task_queue_id=self._config.create_totalmobile_jobs_task_queue_id,
        )

    def create_totalmobile_jobs_service(
        self, survey_type: str
    ) -> CreateTotalmobileJobsService:
        return CreateTotalmobileJobsService(
            totalmobile_service=self.create_totalmobile_service(),
            questionnaire_service=self.create_questionnaire_service(survey_type),
            cloud_task_service=self.create_cloud_task_service(),
        )

    def create_blaise_outcome_service(self) -> BlaiseCaseOutcomeService:
        return BlaiseCaseOutcomeService(blaise_service=self.create_blaise_service())
