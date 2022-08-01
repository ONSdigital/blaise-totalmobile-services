from models.questionnaire_case_model import CaseModel

def test_case_model_returns_a_json():
    mock_blaise_data = '{"qiD.Serial_Number": "90000000"}'

    result = CaseModel.from_json(mock_blaise_data)
    assert result.serial_number == "90000000"


def test_case_model_returns_a_valid_object_when_blaise_field_is_missing():
    mock_blaise_data = '{"Serial_Number": "90000000"}'

    result = CaseModel.from_json(mock_blaise_data)
    assert result.serial_number == ""