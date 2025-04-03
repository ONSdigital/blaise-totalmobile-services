Feature: Filter wave 4 and 5 cases
  Background:
    Given the survey type is "LMS"

  Scenario Outline: Eligible wave 4 and 5 LMS cases without telephone numbers are sent to Totalmobile
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
    Examples: Region 1
      | case_id | questionnaire_name | tm_job_ref        | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 1 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 1 |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 1 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 1 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 1 |           | 110   |

    @other_regions
    Examples: Regions 2-12
      | case_id | questionnaire_name | tm_job_ref        | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 2  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 2  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 2  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 2  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 3  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 3  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 3  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 3  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 4  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 4  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 4  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 4  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 5  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 5  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 5  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 5  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 6  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 6  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 6  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 6  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 7  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 7  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 7  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 7  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 8  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 8  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 8  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 8  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 9  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 9  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 9  | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 9  |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 10 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 10 |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 10 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 10 |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 11 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 11 |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 11 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 11 |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         | 070000 |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        | 070000 |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        | 070000    | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 12 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 4    | Y         |        |        |           | Region 12 |           | 110   |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         | 070000 |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        | 070000 |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        | 070000    | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 12 | Y         | 0     |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 5    | Y         |        |        |           | Region 12 |           | 110   |

  Scenario Outline: Ineligible wave 4 and 5 LMS cases without telephone numbers are sent to Totalmobile
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
    Examples: Region 1
      | case_id | questionnaire_name | outcome_code      | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 1  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 1  |           | 0     |

    @other_regions
    Examples: Regions 2-12
      | case_id | questionnaire_name | outcome_code      | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 2  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 3  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 4  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 5  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 6  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 7  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 8  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 9  |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 10 |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 11 |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 4    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 4    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 4    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 4    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 110               | 5    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 210               | 5    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 300               | 5    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 360               | 5    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 999               | 5    | Y         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 4    | N         |        |        |           | Region 12 |           | 0     |
      | 12345   | LMS2210_AA1        | 0                 | 5    | N         |        |        |           | Region 12 |           | 0     |
