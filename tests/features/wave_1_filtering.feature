Feature: Filter wave 1 cases
  Scenario Outline: Eligible LMS cases are sent to Totalmobile
    Given case <case_id> for <questionnaire_name> has the following data
      | HOut	             | <hout>      |
      | qDataBag.Wave	     | <wave>      |
      | qDataBag.FieldCase   | <fieldcase> |
      | qDataBag.TelNo	     | <telno1>    |
      | qDataBag.TelNo2	     | <telno2>    |
    When create_totalmobile_jobs_trigger is run
    Then case <case_id> for questionnaire <questionnaire_name> is sent to Totalmobile with reference <tm_job_ref>
    Examples:
      | case_id     | questionnaire_name | tm_job_ref        | hout | wave | fieldcase | telno1 | telno2 |
      | 12345	    | LMS2210_AA1	     | LMS2210.AA1-12345 | 0    | 1    | Y         |        |        |
      | 12345	    | LMS2210_AA1	     | LMS2210.AA1-12345 | 310  | 1    | Y         |        |        |
      | 12345	    | LMS2210_AA1	     | LMS2210.AA1-12345 | 320  | 1    | Y         |        |        |
      | 12345	    | LMS8304_RR1	     | LMS8304.RR1-12345 | 0    | 1    | Y         |        |        |
      | 54321	    | LMS2210_AA1	     | LMS2210.AA1-54321 | 0    | 1    | Y         |        |        |

  Scenario Outline: Ineligible LMS cases are not sent to Totalmobile
    Given case <case_id> for <questionnaire_name> has the following data
      | HOut	             | <hout>      |
      | qDataBag.Wave	     | <wave>      |
      | qDataBag.FieldCase   | <fieldcase> |
      | qDataBag.TelNo	     | <telno1>    |
      | qDataBag.TelNo2	     | <telno2>    |
    When create_totalmobile_jobs_trigger is run
    Then case <case_id> for questionnaire <questionnaire_name> is not sent to Totalmobile
    Examples:
      | case_id     | questionnaire_name | hout | wave | fieldcase | telno1      | telno2      |
      | 12345	    | LMS2210_AA1	     | 110  | 1    | Y         |             |             |
      | 12345	    | LMS2210_AA1	     | 0    | 2    | Y         |             |             |
      | 12345	    | LMS2210_AA1	     | 0    | 1    | N         |             |             |
      | 12345	    | LMS2210_AA1	     | 0    | 1    | Y         | 07000000000 |             |
      | 12345	    | LMS2210_AA1	     | 0    | 1    | Y         |             | 07000000000 |
      | 12345	    | LMS8304_RR1	     | 110  | 1    | Y         |             |             |
      | 54321	    | LMS2210_AA1	     | 110  | 1    | Y         |             |             |