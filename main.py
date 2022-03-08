from optimise import OptimiseClient
from dotenv import dotenv_values

config = dotenv_values(".env")

optimise_client = OptimiseClient(
    config["TOTALMOBILE_URL"],
    config["TOTALMOBILE_INSTANCE"],
    config["TOTALMOBILE_CLIENT_ID"],
    config["TOTALMOBILE_CLIENT_SECRET"],
)

world_id = optimise_client.get_world("Region 1")["id"]
print(world_id)
print(optimise_client.get_jobs(world_id))
