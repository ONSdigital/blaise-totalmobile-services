from enum import Enum


class BlaiseFields(str, Enum):
    case_id = "qiD.Serial_Number"
    outcome_code = "hOut"
    admin_outcome_code = "qhAdmin.HOut"
    rotational_outcome_code = "qRotate.RHOut"
    call_history = "catiMana.CatiCall.RegsCalls[1].DialResult"
    knock_to_nudge_indicator = "DMktnIND"
    rotational_knock_to_nudge_indicator = "qRotate.RDMktnIND"
    knock_to_nudge_contact_name = "dMktnName"
    priority = "qDataBag.priority"
    wave = "qDataBag.Wave"
    wave_com_dte = "qDataBag.WaveComDTE"
    address_line_1 = "qDataBag.Prem1"
    address_line_2 = "qDataBag.Prem2"
    address_line_3 = "qDataBag.Prem3"
    county = "qDataBag.District"
    town = "qDataBag.PostTown"
    postcode = "qDataBag.PostCode"
    reference = "qDataBag.UPRN"
    latitude = "qDataBag.UPRN_Latitude"
    longitude = "qDataBag.UPRN_Longitude"
    telephone_number_1 = "qDataBag.TelNo"
    telephone_number_2 = "qDataBag.TelNo2"
    appointment_telephone_number = "telNoAppt"
    field_case = "qDataBag.FieldCase"
    field_region = "qDataBag.FieldRegion"
    field_team = "qDataBag.FieldTeam"
    data_model_name = "dataModelName"
    divided_address_indicator = "qDataBag.DivAddInd"
    rand = "qDataBag.Rand"
    tla = "qDataBag.TLA"
