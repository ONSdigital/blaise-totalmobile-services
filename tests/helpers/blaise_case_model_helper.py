from typing import Optional

from enums.blaise_fields import BlaiseFields
from models.create.blaise.blaise_frs_create_case_model import BlaiseFRSCreateCaseModel
from models.create.blaise.blaise_lms_create_case_model import BlaiseLMSCreateCaseModel
from models.create.blaise.questionnaire_uac_model import UacChunks


class BlaiseCaseModelHelper:
    @staticmethod
    def get_populated_frs_create_case_model(
        questionnaire_name: str = "FRS2101",
        case_id: str = "10010",
        latitude: str = "10020202",
        longitude: str = "34949494",
        address_line1: str = "12 Blaise Street",
        address_line2: str = "Blaise Hill",
        address_line3: str = "Blaiseville",
        town: str = "Newport",
        postcode: str = "cf99rsd",
        reference: str = "reference",
        field_region: str = "Region 1",
        start_date: str = "01-01-2024",
        divided_address: str = "",
        wave_com_dte: str = "31-01-2024",
    ) -> BlaiseFRSCreateCaseModel:
        return BlaiseFRSCreateCaseModel(
            questionnaire_name,
            {
                BlaiseFields.case_id: case_id,
                BlaiseFields.field_region: field_region,
                BlaiseFields.outcome_code: "110",
                BlaiseFields.field_team: "B-Team",
                BlaiseFields.data_model_name: "LM2007",
                BlaiseFields.address_line_1: address_line1,
                BlaiseFields.address_line_2: address_line2,
                BlaiseFields.address_line_3: address_line3,
                BlaiseFields.county: "Gwent",
                BlaiseFields.town: town,
                BlaiseFields.postcode: postcode,
                BlaiseFields.reference: reference,
                BlaiseFields.latitude: latitude,
                BlaiseFields.longitude: longitude,
                BlaiseFields.priority: "1",
                BlaiseFields.rand: "1",
                BlaiseFields.start_date: start_date,
                BlaiseFields.divided_address_indicator: divided_address,
                BlaiseFields.wave_com_dte: wave_com_dte,
                BlaiseFields.LAUA: "Loco",
            },
        )

    @staticmethod
    def get_populated_lms_create_case_model(
        questionnaire_name: str = "LMS2101_AA1",
        case_id: str = "10010",
        latitude: str = "10020202",
        longitude: str = "34949494",
        address_line1: str = "12 Blaise Street",
        address_line2: str = "Blaise Hill",
        address_line3: str = "Blaiseville",
        town: str = "Newport",
        postcode: str = "cf99rsd",
        LAUA: str = "Loco",
        reference: str = "reference",
        field_region: str = "Region 1",
        outcome_code: str = "301",
        data_model_name: str = "LM2007",
        wave_com_dte: str = "31-01-2023",
        wave="1",
        uac_chunks: Optional[UacChunks] = UacChunks(
            uac1="3456", uac2="3453", uac3="4546"
        ),
    ) -> BlaiseLMSCreateCaseModel:
        return BlaiseLMSCreateCaseModel(
            questionnaire_name,
            {
                BlaiseFields.case_id: case_id,
                BlaiseFields.field_region: field_region,
                BlaiseFields.wave: wave,
                BlaiseFields.outcome_code: outcome_code,
                BlaiseFields.telephone_number_1: "07900990901",
                BlaiseFields.telephone_number_2: "07900990902",
                BlaiseFields.appointment_telephone_number: "07900990903",
                BlaiseFields.field_team: "B-Team",
                BlaiseFields.data_model_name: "LM2007",
                BlaiseFields.address_line_1: address_line1,
                BlaiseFields.address_line_2: address_line2,
                BlaiseFields.address_line_3: address_line3,
                BlaiseFields.county: "Gwent",
                BlaiseFields.town: town,
                BlaiseFields.postcode: postcode,
                BlaiseFields.LAUA: LAUA,
                BlaiseFields.reference: reference,
                BlaiseFields.latitude: latitude,
                BlaiseFields.longitude: longitude,
                BlaiseFields.priority: "1",
                BlaiseFields.wave_com_dte: wave_com_dte,
                BlaiseFields.LAUA: "Loco",
            },
            uac_chunks=uac_chunks,
        )
