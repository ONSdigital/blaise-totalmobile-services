Feature: Filter wave 2 and 3 cases
  Background:
    Given the survey type is "LMS"

  Scenario Outline: Eligible wave 2 and 3 LMS cases are sent to Totalmobile
    Given there is a LMS2210_AA1 with a totalmobile release date of today
    And case 12345 for LMS2210_AA1 has the following data
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
    Then a cloud task is created for case 12345 in questionnaire LMS2210_AA1 with the reference LMS2210-AA1.12345

    Examples: Waves 2 and 3, no telephone number, outcome_code is 0, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 1  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 1  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 1  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 1  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 1  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 2  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 2  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 2  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 2  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 2  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 2  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 3  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 3  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 3  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 3  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 3  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 3  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 4  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 4  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 4  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 4  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 4  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 4  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 5  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 5  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 5  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 5  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 5  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 5  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 6  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 6  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 6  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 6  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 6  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 6  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 7  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 7  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 7  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 7  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 7  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 7  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 8  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 8  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 8  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 8  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 8  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 8  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 9  |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 9  |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 9  |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 9  |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 9  |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 9  |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 10 |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 10 |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 10 |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 10 |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 10 |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 10 |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 11 |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 11 |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 11 |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 11 |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 11 |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 11 |           | 320   |
      | 0            | 2    | Y         |        |        |           | Region 12 |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 12 |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 12 |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 12 |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 12 |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 12 |           | 320   |


    Examples: Waves 2 and 3, no telephone number, outcome_code is 0, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 1  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 1  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 1  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 1  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 1  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 2  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 2  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 2  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 2  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 2  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 2  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 3  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 3  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 3  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 3  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 3  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 3  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 4  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 4  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 4  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 4  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 4  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 4  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 6  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 6  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 6  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 6  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 6  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 6  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 7  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 7  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 7  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 7  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 7  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 7  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 8  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 8  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 8  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 8  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 8  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 8  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 9  | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 9  | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 9  | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 9  | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 9  | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 9  | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 10 | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 10 | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 10 | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 10 | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 10 | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 10 | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 11 | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 11 | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 11 | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 11 | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 11 | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 11 | 0         | 320   |
      | 0            | 2    | Y         |        |        |           | Region 12 | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 12 | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 12 | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 12 | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 12 | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 12 | 0         | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 310, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 310          | 2    | Y         |        |        |           | Region 1  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 1  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 1  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 1  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 1  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 1  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 2  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 2  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 2  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 2  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 2  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 2  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 3  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 3  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 3  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 3  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 3  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 3  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 4  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 4  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 4  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 4  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 4  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 4  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 5  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 5  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 5  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 5  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 5  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 5  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 6  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 6  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 6  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 6  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 6  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 6  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 7  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 7  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 7  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 7  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 7  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 7  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 8  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 8  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 8  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 8  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 8  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 8  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 9  |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 9  |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 9  |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 9  |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 9  |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 9  |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 10 |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 10 |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 10 |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 10 |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 10 |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 10 |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 11 |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 11 |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 11 |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 11 |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 11 |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 11 |           | 320   |
      | 310          | 2    | Y         |        |        |           | Region 12 |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 12 |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 12 |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 12 |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 12 |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 12 |           | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 310, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 310          | 2    | Y         |        |        |           | Region 1  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 1  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 1  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 1  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 1  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 1  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 2  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 2  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 2  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 2  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 2  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 2  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 3  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 3  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 3  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 3  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 3  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 3  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 4  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 4  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 4  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 4  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 4  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 4  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 6  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 6  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 6  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 6  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 6  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 6  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 7  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 7  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 7  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 7  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 7  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 7  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 8  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 8  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 8  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 8  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 8  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 8  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 9  | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 9  | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 9  | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 9  | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 9  | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 9  | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 10 | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 10 | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 10 | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 10 | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 10 | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 10 | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 11 | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 11 | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 11 | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 11 | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 11 | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 11 | 0         | 320   |
      | 310          | 2    | Y         |        |        |           | Region 12 | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 12 | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 12 | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 12 | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 12 | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 12 | 0         | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 320, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 320          | 2    | Y         |        |        |           | Region 1  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 1  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 1  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 1  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 1  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 1  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 2  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 2  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 2  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 2  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 2  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 2  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 3  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 3  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 3  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 3  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 3  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 3  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 4  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 4  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 4  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 4  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 4  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 4  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 5  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 5  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 5  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 5  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 5  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 5  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 6  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 6  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 6  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 6  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 6  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 6  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 7  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 7  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 7  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 7  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 7  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 7  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 8  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 8  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 8  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 8  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 8  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 8  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 9  |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 9  |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 9  |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 9  |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 9  |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 9  |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 10 |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 10 |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 10 |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 10 |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 10 |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 10 |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 11 |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 11 |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 11 |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 11 |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 11 |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 11 |           | 320   |
      | 320          | 2    | Y         |        |        |           | Region 12 |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 12 |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 12 |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 12 |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 12 |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 12 |           | 320   |


    Examples: Waves 2 and 3, no telephone number, outcome_code is 320, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 320          | 2    | Y         |        |        |           | Region 1  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 1  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 1  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 1  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 1  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 1  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 2  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 2  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 2  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 2  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 2  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 2  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 3  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 3  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 3  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 3  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 3  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 3  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 4  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 4  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 4  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 4  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 4  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 4  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 5  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 5  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 5  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 6  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 6  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 6  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 6  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 6  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 6  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 7  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 7  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 7  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 7  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 7  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 7  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 8  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 8  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 8  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 8  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 8  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 8  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 9  | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 9  | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 9  | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 9  | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 9  | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 9  | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 10 | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 10 | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 10 | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 10 | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 10 | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 10 | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 11 | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 11 | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 11 | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 11 | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 11 | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 11 | 0         | 320   |
      | 320          | 2    | Y         |        |        |           | Region 12 | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 12 | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 12 | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 12 | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 12 | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 12 | 0         | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 0, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region    | rdmktnind | rhout |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 2  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 2  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 2  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 2  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 2  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 2  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 2  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 2  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 2  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 2  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 2  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 2  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 2  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 2  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 2  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 2  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 2  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 2  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 3  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 3  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 3  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 3  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 3  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 3  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 3  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 3  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 3  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 3  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 3  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 3  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 3  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 3  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 3  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 3  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 3  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 3  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 4  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 4  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 4  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 4  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 4  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 4  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 4  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 4  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 4  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 4  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 4  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 4  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 4  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 4  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 4  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 4  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 4  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 4  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 5  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 5  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 5  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 5  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 5  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 5  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 5  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 5  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 5  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 5  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 5  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 5  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 5  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 5  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 5  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 5  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 5  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 5  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 6  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 6  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 6  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 6  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 6  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 6  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 6  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 6  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 6  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 6  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 6  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 6  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 6  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 6  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 6  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 6  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 6  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 6  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 7  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 7  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 7  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 7  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 7  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 7  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 7  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 7  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 7  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 7  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 7  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 7  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 7  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 7  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 7  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 7  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 7  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 7  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 8  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 8  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 8  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 8  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 8  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 8  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 8  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 8  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 8  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 8  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 8  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 8  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 8  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 8  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 8  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 8  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 8  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 8  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 9  |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 9  |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 9  |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 9  |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 9  |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 9  |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 9  |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 9  |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 9  |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 9  |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 9  |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 9  |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 9  |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 9  |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 9  |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 9  |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 9  |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 9  |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 10 |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 10 |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 10 |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 10 |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 10 |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 10 |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 10 |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 10 |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 10 |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 10 |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 10 |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 10 |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 10 |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 10 |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 10 |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 10 |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 10 |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 10 |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 11 |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 11 |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 11 |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 11 |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 11 |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 11 |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 11 |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 11 |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 11 |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 11 |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 11 |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 11 |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 11 |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 11 |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 11 |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 11 |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 11 |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 11 |           | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 12 |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 12 |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 12 |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 12 |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 12 |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 12 |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 12 |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 12 |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 12 |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 12 |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 12 |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 12 |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 12 |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 12 |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 12 |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 12 |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 12 |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 12 |           | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 0, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region    | rdmktnind | rhout |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 320   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 310, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region    | rdmktnind | rhout |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 2  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 2  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 2  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 2  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 2  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 2  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 2  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 2  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 2  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 2  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 2  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 2  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 2  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 2  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 2  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 2  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 2  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 2  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 3  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 3  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 3  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 3  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 3  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 3  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 3  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 3  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 3  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 3  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 3  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 3  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 3  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 3  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 3  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 3  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 3  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 3  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 4  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 4  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 4  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 4  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 4  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 4  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 4  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 4  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 4  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 4  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 4  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 4  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 4  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 4  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 4  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 4  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 4  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 4  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 5  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 5  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 5  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 5  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 5  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 5  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 5  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 5  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 5  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 5  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 5  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 5  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 5  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 5  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 5  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 5  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 5  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 5  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 6  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 6  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 6  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 6  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 6  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 6  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 6  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 6  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 6  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 6  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 6  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 6  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 6  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 6  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 6  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 6  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 6  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 6  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 7  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 7  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 7  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 7  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 7  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 7  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 7  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 7  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 7  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 7  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 7  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 7  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 7  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 7  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 7  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 7  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 7  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 7  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 8  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 8  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 8  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 8  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 8  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 8  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 8  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 8  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 8  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 8  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 8  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 8  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 8  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 8  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 8  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 8  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 8  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 8  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 9  |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 9  |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 9  |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 9  |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 9  |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 9  |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 9  |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 9  |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 9  |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 9  |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 9  |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 9  |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 9  |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 9  |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 9  |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 9  |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 9  |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 9  |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 10 |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 10 |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 10 |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 10 |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 10 |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 10 |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 10 |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 10 |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 10 |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 10 |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 10 |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 10 |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 10 |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 10 |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 10 |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 10 |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 10 |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 10 |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 11 |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 11 |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 11 |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 11 |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 11 |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 11 |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 11 |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 11 |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 11 |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 11 |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 11 |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 11 |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 11 |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 11 |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 11 |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 11 |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 11 |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 11 |           | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 12 |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 12 |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 12 |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 12 |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 12 |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 12 |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 12 |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 12 |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 12 |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 12 |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 12 |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 12 |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 12 |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 12 |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 12 |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 12 |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 12 |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 12 |           | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 310, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region    | rdmktnind | rhout |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 320   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 320, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region    | rdmktnind | rhout |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 2  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 2  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 2  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 2  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 2  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 2  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 2  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 2  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 2  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 2  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 2  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 2  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 2  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 2  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 2  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 2  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 2  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 2  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 3  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 3  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 3  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 3  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 3  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 3  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 3  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 3  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 3  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 3  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 3  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 3  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 3  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 3  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 3  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 3  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 3  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 3  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 4  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 4  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 4  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 4  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 4  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 4  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 4  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 4  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 4  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 4  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 4  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 4  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 4  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 4  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 4  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 4  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 4  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 4  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 5  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 5  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 5  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 5  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 5  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 5  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 5  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 5  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 5  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 5  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 5  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 5  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 5  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 5  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 5  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 5  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 5  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 5  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 6  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 6  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 6  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 6  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 6  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 6  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 6  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 6  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 6  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 6  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 6  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 6  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 6  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 6  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 6  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 6  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 6  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 6  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 7  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 7  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 7  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 7  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 7  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 7  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 7  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 7  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 7  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 7  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 7  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 7  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 7  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 7  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 7  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 7  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 7  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 7  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 8  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 8  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 8  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 8  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 8  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 8  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 8  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 8  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 8  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 8  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 8  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 8  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 8  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 8  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 8  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 8  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 8  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 8  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 9  |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 9  |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 9  |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 9  |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 9  |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 9  |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 9  |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 9  |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 9  |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 9  |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 9  |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 9  |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 9  |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 9  |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 9  |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 9  |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 9  |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 9  |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 10 |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 10 |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 10 |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 10 |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 10 |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 10 |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 10 |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 10 |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 10 |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 10 |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 10 |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 10 |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 10 |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 10 |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 10 |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 10 |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 10 |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 10 |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 11 |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 11 |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 11 |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 11 |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 11 |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 11 |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 11 |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 11 |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 11 |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 11 |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 11 |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 11 |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 11 |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 11 |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 11 |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 11 |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 11 |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 11 |           | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 12 |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 12 |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 12 |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 12 |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 12 |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 12 |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 12 |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 12 |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 12 |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 12 |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 12 |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 12 |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 12 |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 12 |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 12 |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 12 |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 12 |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 12 |           | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 320, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region    | rdmktnind | rhout |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 2  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 2  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 2  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 2  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 2  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 2  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 3  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 3  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 3  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 3  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 3  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 3  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 4  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 4  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 4  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 4  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 4  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 4  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 5  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 5  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 5  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 5  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 5  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 5  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 6  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 6  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 6  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 6  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 6  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 6  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 7  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 7  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 7  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 7  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 7  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 7  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 8  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 8  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 8  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 8  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 8  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 8  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 9  | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 9  | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 9  | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 9  | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 9  | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 9  | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 10 | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 10 | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 10 | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 10 | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 10 | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 10 | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 11 | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 11 | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 11 | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 11 | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 11 | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 11 | 0         | 320   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 12 | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 12 | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 12 | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 12 | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 12 | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 12 | 0         | 320   |

  Scenario Outline: Ineligible wave 2 and 3 LMS cases are not sent to Totalmobile
    Given there is a LMS2210_AA1 with a totalmobile release date of today
    And case 12345 for LMS2210_AA1 has the following data
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

    Examples: Waves 2 and 3, outcome_code is 0, fieldcase is N (thus making it ineligible)
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 0            | 2    | N         |        |        |           | Region 1  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 1  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 1  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 1  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 1  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 1  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 1  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 1  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 2  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 2  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 2  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 2  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 2  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 2  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 2  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 2  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 3  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 3  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 3  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 3  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 3  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 3  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 3  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 3  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 4  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 4  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 4  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 4  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 4  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 4  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 4  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 4  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 5  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 5  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 5  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 5  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 5  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 5  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 5  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 5  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 6  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 6  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 6  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 6  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 6  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 6  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 6  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 6  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 7  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 7  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 7  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 7  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 7  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 7  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 7  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 7  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 8  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 8  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 8  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 8  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 8  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 8  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 8  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 8  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 9  |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 9  |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 9  |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 9  |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 9  |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 9  |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 9  |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 9  |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 10 |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 10 |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 10 |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 10 |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 10 |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 10 |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 10 |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 10 |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 11 |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 11 |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 11 |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 11 |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 11 |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 11 |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 11 |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 11 |           | 0     |
      | 0            | 2    | N         |        |        |           | Region 12 |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 12 |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 12 |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 12 |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 12 |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 12 |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 12 |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 12 |           | 0     |


    Examples: Waves 2 and 3, outcome_code is 0, rdmktnind is 1 (thus making it ineligible)
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 1  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 1  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 1  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 1  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 1  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 1  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 1  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 2  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 2  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 2  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 2  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 2  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 2  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 2  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 2  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 3  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 3  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 3  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 3  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 3  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 3  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 3  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 3  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 4  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 4  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 4  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 4  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 4  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 4  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 4  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 4  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 5  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 5  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 5  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 5  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 5  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 5  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 5  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 5  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 6  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 6  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 6  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 6  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 6  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 6  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 6  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 6  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 7  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 7  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 7  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 7  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 7  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 7  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 7  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 7  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 8  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 8  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 8  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 8  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 8  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 8  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 8  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 8  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 9  | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 9  | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 9  | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 9  | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 9  | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 9  | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 9  | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 9  | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 10 | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 10 | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 10 | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 10 | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 10 | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 10 | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 10 | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 10 | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 11 | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 11 | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 11 | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 11 | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 11 | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 11 | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 11 | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 11 | 1          | 0     |
      | 0            | 2    | Y         |        |        |           | Region 12 | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 12 | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 12 | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 12 | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 12 | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 12 | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 12 | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 12 | 1          | 0     |

    Examples: Waves 2 and 3, outcome_code is 110 (thus making it ineligible)
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 110          | 2    | Y         |        |        |           | Region 1  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 1  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 1  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 1  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 1  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 1  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 1  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 1  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 2  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 2  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 2  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 2  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 2  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 2  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 2  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 2  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 3  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 3  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 3  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 3  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 3  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 3  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 3  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 3  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 4  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 4  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 4  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 4  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 4  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 4  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 4  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 4  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 5  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 5  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 5  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 5  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 5  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 5  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 5  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 5  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 6  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 6  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 6  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 6  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 6  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 6  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 6  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 6  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 7  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 7  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 7  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 7  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 7  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 7  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 7  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 7  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 8  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 8  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 8  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 8  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 8  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 8  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 8  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 8  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 9  |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 9  |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 9  |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 9  |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 9  |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 9  |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 9  |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 9  |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 10 |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 10 |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 10 |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 10 |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 10 |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 10 |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 10 |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 10 |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 11 |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 11 |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 11 |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 11 |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 11 |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 11 |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 11 |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 11 |           | 0     |
      | 110          | 2    | Y         |        |        |           | Region 12 |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 12 |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 12 |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 12 |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 12 |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 12 |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 12 |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 12 |           | 0     |

    Examples: Waves 2 and 3, outcome_code is 0, rhout is 110 (thus making it ineligible)
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region    | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 1  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 1  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 1  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 1  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 1  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 1  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 1  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 2  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 2  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 2  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 2  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 2  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 2  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 2  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 2  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 3  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 3  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 3  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 3  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 3  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 3  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 3  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 3  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 4  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 4  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 4  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 4  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 4  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 4  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 4  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 4  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 5  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 5  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 5  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 5  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 5  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 5  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 5  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 5  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 6  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 6  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 6  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 6  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 6  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 6  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 6  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 6  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 7  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 7  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 7  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 7  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 7  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 7  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 7  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 7  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 8  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 8  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 8  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 8  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 8  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 8  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 8  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 8  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 9  |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 9  |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 9  |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 9  |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 9  |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 9  |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 9  |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 9  |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 10 |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 10 |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 10 |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 10 |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 10 |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 10 |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 10 |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 10 |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 11 |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 11 |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 11 |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 11 |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 11 |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 11 |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 11 |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 11 |           | 110   |
      | 0            | 2    | Y         |        |        |           | Region 12 |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 12 |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 12 |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 12 |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 12 |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 12 |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 12 |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 12 |           | 110   |
