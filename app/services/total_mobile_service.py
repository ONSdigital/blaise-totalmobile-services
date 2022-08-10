from appconfig.config import Config
from services import questionnaire_service

def update_case_telephone_number(
    questionnaire_name: str, case_id: str, telephone_number: str
) -> None:
    print(f"Updating telephone number for {questionnaire_name}, {case_id}, please wait...")
    config = Config.from_env()
    questionnaire_service.update_case_field(questionnaire_name, case_id, "qDataBag.TelNo", telephone_number, config)


def do_something_service(reference: str) -> None:
    print(f"The reference number is: {reference}")
    print("There are no solid requirements for this feature. You shall not pass!")
