import os

from dataclasses import dataclass


@dataclass
class Config:
    totalmobile_url: str
    totalmobile_instance: str
    totalmobile_client_id: str
    totalmobile_client_secret: str

    @classmethod
    def from_env(cls):
        return cls(
            totalmobile_url = os.environ.get("TOTALMOBILE_URL"),
            totalmobile_instance = os.environ.get("TOTALMOBILE_INSTANCE"),
            totalmobile_client_id = os.environ.get("TOTALMOBILE_CLIENT_ID"),
            totalmobile_client_secret = os.environ.get("TOTALMOBILE_CLIENT_SECRET"),
        )

    def log(self):
        print(f"Configuration - totalmobile_url: {self.totalmobile_url}")
        print(f"Configuration - totalmobile_instance: {self.totalmobile_instance}")
        print(f"Configuration - totalmobile_client_id: {self.totalmobile_client_id}")
        print(f"Configuration - totalmobile_client_secret: {self.totalmobile_client_secret}")
