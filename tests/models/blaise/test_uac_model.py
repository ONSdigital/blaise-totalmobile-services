from models.blaise.uac_model import UacModel


def test_import_case_data_returns_a_populated_model():
    uac_data_dictionary = {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8175",
                "uac2": "4725",
                "uac3": "3990"
            },
            "full_uac": "817647263991"
        }

    result = UacModel.import_uac_data(uac_data_dictionary)

    assert result.case_id == "10010"
    assert result.uac_chunks.uac1 == "8175"
    assert result.uac_chunks.uac2 == "4725"
    assert result.uac_chunks.uac3 == "3990"

