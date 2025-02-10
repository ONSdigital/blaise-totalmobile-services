from datetime import datetime

import pytest

from enums.blaise_fields import BlaiseFields
from models.common.blaise.blaise_case_model import BlaiseCaseModel


class TestBlaiseCaseModel:
    @pytest.fixture
    def sample_lms_case_data(self):
        return {
            BlaiseFields.case_id: "10010",
            BlaiseFields.outcome_code: "301",
            BlaiseFields.rotational_outcome_code: "300",
            BlaiseFields.call_history: "1",
            BlaiseFields.priority: "High",
            BlaiseFields.wave: "2",
            BlaiseFields.wave_com_dte: "31-01-2023",
            BlaiseFields.address_line_1: "12 Blaise Street",
            BlaiseFields.address_line_2: "Blaise Hill",
            BlaiseFields.address_line_3: "Blaiseville",
            BlaiseFields.county: "Countyshire",
            BlaiseFields.town: "Townsville",
            BlaiseFields.postcode: "cf99rsd",
            BlaiseFields.reference: "reference",
            BlaiseFields.latitude: "10020202",
            BlaiseFields.longitude: "34949494",
            BlaiseFields.telephone_number_1: "01234567890",
            BlaiseFields.telephone_number_2: "",
            BlaiseFields.appointment_telephone_number: "09876543210",
            BlaiseFields.field_case: "FIELD123",
            BlaiseFields.field_region: "Region 1",
            BlaiseFields.field_team: "TeamA",
            BlaiseFields.rotational_knock_to_nudge_indicator: "1",
            BlaiseFields.data_model_name: "LM2007",
            BlaiseFields.local_auth: "Loco",
        }

    class MockLMSBlaiseCaseModel(BlaiseCaseModel):
        @staticmethod
        def required_fields():
            return ["case_id", "outcome_code", "call_history"]

    @pytest.fixture
    def model(self, sample_lms_case_data):
        return self.MockLMSBlaiseCaseModel("LMS123", sample_lms_case_data)

    def test_questionnaire_name(self, model):
        assert model.questionnaire_name == "LMS123"

    def test_tla(self, model):
        assert model.tla == "LMS"

    def test_case_id(self, model):
        assert model.case_id == "10010"

    def test_outcome_code_conversion(self, model):
        assert model.outcome_code == 301

    def test_rotational_outcome_code_conversion(self, model):
        assert model.rotational_outcome_code == 300

    def test_has_call_history(self, model):
        assert model.has_call_history is True

    def test_priority(self, model):
        assert model.priority == "High"

    def test_wave_conversion(self, model):
        assert model.wave == 2

    def test_wave_com_dte_conversion(self, model):
        assert model.wave_com_dte == datetime(2023, 1, 31)

    def test_empty_wave_com_dte_returns_none(self, sample_lms_case_data):
        sample_lms_case_data[BlaiseFields.wave_com_dte] = ""
        model = self.MockLMSBlaiseCaseModel("LMS123", sample_lms_case_data)
        assert model.wave_com_dte is None

    def test_convert_indicator_to_y_n_or_empty(self):
        assert BlaiseCaseModel.convert_indicator_to_y_n_or_empty("1") == "Y"
        assert BlaiseCaseModel.convert_indicator_to_y_n_or_empty("0") == "N"
        assert BlaiseCaseModel.convert_indicator_to_y_n_or_empty("") == ""

    def test_convert_string_to_integer(self):
        assert BlaiseCaseModel.convert_string_to_integer("10") == 10
        assert BlaiseCaseModel.convert_string_to_integer("") == 0

    def test_string_to_bool(self):
        assert BlaiseCaseModel.string_to_bool("1") is True
        assert BlaiseCaseModel.string_to_bool("") is False
        assert BlaiseCaseModel.string_to_bool(None) is False
