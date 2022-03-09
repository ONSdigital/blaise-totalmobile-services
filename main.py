from uuid import uuid4
from dotenv import dotenv_values
from bus import BusClient

from optimise import OptimiseClient
import blaise_restapi

config = dotenv_values(".env")

url = config["TOTALMOBILE_URL"]
instance = config["TOTALMOBILE_INSTANCE"]
client_id = config["TOTALMOBILE_CLIENT_ID"]
client_secret = config["TOTALMOBILE_CLIENT_SECRET"]
bus_url = config["BUS_URL"]
bus_client_id = config["BUS_CLIENT_ID"]
instrument = config["INSTRUMENT_NAME"]

if (
    url is None
    or instance is None
    or client_id is None
    or client_secret is None
    or bus_url is None
    or bus_client_id is None
    or instrument is None
):
    print(
        "Must set: "
        + "TOTALMOBILE_URL, TOTALMOBILE_INSTANCE, "
        + "TOTALMOBILE_CLIENT_ID, TOTALMOBILE_CLIENT_SECRET, "
        + "BUS_URL, BUS_CLIENT_ID, INSTRUMENT_NAME"
    )
    exit(1)

optimise_client = OptimiseClient(
    url,
    instance,
    client_id,
    client_secret,
)

world = "Region 1"

world_id = optimise_client.get_world(world)["id"]
print(world_id)
# print(optimise_client.get_resources())
# print("TOTAL")
# print(len(optimise_client.get_jobs(world_id)))
# for _ in range(357):
#     optimise_client.create_job(
#         world_id,
#         {
#             "identity": {"reference": str(uuid4())},
#             "duration": 10,
#             "description": "test-job",
#             "skills": [{"identity": {"reference": "interviewer"}}],
#         },
#     )
# print(optimise_client.get_dispatch())

restapi_client = blaise_restapi.Client("http://localhost:8081")

bus_client = BusClient(bus_url, bus_client_id)
uacs = bus_client.get_uacs_by_case_id(instrument)

cases = restapi_client.get_instrument_data(
    "gusty",
    instrument,
    [
        "qDataBag.UPRN_Latitude",
        "qDataBag.UPRN_Longitude",
        "qDataBag.Prem1",
        "qDataBag.Prem2",
        "qDataBag.Prem3",
        "qDataBag.PostTown",
        "qDataBag.PostCode",
        "qDataBag.TelNo",
        "qDataBag.TelNo2",
        "hOut",
        "srvStat",
        "qiD.Serial_Number",
    ],
)

for case in cases["reportingData"]:
    if case["srvStat"] != "3" and case["hOut"] not in ["360", "390"]:
        uac_info = uacs[case["qiD.Serial_Number"]]
        optimise_client.create_job(
            world_id,
            {
                "identity": {
                    "reference": f"{world}-{instrument.replace('_', '-')}-{case['qiD.Serial_Number']}"
                },
                "duration": 10,
                "description": "test-job",
                "skills": [{"identity": {"reference": "interviewer"}}],
                "location": {
                    "address": f"{case['qDataBag.Prem1']}, {case['qDataBag.Prem2']}, {case['qDataBag.Prem3']}, {case['qDataBag.PostTown']}, {case['qDataBag.PostCode']}",
                    "addressDetail": {
                        "addressLine1": case["qDataBag.Prem1"],
                        "addressLine2": case["qDataBag.Prem2"],
                        "addressLine3": case["qDataBag.Prem3"],
                        "addressLine4": case["qDataBag.PostTown"],
                        "postCode": case["qDataBag.PostCode"],
                        "coordinates": {
                            "latitude": case["qDataBag.UPRN_Latitude"],
                            "longitude": case["qDataBag.UPRN_Longitude"],
                        },
                    },
                },
                "contact": {
                    "homePhone": case["qDataBag.TelNo"],
                    "mobilePhone": case["qDataBag.TelNo2"],
                },
                "attributes": [
                    {"name": "UAC1", "value": uac_info["uac_chunks"]["uac1"]},
                    {"name": "UAC2", "value": uac_info["uac_chunks"]["uac2"]},
                    {"name": "UAC3", "value": uac_info["uac_chunks"]["uac3"]},
                    {"name": "study", "value": instrument},
                    {"name": "case_id", "value": case["qiD.Serial_Number"]},
                ],
            },
        )
