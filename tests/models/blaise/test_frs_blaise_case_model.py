from datetime import datetime

import pytest

from enums.blaise_fields import BlaiseFields
from models.common.blaise.frs_blaise_case_model import FRSBlaiseCaseModel


class TestFRSBlaiseCaseModel:
    @pytest.fixture
    def sample_frs_case_data(self):
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

    class MockFRSBlaiseCaseModelBase(FRSBlaiseCaseModel):
        @staticmethod
        def required_fields():
            # arrange
            return ["case_id", "outcome_code"]

    @pytest.fixture
    def model(self, sample_frs_case_data):
        # act
        return self.MockFRSBlaiseCaseModelBase("FRS2101", sample_frs_case_data)

    def test_frs_blaise_case_model_questionnaire_name_returns_expected_value(
        self, model
    ):
        assert model.questionnaire_name == "FRS2101"

    def test_frs_blaise_case_model_tla_returns_expected_value(self, model):
        assert model.tla == "FRS"

    def test_frs_blaise_case_model_case_id_returns_expected_value(self, model):
        assert model.case_id == "10010"

    def test_frs_blaise_case_model_outcome_code_returns_expected_value(self, model):
        assert model.outcome_code == 301

    def test_frs_blaise_case_model_wave_com_dte_returns_expected_value(self, model):
        assert model.wave_com_dte == datetime(2023, 1, 31)

    def test_frs_blaise_case_model_address_line_1_returns_expected_value(self, model):
        assert model.address_line_1 == "12 Blaise Street"

    def test_frs_blaise_case_model_address_line_2_returns_expected_value(self, model):
        assert model.address_line_2 == "Blaise Hill"

    def test_frs_blaise_case_model_address_line_3_returns_expected_value(self, model):
        assert model.address_line_3 == "Blaiseville"

    def test_frs_blaise_case_model_county_returns_expected_value(self, model):
        assert model.county == "Countyshire"

    def test_frs_blaise_case_model_town_returns_expected_value(self, model):
        assert model.town == "Townsville"

    def test_frs_blaise_case_model_postcode_returns_expected_value(self, model):
        assert model.postcode == "cf99rsd"

    def test_frs_blaise_case_model_reference_returns_expected_value(self, model):
        assert model.reference == "reference"

    def test_frs_blaise_case_model_latitude_returns_expected_value(self, model):
        assert model.latitude == "10020202"

    def test_frs_blaise_case_model_longitude_returns_expected_value(self, model):
        assert model.longitude == "34949494"

    def test_frs_blaise_case_model_field_region_returns_expected_value(self, model):
        assert model.field_region == "Region 1"

    def test_frs_blaise_case_model_field_team_returns_expected_value(self, model):
        assert model.field_team == "TeamA"

    def test_frs_blaise_case_model_local_auth_returns_expected_value(self, model):
        assert model.local_auth == "Loco"

    def test_frs_blaise_case_model_empty_wave_com_dte_returns_none_returns_expected_value(
        self, sample_frs_case_data
    ):
        sample_frs_case_data[BlaiseFields.wave_com_dte] = ""
        model = self.MockFRSBlaiseCaseModelBase("FRS123", sample_frs_case_data)
        assert model.wave_com_dte is None

    def test_frs_blaise_case_model_convert_string_to_integer_returns_expected_value(
        self,
    ):
        assert FRSBlaiseCaseModel.convert_string_to_integer("10") == 10
        assert FRSBlaiseCaseModel.convert_string_to_integer("") == 0

    def test_frs_blaise_case_model_does_not_return_any_lms_properties(self, model):
        assert hasattr(model, "case_data")  # Expected FRS property
        assert not hasattr(model, "has_call_history")  # LMS property not expected here
