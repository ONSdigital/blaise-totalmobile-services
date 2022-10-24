Feature: Filter wave 2 and 3 cases

  Scenario Outline: Eligible wave 2 and 3 LMS cases without telephone numbers are sent to Totalmobile
    Given there is a <questionnaire_name> with a totalmobile release date of today
    And case <case_id> for <questionnaire_name> has the following data
      | field_name           | value          |
      | outcome_code         | <outcome_code> |
      | qDataBag.Wave        | <wave>         |
      | qDataBag.FieldCase   | <fieldcase>    |
      | qDataBag.TelNo       | <telno1>       |
      | qDataBag.TelNo2      | <telno2>       |
      | telNoAppt            | <telNoAppt>    |
      | qDataBag.FieldRegion | <region>       |
      | qRotate.RDMktnIND    | <rdmktnind>    |
      | qRotate.RHOut        | <rhout>        |
    When create_totalmobile_jobs is run
    Then a cloud task is created for case <case_id> in questionnaire <questionnaire_name> with the reference <tm_job_ref>
    Examples:
      | case_id | questionnaire_name | tm_job_ref        | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |        |        |           | Region 1 |           | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |        |        |           | Region 1 |           | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |        |        |           | Region 1 | N         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |        |        |           | Region 1 | N         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |        |        |           | Region 1 | N         | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |        |        |           | Region 1 | N         | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |        |        |           | Region 1 |           | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |        |        |           | Region 1 |           | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |        |        |           | Region 1 | N         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |        |        |           | Region 1 | N         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |        |        |           | Region 1 | N         | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |        |        |           | Region 1 | N         | 310   |

  Scenario Outline: Eligible wave 2 and 3 LMS cases with a telephone number are sent to Totalmobile
    Given there is a <questionnaire_name> with a totalmobile release date of today
    And case <case_id> for <questionnaire_name> has the following data
      | field_name           | value          |
      | outcome_code         | <outcome_code> |
      | qDataBag.Wave        | <wave>         |
      | qDataBag.FieldCase   | <fieldcase>    |
      | qDataBag.TelNo       | <telno1>       |
      | qDataBag.TelNo2      | <telno2>       |
      | telNoAppt            | <telNoAppt>    |
      | qDataBag.FieldRegion | <region>       |
      | qRotate.RHOut        | <rhout>        |
    When create_totalmobile_jobs is run
    Then a cloud task is created for case <case_id> in questionnaire <questionnaire_name> with the reference <tm_job_ref>
    Examples:
      | case_id | questionnaire_name | tm_job_ref        | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region   | rhout |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         |         | 0700000   | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         |         | 0700000   | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 2    | Y         |         |         | 0700000   | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 2    | Y         |         |         | 0700000   | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         |         | 0700000   | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         |         | 0700000   | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         | 0700000 |         |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         | 0700000 |           | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         |         | 0700000   | Region 1 | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 3    | Y         |         |         | 0700000   | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         | 0700000 |         |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         | 0700000 |           | Region 1 | 310   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 3    | Y         |         |         | 0700000   | Region 1 | 310   |


  Scenario Outline: Ineligible wave 2 and 3 LMS cases without telephone numbers are sent to Totalmobile
    Given there is a <questionnaire_name> with a totalmobile release date of today
    And case <case_id> for <questionnaire_name> has the following data
      | field_name           | value          |
      | outcome_code         | <outcome_code> |
      | qDataBag.Wave        | <wave>         |
      | qDataBag.FieldCase   | <fieldcase>    |
      | qDataBag.TelNo       | <telno1>       |
      | qDataBag.TelNo2      | <telno2>       |
      | telNoAppt            | <telNoAppt>    |
      | qDataBag.FieldRegion | <region>       |
      | qRotate.RDMktnIND    | <rdmktnind>    |
      | qRotate.RHOut        | <rhout>        |
    When create_totalmobile_jobs is run
    Then no cloud tasks are created
    Examples:
      | case_id | questionnaire_name | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 12345   | LMS2210_AA1        | 110          | 2    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | N         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | Y         |        |        |           | Region 1 | Y         | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | Y         |        |        |           | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | 110          | 2    | Y         | 070000 |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | N         | 070000 |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | Y         | 070000 |        |           | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | 110          | 2    | Y         |        | 070000 |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | N         |        | 070000 |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | Y         |        | 070000 |           | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | 110          | 2    | Y         |        |        | 070000    | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | N         |        |        | 070000    | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 2    | Y         |        |        | 070000    | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | 110          | 3    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | N         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | Y         |        |        |           | Region 1 | Y         | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | Y         |        |        |           | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | 110          | 3    | Y         | 070000 |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | N         | 070000 |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | Y         | 070000 |        |           | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | 110          | 3    | Y         |        | 070000 |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | N         |        | 070000 |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | Y         |        | 070000 |           | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | 110          | 3    | Y         |        |        | 070000    | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | N         |        |        | 070000    | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | 0            | 3    | Y         |        |        | 070000    | Region 1 |           | 110   |
