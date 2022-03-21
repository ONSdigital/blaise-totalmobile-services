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

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            totalmobile_url=os.getenv("TOTALMOBILE_URL", ""),
            totalmobile_instance=os.getenv("TOTALMOBILE_INSTANCE", ""),
            totalmobile_client_id=os.getenv("TOTALMOBILE_CLIENT_ID", ""),
            totalmobile_client_secret=os.getenv("TOTALMOBILE_CLIENT_SECRET", ""),
        )

    def log(self) -> None:
        print(f"Configuration - totalmobile_url: {self.totalmobile_url}")
        print(f"Configuration - totalmobile_instance: {self.totalmobile_instance}")
        print(f"Configuration - totalmobile_client_id: {self.totalmobile_client_id}")
        print(
            f"Configuration - totalmobile_client_secret: {self.totalmobile_client_secret}"
        )

    def validate(self) -> None:
        errored_fields = []
        for field in fields(self):
            if getattr(self, field.name) == "":
                errored_fields.append(field.name)
        if len(errored_fields) > 0:
            raise ConfigError(f"Config fields not set: {errored_fields}")
