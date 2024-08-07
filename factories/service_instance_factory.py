from appconfig import Config
from client.messaging import MessagingClient
from client.optimise import OptimiseClient
from services.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.blaise_service import RealBlaiseService
from services.case_filters.case_filter_wave_1 import CaseFilterWave1
from services.case_filters.case_filter_wave_2 import CaseFilterWave2
from services.case_filters.case_filter_wave_3 import CaseFilterWave3
from services.case_filters.case_filter_wave_4 import CaseFilterWave4
from services.case_filters.case_filter_wave_5 import CaseFilterWave5
from services.cloud_task_service import CloudTaskService
from services.create_totalmobile_jobs_service import CreateTotalmobileJobsService
from services.datastore_service import DatastoreService
from services.frs_eligible_case_service import FRSEligibleCaseService
from services.lms_eligible__case_service import LMSEligibleCaseService
from services.mappers.blaise_frs_case_mapper_service import BlaiseFRSCaseMapperService
from services.mappers.blaise_lms_case_mapper_service import BlaiseLMSCaseMapperService
from services.mappers.totalmobile_mapper_service import TotalmobileMapperService
from services.questionnaires.frs_questionnaire_service import FRSQuestionnaireService
from services.questionnaires.lms_questionnaire_service import LMSQuestionnaireService
from services.totalmobile_service import RealTotalmobileService
from services.uac.uac_service import UacService


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

    @staticmethod
    def create_lms_mapper_service() -> BlaiseLMSCaseMapperService:
        return BlaiseLMSCaseMapperService()

    @staticmethod
    def create_frs_mapper_service() -> BlaiseFRSCaseMapperService:
        return BlaiseFRSCaseMapperService()

    def create_lms_questionnaire_service(self) -> LMSQuestionnaireService:
        return LMSQuestionnaireService(
            blaise_service=self.create_blaise_service(),
            mapper_service=self.create_lms_mapper_service(),
            eligible_case_service=self.create_eligible_lms_case_service(),
            datastore_service=self.create_datastore_service(),
        )

    def create_frs_questionnaire_service(self) -> FRSQuestionnaireService:
        return FRSQuestionnaireService(
            blaise_service=self.create_blaise_service(),
            mapper_service=self.create_frs_mapper_service(),
            eligible_case_service=self.create_eligible_frs_case_service(),
            datastore_service=self.create_datastore_service(),
        )

    def create_totalmobile_mapper_service(self) -> TotalmobileMapperService:
        return TotalmobileMapperService(uac_service=self.create_uac_service())

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

    def create_uac_service(self) -> UacService:
        return UacService(config=self._config)

    def create_cloud_task_service(self) -> CloudTaskService:
        return CloudTaskService(
            config=self._config,
            task_queue_id=self._config.create_totalmobile_jobs_task_queue_id,
        )

    def create_totalmobile_jobs_service(
        self, survey_type: str
    ) -> CreateTotalmobileJobsService:
        if survey_type == "LMS":
            return CreateTotalmobileJobsService(
                totalmobile_service=self.create_totalmobile_service(),
                questionnaire_service=self.create_lms_questionnaire_service(),
                cloud_task_service=self.create_cloud_task_service(),
            )

        return CreateTotalmobileJobsService(
            totalmobile_service=self.create_totalmobile_service(),
            questionnaire_service=self.create_frs_questionnaire_service(),
            cloud_task_service=self.create_cloud_task_service(),
        )

    def create_blaise_outcome_service(self) -> BlaiseCaseOutcomeService:
        return BlaiseCaseOutcomeService(blaise_service=self.create_blaise_service())
