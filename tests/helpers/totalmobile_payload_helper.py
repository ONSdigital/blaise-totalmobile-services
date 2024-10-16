from typing import Dict, Optional

from models.create.blaise.blaise_frs_create_case_model import BlaiseFRSCreateCaseModel
from models.create.blaise.blaise_lms_create_case_model import BlaiseLMSCreateCaseModel
from models.create.blaise.questionnaire_uac_model import UacChunks


def lms_totalmobile_payload_helper(
    questionnaire_name: str,
    case: BlaiseLMSCreateCaseModel,
    uac_chunks: Optional[UacChunks],
) -> dict[str, object]:

    payload_dictionary = {
        "additionalProperties": [
            {"name": "surveyName", "value": case.data_model_name},
            {"name": "tla", "value": case.tla},
            {"name": "wave", "value": f"{case.wave}"},
            {"name": "priority", "value": case.priority},
            {"name": "fieldRegion", "value": case.field_region},
            {"name": "fieldTeam", "value": case.field_team},
            {"name": "postCode", "value": case.postcode},
        ],
        "attributes": [
            {"name": "Region", "value": case.field_region},
            {"name": "Team", "value": case.field_team},
        ],
        "contact": {"name": case.postcode},
        "description": f'UAC: {uac_chunks.formatted_chunks() if uac_chunks is not None else ""}\n'
        f'Due Date: {case.wave_com_dte.strftime("%d/%m/%Y") if case.wave_com_dte is not None else ""}\n'
        f"Study: {questionnaire_name}\n"
        f"Case ID: {case.case_id}\n"
        f"Wave: {case.wave}",
        "dueDate": {
            "end": case.wave_com_dte.strftime("%Y-%m-%d")
            if case.wave_com_dte is not None
            else ""
        },
        "duration": 15,
        "identity": {
            "reference": f'{questionnaire_name.replace("_", "-")}.{case.case_id}'
        },
        "location": {
            "address": "12 Blaise Street, Blaise Hill, Blaiseville, Newport, "
            f"{case.postcode}",
            "addressDetail": {
                "addressLine1": "12 Blaise Street, Blaise Hill",
                "addressLine2": "Blaiseville",
                "addressLine3": "Gwent",
                "addressLine4": "Newport",
                "coordinates": {"latitude": "10020202", "longitude": "34949494"},
                "postCode": case.postcode,
            },
            "reference": case.reference,
        },
        "origin": "ONS",
        "skills": [{"identity": {"reference": case.tla}}],
        "workType": case.tla,
    }

    if uac_chunks is not None:
        payload_dictionary["additionalProperties"].append({"name": "uac1", "value": uac_chunks.uac1})  # type: ignore
        payload_dictionary["additionalProperties"].append({"name": "uac2", "value": uac_chunks.uac2})  # type: ignore
        payload_dictionary["additionalProperties"].append({"name": "uac3", "value": uac_chunks.uac3})  # type: ignore

    return payload_dictionary


def frs_totalmobile_payload_helper(
    questionnaire_name: str, case: BlaiseFRSCreateCaseModel
) -> Dict[str, object]:
    due_date = (
        case.wave_com_dte.strftime("%d/%m/%Y") if case.wave_com_dte is not None else ""
    )

    payload_dictionary = {
        "additionalProperties": [
            {"name": "tla", "value": case.tla},
            {"name": "rand", "value": case.rand},
            {"name": "fieldRegion", "value": case.field_region},
            {"name": "fieldTeam", "value": case.field_team},
            {"name": "postCode", "value": case.postcode},
        ],
        "attributes": [],
        "contact": {"name": case.postcode},
        "description": (
            "Warning Divided Address" if case.divided_address_indicator == "1" else ""
        ),
        "dueDate": {"end": due_date},
        "duration": 15,
        "identity": {
            "reference": f'{questionnaire_name.replace("_", "-")}.{case.case_id}'
        },
        "location": {
            "address": "12 Blaise Street, Blaise Hill, Blaiseville, Newport, "
            f"{case.postcode}",
            "addressDetail": {
                "addressLine1": "12 Blaise Street, Blaise Hill",
                "addressLine2": "Blaiseville",
                "addressLine3": "Gwent",
                "addressLine4": "Newport",
                "coordinates": {"latitude": "10020202", "longitude": "34949494"},
                "postCode": f"{case.postcode}",
            },
            "reference": case.reference,
        },
        "origin": "",
        "skills": [{"identity": {"reference": case.tla}}],
        "workType": case.tla,
    }

    return payload_dictionary
