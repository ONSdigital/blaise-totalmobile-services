from datetime import datetime
from typing import Dict, List

from models.blaise.blaise_lms_case_information_model import BlaiseLMSCaseInformationModel, ContactDetails
from models.blaise.blaise_case_information_base_model import AddressDetails
from models.blaise.blaise_case_information_base_model import AddressCoordinates, Address
from services.mappers.mapper_base import MapperServiceBase


class BlaiseLMSCaseMapperService(MapperServiceBase):

    def map_lms_case_information_models(
            self,
            questionnaire_name: str,
            questionnaire_case_data: List[Dict[str, str]]) -> List[BlaiseLMSCaseInformationModel]:

        cases = []
        for case_data_item in questionnaire_case_data:
            case = self.map_lms_case_information_model(
                questionnaire_name,
                case_data_item
            )
            cases.append(case)

        return cases

    def map_lms_case_information_model(
            self,
            questionnaire_name: str,
            case_data_dictionary: Dict[str, str]) -> BlaiseLMSCaseInformationModel:

        wave_com_dte_str = case_data_dictionary.get("qDataBag.WaveComDTE", "")
        wave_com_dte = (
            datetime.strptime(wave_com_dte_str, "%d-%m-%Y")
            if wave_com_dte_str != ""
            else None
        )
        wave = str(case_data_dictionary.get("qDataBag.Wave"))
        tla = questionnaire_name[0:3]

        return BlaiseLMSCaseInformationModel(
            questionnaire_name=questionnaire_name,
            tla=tla,
            case_id=self.get_case_id(case_data_dictionary),
            data_model_name=case_data_dictionary.get("dataModelName"),
            wave=int(wave) if wave != 'None' else None,
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
            contact_details=ContactDetails(
                telephone_number_1=case_data_dictionary.get("qDataBag.TelNo"),
                telephone_number_2=case_data_dictionary.get("qDataBag.TelNo2"),
                appointment_telephone_number=case_data_dictionary.get("telNoAppt"),
            ),
            outcome_code=self.get_outcome_code(case_data_dictionary),
            priority=case_data_dictionary.get("qDataBag.Priority"),
            field_case=case_data_dictionary.get("qDataBag.FieldCase"),
            field_region=case_data_dictionary.get("qDataBag.FieldRegion"),
            field_team=case_data_dictionary.get("qDataBag.FieldTeam"),
            wave_com_dte=wave_com_dte,
            has_call_history=self.string_to_bool(
                case_data_dictionary.get("catiMana.CatiCall.RegsCalls[1].DialResult")
            ),
            rotational_knock_to_nudge_indicator=self.convert_indicator_to_y_n_or_empty(
                case_data_dictionary.get("qRotate.RDMktnIND")
            ),
            rotational_outcome_code=self.convert_string_to_integer(
                case_data_dictionary.get("qRotate.RHOut", "0")
            ),
        )
