import blaise_restapi

from dotenv import dotenv_values

config = dotenv_values(".env")
blaise_api_url = config["BLAISE_API_URL"]
server_park = config["BLAISE_SERVER_PARK"]
if blaise_api_url is None or server_park is None:
    print("Environment variable missing")
    exit(1)
restapi_client = blaise_restapi.Client(blaise_api_url)


def update_case_telephone_number(instrument_name, case_id, telephone_number):
    data_fields = {"qDataBag.TelNo": telephone_number}
    if restapi_client.patch_case_data(server_park, instrument_name, case_id, data_fields) is None:
        return 200


def do_something_service(reference):
    print(f"The reference number is: {reference}")
    print("There are no solid requirements for this feature. You shall not pass!")
