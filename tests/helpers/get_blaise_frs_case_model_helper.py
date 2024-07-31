from datetime import datetime
from typing import Optional

from models.blaise.blaise_case_information_model import (
    Address,
    AddressCoordinates,
    AddressDetails,
)
from models.blaise.blaise_frs_case_information_model import BlaiseFRSCaseInformationModel


def get_frs_populated_case_model(
    questionnaire_name: str = "FRS2101",
    tla: str = "FRS",
    case_id: str = "910000",
    data_model_name: str = "FRS2101",
    wave: int = 1,
    address_line_1: str = "12 Blaise Street",
    address_line_2: str = "Blaise Hill",
    address_line_3: str = "Blaiseville",
    county: str = "Gwent",
    town: str = "Newport",
    postcode: str = "FML134D",
    latitude: str = "10020202",
    longitude: str = "34949494",
    reference: str = "100012675377",
    priority: str = "1",
    field_case: str = "Y",
    field_region: str = "Region 1",
    field_team: str = "B-Team",
    wave_com_dte: Optional[datetime] = None,
):
    return BlaiseFRSCaseInformationModel(
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
        priority=priority,
        field_case=field_case,
        field_region=field_region,
        field_team=field_team,
        wave_com_dte=wave_com_dte,
    )
