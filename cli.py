from dotenv import dotenv_values
from bus import BusClient

from optimise import OptimiseClient
import blaise_restapi
import json

config = dotenv_values(".env")

totalmobile_url = config["TOTALMOBILE_URL"]
totalmobile_instance = config["TOTALMOBILE_INSTANCE"]
totalmobile_client_id = config["TOTALMOBILE_CLIENT_ID"]
totalmobile_client_secret = config["TOTALMOBILE_CLIENT_SECRET"]
blaise_api_url = config["BLAISE_API_URL"]
blaise_server_park = config["BLAISE_SERVER_PARK"]
bus_url = config["BUS_URL"]
bus_client_id = config["BUS_CLIENT_ID"]
instrument = config["INSTRUMENT_NAME"]

if (
    totalmobile_url is None
    or totalmobile_instance is None
    or totalmobile_client_id is None
    or totalmobile_client_secret is None
    or blaise_api_url is None
    or blaise_server_park is None
    or bus_url is None
    or bus_client_id is None
    or instrument is None
):
    print("Environment variable missing")
    exit(1)

restapi_client = blaise_restapi.Client(blaise_api_url)

bus_client = BusClient(bus_url, bus_client_id)

optimise_client = OptimiseClient(
    totalmobile_url,
    totalmobile_instance,
    totalmobile_client_id,
    totalmobile_client_secret,
)

world = "Region 1"
world_id = optimise_client.get_world(world)["id"]


# uacs = bus_client.get_uacs_by_case_id(instrument)

cases = restapi_client.get_instrument_data(
    blaise_server_park,
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

output_cases = []
for index, case in enumerate(cases["reportingData"]):
    if case["srvStat"] != "3" and case["hOut"] not in ["360", "390"]:  # tla !?
        output_case = {"instrument": instrument, "case": case, "world_id": world_id}
        output_cases.append(output_case)
    if index >= 100:
        break
# uac_info = uacs[case["qiD.Serial_Number"]]
# optimise_client.create_job(
#     world_id,
#     {
#         "identity": {
#             "reference": f"{instrument[:3]}{case['qiD.Serial_Number']}"
#         },
#         "origin": "ONS",
#         "clientReference": "2",  # num of no contacts allowed
#         "duration": 30,
#         "description": "test-job",
#         "workType": "KTN",
#         "skills": [{"identity": {"reference": "KTN"}}],
#         "dueDate": {
#             "start": "",  # !?
#             "end": "",  # !?
#         },
#         "location": {
#             "address": f"{case['qDataBag.Prem1']}, {case['qDataBag.Prem2']}, {case['qDataBag.PostTown']}",
#             "reference": case["qiD.Serial_Number"],
#             "addressDetail": {
#                 "name": f"{case['qDataBag.Prem1']}, {case['qDataBag.Prem2']}, {case['qDataBag.PostTown']}",
#                 "addressLine2": case["qDataBag.Prem1"],
#                 "addressLine3": case["qDataBag.Prem2"],
#                 "addressLine4": case["qDataBag.PostTown"],
#                 "postCode": case["qDataBag.PostCode"],
#                 "coordinates": {
#                     "latitude": case["qDataBag.UPRN_Latitude"],
#                     "longitude": case["qDataBag.UPRN_Longitude"],
#                 },
#             },
#         },
#         "contact": {
#             "name": case["qDataBag.PostCode"],
#             "homePhone": case["qDataBag.TelNo"],
#             "mobilePhone": case["qDataBag.TelNo2"],
#             "contactDetail": {
#                 "contactId": instrument[:3],  # survey tla
#                 "contactIdLabel": instrument[-1],  # wave - lms specific!
#                 "preferredName": instrument[4:7],  # 3 digit field period..!?
#             },
#         },
#         "attributes": [
#             {"name": "UAC1", "value": uac_info["uac_chunks"]["uac1"]},
#             {"name": "UAC2", "value": uac_info["uac_chunks"]["uac2"]},
#             {"name": "UAC3", "value": uac_info["uac_chunks"]["uac3"]},
#             {"name": "study", "value": instrument},
#             {"name": "case_id", "value": case["qiD.Serial_Number"]},
#         ],
#     },
# )
# break  # testing
print(json.dumps(output_cases))
