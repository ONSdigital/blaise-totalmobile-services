from enum import Enum


class LMSQuestionnaireOutcomeCodes(Enum):
    NOT_STARTED_0 = 0
    WEB_NUDGED_120 = 120
    APPOINTMENT_300 = 300
    NON_CONTACT_310 = 310
    PHONE_NO_REMOVED_BY_TO_320 = 320
    REFUSAL_HARD_460 = 460
    REFUSAL_SOFT_461 = 461
    INELIGIBLE_NO_TRACE_OF_ADDRESS_510 = 510
    INELIGIBLE_VACANT_540 = 540
    INELIGIBLE_NON_RESIDENTIAL_551 = 551
    INELIGIBLE_INSTITUTION_560 = 560
    INELIGIBLE_SECOND_OR_HOLIDAY_HOME_580 = 580
    WRONG_ADDRESS_640 = 640


class FRSQuestionnaireOutcomeCodes(Enum):
    NOT_STARTED_0 = 0
    COMPLETED_110 = 110
    PARTIALLY_COMPLETED_210 = 210
    NO_CONTACT_WITH_ANYONE_AT_ADDRESS_310 = 310
    CONTACT_MADE_AT_ADDRESS_NO_CONTACT_WITH_SAMPLED_HOUSEHOLD_MULTI_320 = 320
    CONTACT_WITH_SAMPLED_HOUSEHOLD_NO_CONTACT_WITH_RESPONSIBLE_RESIDENT_330 = 330
    HQ_OFFICE_REFUSAL_GENERAL_410 = 410
    MULTI_INFORMATION_REFUSED_NO_OF_HOUSEHOLDS_AT_ADDRESS_420 = 420
    REFUSAL_AT_INTRODUCTION_BEFORE_INTERVIEW_BY_ADULT_HOUSEHOLD_MEMBER_431 = 431
    REFUSAL_AT_INTRODUCTION_BEFORE_INTERVIEW_BY_PROXY_432 = 432
    REFUSAL_DURING_INTERVIEW_HRP_BU_MEMBER_REFUSED_TO_COMPLETE_INTERVIEW_441 = 441
    REFUSAL_DURING_INTERVIEW_12_PLUS_DKS_OR_REFUSALS_IN_HHLD_SECTION_HRP_BU_442 = 442
    BROKEN_APPOINTMENT_NO_RE_CONTACT_450 = 450
    ILL_AT_HOME_DURING_SURVEY_PERIOD_512 = 512
    AWAY_IN_HOSPITAL_DURING_SURVEY_PERIOD_522 = 522
    PHYSICALLY_MENTALLY_UNABLE_INCOMPETENT_532 = 532
    LANGUAGE_DIFFICULTIES_542 = 542
    NOT_ISSUED_TO_INTERVIEWER_OFFICE_APPROVAL_NEEDED_611 = 611
    ISSUED_BUT_NOT_ATTEMPTED_OFFICE_APPROVAL_NEEDED_612 = 612
    INACCESSIBLE_620 = 620
    UNABLE_TO_LOCATE_ADDRESS_630 = 630
    UNKNOWN_WHETHER_RESIDENTIAL_HOUSING_INFORMATION_REFUSED_641 = 641
    UNKNOWN_WHETHER_RESIDENTIAL_HOUSING_NO_CONTACT_WITH_KNOWLEDGEABLE_PERSON_642 = 642
    RESIDENTIAL_ADDRESS_UNKNOWN_IF_ELIGIBLE_HOUSEHOLD_INFORMATION_REFUSED_651 = 651
    RESIDENTIAL_ADDRESS_UNKNOWN_IF_ELIGIBLE_HOUSEHOLD_NO_CONTACT_WITH_KNOWLEDGEABLE_PERSON_652 = (
        652
    )
    OTHER_UNKNOWN_ELIGIBILITY_OFFICE_APPROVAL_NEEDED_670 = 670
    NOT_YET_BUILT_UNDER_CONSTRUCTION_710 = 710
    DEMOLISHED_DERELICT_720 = 720
    VACANT_EMPTY_730 = 730
    NON_RESIDENTIAL_ADDRESS_740 = 740
    ADDRESS_OCCUPIED_NO_RESIDENT_HOUSEHOLD_750 = 750
    COMMUNAL_ESTABLISHMENT_INSTITUTION_760 = 760
    DWELLING_OF_FOREIGN_SERVICE_PERSONNEL_DIPLOMATS_771 = 771
    ALL_RESIDENTS_UNDER_16_772 = 772
    OTHER_RESIDENT_HOUSEHOLD_NO_ELIGIBLE_RESIDENTS_773 = 773
    DIRECTED_NOT_TO_SAMPLE_AT_ADDRESS_781 = 781
    NOT_TO_INTERVIEW_INSTRUCTS_SCOTTISH_PRE_SELECTION_SHEET_782 = 782
    HOUSEHOLD_LIMIT_ON_QUOTA_REACHED_MAXIMUM_OF_4_EXTRA_HOUSEHOLDS_783 = 783
    OTHER_OFFICE_APPROVAL_NEEDED_790 = 790
