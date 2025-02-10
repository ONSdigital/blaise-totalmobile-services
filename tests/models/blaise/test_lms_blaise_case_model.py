from datetime import datetime

import pytest

from enums.blaise_fields import BlaiseFields
from models.common.blaise.lms_blaise_case_model import LMSBlaiseCaseModel


class TestLMSBlaiseCaseModel:
    @pytest.fixture
    def sample_lms_case_data(self):
        # arrange
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
            BlaiseFields.telephone_number_2: "07878878787",
            BlaiseFields.appointment_telephone_number: "09876543210",
            BlaiseFields.field_case: "FIELD123",
            BlaiseFields.field_region: "Region 1",
            BlaiseFields.field_team: "TeamA",
            BlaiseFields.rotational_knock_to_nudge_indicator: "1",
            BlaiseFields.data_model_name: "LM2007",
            BlaiseFields.local_auth: "Loco",
        }

    class MockLMSBlaiseCaseModelBase(LMSBlaiseCaseModel):
        @staticmethod
        def required_fields():
            # arrange
            return ["case_id", "outcome_code", "call_history"]

    @pytest.fixture
    def model(self, sample_lms_case_data):
        # act
        return self.MockLMSBlaiseCaseModelBase("LMS2101_AA1", sample_lms_case_data)

    def test_lms_blaise_case_model_questionnaire_name_returns_expected_value(
        self, model
    ):
        assert model.questionnaire_name == "LMS2101_AA1"

    def test_lms_blaise_case_model_tla_returns_expected_value(self, model):
        assert model.tla == "LMS"

    def test_lms_blaise_case_model_case_id_returns_expected_value(self, model):
        assert model.case_id == "10010"

    def test_lms_blaise_case_model_outcome_code_returns_expected_value(self, model):
        assert model.outcome_code == 301

    def test_lms_blaise_case_model_wave_com_dte_returns_expected_value(self, model):
        assert model.wave_com_dte == datetime(2023, 1, 31)

    def test_lms_blaise_case_model_address_line_1_returns_expected_value(self, model):
        assert model.address_line_1 == "12 Blaise Street"

    def test_lms_blaise_case_model_address_line_2_returns_expected_value(self, model):
        assert model.address_line_2 == "Blaise Hill"

    def test_lms_blaise_case_model_address_line_3_returns_expected_value(self, model):
        assert model.address_line_3 == "Blaiseville"

    def test_lms_blaise_case_model_county_returns_expected_value(self, model):
        assert model.county == "Countyshire"

    def test_lms_blaise_case_model_town_returns_expected_value(self, model):
        assert model.town == "Townsville"

    def test_lms_blaise_case_model_postcode_returns_expected_value(self, model):
        assert model.postcode == "cf99rsd"

    def test_lms_blaise_case_model_reference_returns_expected_value(self, model):
        assert model.reference == "reference"

    def test_lms_blaise_case_model_latitude_returns_expected_value(self, model):
        assert model.latitude == "10020202"

    def test_lms_blaise_case_model_longitude_returns_expected_value(self, model):
        assert model.longitude == "34949494"

    def test_lms_blaise_case_model_field_region_returns_expected_value(self, model):
        assert model.field_region == "Region 1"

    def test_lms_blaise_case_model_field_team_returns_expected_value(self, model):
        assert model.field_team == "TeamA"

    def test_lms_blaise_case_model_local_auth_returns_expected_value(self, model):
        assert model.local_auth == "Loco"

    def test_lms_blaise_case_model_rotational_outcome_code_returns_expected_value(
        self, model
    ):
        assert model.rotational_outcome_code == 300

    def test_lms_blaise_case_model_has_call_history_returns_expected_value(self, model):
        assert model.has_call_history is True

    def test_lms_blaise_case_model_priority_returns_expected_value(self, model):
        assert model.priority == "High"

    def test_lms_blaise_case_model_wave_returns_expected_value(self, model):
        assert model.wave == 2

    def test_lms_blaise_case_model_telephone_number_1_returns_expected_value(
        self, model
    ):
        assert model.telephone_number_1 == "01234567890"

    def test_lms_blaise_case_model_telephone_number_2_returns_expected_value(
        self, model
    ):
        assert model.telephone_number_2 == "07878878787"

    def test_lms_blaise_case_model_appointment_telephone_number_returns_expected_value(
        self, model
    ):
        assert model.appointment_telephone_number == "09876543210"

    def test_lms_blaise_case_model_field_case_returns_expected_value(self, model):
        assert model.field_case == "FIELD123"

    def test_lms_blaise_case_model_rotational_knock_to_nudge_indicator_returns_expected_value(
        self, model
    ):
        assert model.rotational_knock_to_nudge_indicator == "Y"

    def test_lms_blaise_case_model_data_model_name_returns_expected_value(self, model):
        assert model.data_model_name == "LM2007"

    def test_lms_blaise_case_model_empty_wave_com_dte_returns_none_returns_expected_value(
        self, sample_lms_case_data
    ):
        sample_lms_case_data[BlaiseFields.wave_com_dte] = ""
        model = self.MockLMSBlaiseCaseModelBase("LMS123", sample_lms_case_data)
        assert model.wave_com_dte is None

    def test_lms_blaise_case_model_convert_indicator_to_y_n_or_empty_returns_expected_value(
        self,
    ):
        assert LMSBlaiseCaseModel.convert_indicator_to_y_n_or_empty("1") == "Y"
        assert LMSBlaiseCaseModel.convert_indicator_to_y_n_or_empty("0") == "N"
        assert LMSBlaiseCaseModel.convert_indicator_to_y_n_or_empty("") == ""

    def test_lms_blaise_case_model_convert_string_to_integer_returns_expected_value(
        self,
    ):
        assert LMSBlaiseCaseModel.convert_string_to_integer("10") == 10
        assert LMSBlaiseCaseModel.convert_string_to_integer("") == 0

    def test_lms_blaise_case_model_string_to_bool_returns_expected_value(self):
        assert LMSBlaiseCaseModel.string_to_bool("1") is True
        assert LMSBlaiseCaseModel.string_to_bool("") is False
        assert LMSBlaiseCaseModel.string_to_bool(None) is False
