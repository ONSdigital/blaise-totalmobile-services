from datetime import datetime
from typing import Optional

from models.blaise.blaise_case_information_base_model import (
    Address,
    AddressCoordinates,
    AddressDetails,
)
from models.blaise.blaise_lms_case_information_model import (
    BlaiseLMSCaseInformationModel,
    ContactDetails,
)


def get_populated_case_model(
    questionnaire_name: str = "LMS2101_AA1",
    tla: str = "LMS",
    case_id: str = "90000",
    data_model_name: str = "LM2007",
    wave: int = 1,
    address_line_1: str = "12 Blaise Street",
    address_line_2: str = "Blaise Hill",
    address_line_3: str = "Blaiseville",
    county: str = "Gwent",
    town: str = "Newport",
    postcode: str = "FML134D",
    telephone_number_1: str = "07900990901",
    telephone_number_2: str = "07900990902",
    appointment_telephone_number: str = "07900990903",
    outcome_code: int = 301,
    latitude: str = "10020202",
    longitude: str = "34949494",
    reference: str = "100012675377",
    priority: str = "1",
    field_case: str = "Y",
    field_region: str = "Region 1",
    field_team: str = "B-Team",
    wave_com_dte: Optional[datetime] = datetime(2023, 1, 31),
    rotational_knock_to_nudge_indicator: str = "Y",
    rotational_outcome_code: int = 310,
):
    return BlaiseLMSCaseInformationModel(
        questionnaire_name=questionnaire_name,
        tla=tla,
        case_id=case_id,
        data_model_name=data_model_name,
        wave=wave,
        address_details=AddressDetails(
            reference=reference,
            address=Address(
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                address_line_3=address_line_3,
                county=county,
                town=town,
                postcode=postcode,
                coordinates=AddressCoordinates(
                    latitude=latitude,
                    longitude=longitude,
                ),
            ),
        ),
        contact_details=ContactDetails(
            telephone_number_1=telephone_number_1,
            telephone_number_2=telephone_number_2,
            appointment_telephone_number=appointment_telephone_number,
        ),
        outcome_code=outcome_code,
        priority=priority,
        field_case=field_case,
        field_region=field_region,
        field_team=field_team,
        wave_com_dte=wave_com_dte,
        rotational_knock_to_nudge_indicator=rotational_knock_to_nudge_indicator,
        rotational_outcome_code=rotational_outcome_code,
        has_call_history=False,
        divided_address_indicator=None  #TODO
    )
