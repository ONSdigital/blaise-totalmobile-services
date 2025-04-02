Feature: Filter wave 1 cases
  Background:
    Given the survey type is "LMS"

  Scenario Outline: Eligible LMS cases are sent to Totalmobile
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
    When create_totalmobile_jobs is run
    Then a cloud task is created for case <case_id> in questionnaire <questionnaire_name> with the reference <tm_job_ref>
    Examples:
      | case_id | questionnaire_name | tm_job_ref        | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 1  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 1  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 1  |
      | 12345   | LMS8304_RR1        | LMS8304-RR1.12345 | 0            | 1    | Y         |        |        |           | Region 1  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 1  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 2  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 3  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 4  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 5  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 6  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 7  |
      | 54321   | LMS2210_AA1        | LMS2210-AA1.54321 | 0            | 1    | Y         |        |        |           | Region 8  |

    @documentation
    Examples: Region 1-12 with outcome code permutations
      | case_id | questionnaire_name | tm_job_ref        | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 1  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 1  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 1  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 2  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 2  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 2  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 3  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 3  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 3  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 4  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 4  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 4  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 5  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 5  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 5  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 6  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 6  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 6  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 7  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 7  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 7  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 8  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 8  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 8  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 9  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 9  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 9  |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 10 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 10 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 10 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 11 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 11 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 11 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 0            | 1    | Y         |        |        |           | Region 12 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 310          | 1    | Y         |        |        |           | Region 12 |
      | 12345   | LMS2210_AA1        | LMS2210-AA1.12345 | 320          | 1    | Y         |        |        |           | Region 12 |

  Scenario Outline: Ineligible LMS cases are not sent to Totalmobile
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
    When create_totalmobile_jobs is run
    Then no cloud tasks are created
    Examples: Region 1 only with all eligibility criteria permutations
      | case_id | questionnaire_name | outcome_code | wave | fieldcase | telno1    | telno2    | telNoAppt | region    |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 1  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 1  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 1  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 1  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 1  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 1  |

    @documentation
    Examples: Region 2-12 with all all eligibility criteria permutations, as well as Regions 0 & 13 for admin and testing
      | case_id | questionnaire_name | outcome_code | wave | fieldcase | telno1    | telno2    | telNoAppt | region    |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 2  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 2  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 2  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 2  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 2  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 2  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 3  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 3  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 3  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 3  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 3  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 3  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 4  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 4  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 4  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 4  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 4  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 4  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 5  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 5  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 5  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 5  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 5  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 5  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 6  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 6  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 6  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 6  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 6  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 6  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 7  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 7  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 7  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 7  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 7  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 7  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 8  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 8  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 8  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 8  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 8  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 8  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 9  |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 9  |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 9  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 9  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 9  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 9  |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 10 |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 10 |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 10 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 10 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 10 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 10 |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 11 |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 11 |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 11 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 11 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 11 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 11 |
      | 12345   | LMS2210_AA1        | 0            | 8    | Y         |           |           |           | Region 12 |
      | 12345   | LMS2210_AA1        | 110          | 1    | Y         |           |           |           | Region 12 |
      | 12345   | LMS2210_AA1        | 0            | 1    | N         |           |           |           | Region 12 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         | 072345678 |           |           | Region 12 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           | 072345678 |           | Region 12 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           | 072345678 | Region 12 |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           |           | Region 0  |
      | 12345   | LMS2210_AA1        | 0            | 1    | Y         |           |           |           | Region 13 |