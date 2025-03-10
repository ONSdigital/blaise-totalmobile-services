from typing import Dict

from client.bus import Uac
from models.create.blaise.questionnaire_uac_model import QuestionnaireUacModel


def test_import_case_data_returns_a_populated_model():
    # arrange
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8175",
                "uac2": "4725",
                "uac3": "3990",
                "uac4": "None",
            },
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {
                "uac1": "4175",
                "uac2": "5725",
                "uac3": "6990",
                "uac4": "None",
            },
            "full_uac": "417657266991",
        },
    }

    # act
    result = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    # assert
    assert len(result.questionnaire_case_uacs) == 2

    assert result.questionnaire_case_uacs["10010"].uac1 == "8175"
    assert result.questionnaire_case_uacs["10010"].uac2 == "4725"
    assert result.questionnaire_case_uacs["10010"].uac3 == "3990"

    assert result.questionnaire_case_uacs["10020"].uac1 == "4175"
    assert result.questionnaire_case_uacs["10020"].uac2 == "5725"
    assert result.questionnaire_case_uacs["10020"].uac3 == "6990"


def test_get_uac_chunks_returns_the_corect_uac():
    # arrange
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8175",
                "uac2": "4725",
                "uac3": "3990",
                "uac4": "None",
            },
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {
                "uac1": "4175",
                "uac2": "5725",
                "uac3": "6990",
                "uac4": "None",
            },
            "full_uac": "417657266991",
        },
    }

    questionnaire_model = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    # act
    result = questionnaire_model.get_uac_chunks("10010")

    # assert
    assert result.uac1 == "8175"
    assert result.uac2 == "4725"
    assert result.uac3 == "3990"


def test_get_uac_chunks_returns_none_if_case_not_in_dictionary():
    # arrange
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8175",
                "uac2": "4725",
                "uac3": "3990",
                "uac4": "None",
            },
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {
                "uac1": "4175",
                "uac2": "5725",
                "uac3": "6990",
                "uac4": "None",
            },
            "full_uac": "417657266991",
        },
    }

    questionnaire_model = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    # act
    result = questionnaire_model.get_uac_chunks("10030")

    # assert
    assert result is None


def test_get_uac_chunks_returns_none_if_case_id_not_supplied():
    # arrange
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8175",
                "uac2": "4725",
                "uac3": "3990",
                "uac4": "None",
            },
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {
                "uac1": "4175",
                "uac2": "5725",
                "uac3": "6990",
                "uac4": "None",
            },
            "full_uac": "417657266991",
        },
    }

    questionnaire_model = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    # act
    result = questionnaire_model.get_uac_chunks(None)

    # assert
    assert result is None


def test_import_case_data_returns_a_correctly_populated_model_when_three_uac_chunks_are_provided():
    # arrange
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "1234",
                "uac2": "4567",
                "uac3": "7890",
                "uac4": "None",
            },
            "full_uac": "123445677890",
        }
    }

    # act
    result = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    # assert
    assert len(result.questionnaire_case_uacs) == 1

    assert result.questionnaire_case_uacs["10010"].uac1 == "1234"
    assert result.questionnaire_case_uacs["10010"].uac2 == "4567"
    assert result.questionnaire_case_uacs["10010"].uac3 == "7890"


def test_import_case_data_returns_a_correctly_populated_model_when_four_uac_chunks_are_provided():
    # arrange
    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "1234",
                "uac2": "4567",
                "uac3": "7890",
                "uac4": "0987",
            },
            "full_uac": "1234456778900987",
        }
    }

    # act
    result = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    # assert
    assert len(result.questionnaire_case_uacs) == 1

    assert result.questionnaire_case_uacs["10010"].uac1 == "1234"
    assert result.questionnaire_case_uacs["10010"].uac2 == "4567"
    assert result.questionnaire_case_uacs["10010"].uac3 == "7890"
    assert result.questionnaire_case_uacs["10010"].uac4 == "0987"
