import os
from dataclasses import dataclass, fields


class ConfigError(Exception):
    pass


@dataclass
class Config:
    totalmobile_url: str
    totalmobile_instance: str
    totalmobile_client_id: str
    totalmobile_client_secret: str
    create_totalmobile_jobs_task_queue_id: str
    gcloud_project: str
    region: str
    blaise_api_url: str
    blaise_server_park: str
    cma_server_park: str
    cloud_function_sa: str
    bus_api_url: str
    bus_client_id: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            totalmobile_url=os.getenv("TOTALMOBILE_URL", ""),
            totalmobile_instance=os.getenv("TOTALMOBILE_INSTANCE", ""),
            totalmobile_client_id=os.getenv("TOTALMOBILE_CLIENT_ID", ""),
            totalmobile_client_secret=os.getenv("TOTALMOBILE_CLIENT_SECRET", ""),
            create_totalmobile_jobs_task_queue_id=os.getenv("CREATE_TOTALMOBILE_JOBS_TASK_QUEUE_ID", ""),
            gcloud_project=os.getenv("GCLOUD_PROJECT", ""),
            region=os.getenv("REGION", ""),
            blaise_api_url=os.getenv("BLAISE_API_URL", ""),
            blaise_server_park=os.getenv("BLAISE_SERVER_PARK", ""),
            cma_server_park=os.getenv("CMA_SERVER_PARK", ""),
            cloud_function_sa=os.getenv("CLOUD_FUNCTION_SA", ""),
            bus_api_url=os.getenv("BUS_API_URL", ""),
            bus_client_id=os.getenv("BUS_CLIENT_ID", ""),
        )

    def log(self) -> None:
        print(f"Configuration - totalmobile_url: {self.totalmobile_url}")
        print(f"Configuration - totalmobile_instance: {self.totalmobile_instance}")
        print(f"Configuration - totalmobile_client_id: {self.totalmobile_client_id}")
        if self.totalmobile_client_secret is None:
            print("Configuration - totalmobile_client_secret: None")
        else:
            print("Configuration - totalmobile_client_secret: Provided")
        print(
            f"Configuration - create_totalmobile_jobs_task_queue_id: {self.create_totalmobile_jobs_task_queue_id}"
        )
        print(f"Configuration - gcloud_project: {self.gcloud_project}")
        print(f"Configuration - region: {self.region}")
        print(f"Configuration - blaise_api_url: {self.blaise_api_url}")
        print(f"Configuration - blaise_server_park: {self.blaise_server_park}")
        print(f"Configuration - cma_server_park: {self.cma_server_park}")
        print(f"Configuration - cloud_function_sa: {self.cloud_function_sa}")
        print(f"Configuration - bus_api_url: {self.bus_api_url}")
        print(f"Configuration - bus_client_id: {self.bus_client_id}")
