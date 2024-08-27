from typing import Optional

from models.create.blaise.blaiise_frs_create_case_model import BlaiseFRSCreateCaseModel
from models.create.blaise.blaiise_lms_create_case_model import BlaiseLMSCreateCaseModel
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
        divided_address: str = "",
    ) -> BlaiseFRSCreateCaseModel:
        return BlaiseFRSCreateCaseModel(
            questionnaire_name,
            {
                "qiD.Serial_Number": case_id,
                "qDataBag.FieldRegion": field_region,
                "hOut": "110",
                "qDataBag.FieldTeam": "B-Team",
                "dataModelName": "LM2007",
                "qDataBag.Prem1": address_line1,
                "qDataBag.Prem2": address_line2,
                "qDataBag.Prem3": address_line3,
                "qDataBag.District": "Gwent",
                "qDataBag.PostTown": town,
                "qDataBag.PostCode": postcode,
                "qDataBag.UPRN": reference,
                "qDataBag.UPRN_Latitude": latitude,
                "qDataBag.UPRN_Longitude": longitude,
                "qDataBag.priority": "1",
                "qDataBag.Rand": "1",
                "qDataBag.DivAddInd": divided_address,
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
                "qiD.Serial_Number": case_id,
                "qDataBag.FieldRegion": field_region,
                "qDataBag.Wave": wave,
                "hOut": outcome_code,
                "qDataBag.TelNo": "07900990901",
                "qDataBag.TelNo2": "07900990902",
                "telNoAppt": "07900990903",
                "qDataBag.FieldTeam": "B-Team",
                "dataModelName": data_model_name,
                "qDataBag.Prem1": address_line1,
                "qDataBag.Prem2": address_line2,
                "qDataBag.Prem3": address_line3,
                "qDataBag.District": "Gwent",
                "qDataBag.PostTown": town,
                "qDataBag.PostCode": postcode,
                "qDataBag.UPRN": reference,
                "qDataBag.UPRN_Latitude": latitude,
                "qDataBag.UPRN_Longitude": longitude,
                "qDataBag.priority": "1",
                "qDataBag.WaveComDTE": wave_com_dte,
                "qDataBag.Rand": "1",
            },
            uac_chunks=uac_chunks,
        )
