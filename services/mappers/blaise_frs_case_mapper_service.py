from datetime import datetime
from typing import Dict, List

from models.blaise.blaise_frs_case_information_model import BlaiseFRSCaseInformationModel
from models.blaise.blaise_case_information_base_model import AddressDetails
from models.blaise.blaise_case_information_base_model import AddressCoordinates, Address
from services.mappers.mapper_base import MapperServiceBase


class BlaiseFRSCaseMapperService(MapperServiceBase):

    def map_frs_case_information_models(
            self,
            questionnaire_name: str,
            questionnaire_case_data: List[Dict[str, str]]) -> List[BlaiseFRSCaseInformationModel]:

        cases = []
        for case_data_item in questionnaire_case_data:
            case = self.map_frs_case_information_model(
                questionnaire_name,
                case_data_item
            )
            cases.append(case)

        return cases

    def map_frs_case_information_model(
            self,
            questionnaire_name: str,
            case_data_dictionary: Dict[str, str]) -> BlaiseFRSCaseInformationModel:

        wave_com_dte_str = case_data_dictionary.get("qDataBag.WaveComDTE", "")
        wave_com_dte = (
            datetime.strptime(wave_com_dte_str, "%d-%m-%Y")
            if wave_com_dte_str != ""
            else None
        )
        wave = case_data_dictionary.get("qDataBag.Wave")
        tla = questionnaire_name[0:3]

        return BlaiseFRSCaseInformationModel(
            questionnaire_name=questionnaire_name,
            tla=tla,
            case_id=case_data_dictionary.get("qiD.Serial_Number"),
            data_model_name=case_data_dictionary.get("dataModelName"),
            wave=int(wave) if wave else None,
            address_details=AddressDetails(
                reference=case_data_dictionary.get("qDataBag.UPRN", ""),
                address=Address(
                    address_line_1=case_data_dictionary.get("qDataBag.Prem1"),
                    address_line_2=case_data_dictionary.get("qDataBag.Prem2"),
                    address_line_3=case_data_dictionary.get("qDataBag.Prem3"),
                    county=case_data_dictionary.get("qDataBag.District"),
                    town=case_data_dictionary.get("qDataBag.PostTown"),
                    postcode=case_data_dictionary.get("qDataBag.PostCode"),
                    coordinates=AddressCoordinates(
                        latitude=case_data_dictionary.get("qDataBag.UPRN_Latitude"),
                        longitude=case_data_dictionary.get("qDataBag.UPRN_Longitude"),
                    ),
                ),
            ),
            priority=case_data_dictionary.get("qDataBag.Priority"),
            field_case=case_data_dictionary.get("qDataBag.FieldCase"),
            field_region=case_data_dictionary.get("qDataBag.FieldRegion"),
            field_team=case_data_dictionary.get("qDataBag.FieldTeam"),
            wave_com_dte=wave_com_dte
        )
