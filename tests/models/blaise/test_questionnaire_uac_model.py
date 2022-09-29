from typing import Dict

from client.bus import Uac
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel


def test_import_case_data_returns_a_populated_model():
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {"uac1": "8175", "uac2": "4725", "uac3": "3990"},
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {"uac1": "4175", "uac2": "5725", "uac3": "6990"},
            "full_uac": "417657266991",
        },
    }

    result = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    assert len(result.questionnaire_case_uacs) == 2

    assert result.questionnaire_case_uacs["10010"].uac1 == "8175"
    assert result.questionnaire_case_uacs["10010"].uac2 == "4725"
    assert result.questionnaire_case_uacs["10010"].uac3 == "3990"

    assert result.questionnaire_case_uacs["10020"].uac1 == "4175"
    assert result.questionnaire_case_uacs["10020"].uac2 == "5725"
    assert result.questionnaire_case_uacs["10020"].uac3 == "6990"
