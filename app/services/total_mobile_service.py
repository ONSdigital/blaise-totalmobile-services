import blaise_restapi

from appconfig import Config


def update_case_telephone_number(instrument_name, case_id, telephone_number):
    config = Config.from_env()
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    data_fields = {"qDataBag.TelNo": telephone_number}
    restapi_client.patch_case_data(config.blaise_server_park, instrument_name, case_id, data_fields)


def do_something_service(reference):
    print(f"The reference number is: {reference}")
    print("There are no solid requirements for this feature. You shall not pass!")
