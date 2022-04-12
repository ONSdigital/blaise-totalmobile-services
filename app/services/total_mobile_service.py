import blaise_restapi

from appconfig import Config


def update_case_telephone_number(
    instrument_name: str, case_id: str, telephone_number: str
) -> None:
    print(f"Updating telephone number for {instrument_name}, {case_id}, please wait...")
    config = Config.from_env()
    restapi_client = blaise_restapi.Client(config.blaise_api_url)
    print(f"\nrest_api: {restapi_client}")

    data_fields = {"qDataBag.TelNo": telephone_number}
    print(f"\ndata_fields: {data_fields}")
    restapi_client.patch_case_data(
        config.blaise_server_park, instrument_name, case_id, data_fields
    )


def do_something_service(reference: str) -> None:
    print(f"The reference number is: {reference}")
    print("There are no solid requirements for this feature. You shall not pass!")
