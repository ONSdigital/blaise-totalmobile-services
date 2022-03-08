from dotenv import dotenv_values

from optimise import OptimiseClient

config = dotenv_values(".env")

url = config["TOTALMOBILE_URL"]
instance = config["TOTALMOBILE_INSTANCE"]
client_id = config["TOTALMOBILE_CLIENT_ID"]
client_secret = config["TOTALMOBILE_CLIENT_SECRET"]

if url is None or instance is None or client_id is None or client_secret is None:
    print(
        "Must set: "
        + "TOTALMOBILE_URL, TOTALMOBILE_INSTANCE, "
        + "TOTALMOBILE_CLIENT_ID, TOTALMOBILE_CLIENT_SECRET"
    )
    exit(1)

optimise_client = OptimiseClient(
    url,
    instance,
    client_id,
    client_secret,
)

world_id = optimise_client.get_world("Region 1")["id"]
print(world_id)
print(optimise_client.get_jobs(world_id))
