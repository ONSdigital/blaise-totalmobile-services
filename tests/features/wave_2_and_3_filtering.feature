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
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1 |           | 0     |
      | 0            | 2    | Y         |        |        |           | Region 1 |           | 310   |
      | 0            | 2    | Y         |        |        |           | Region 1 |           | 320   |
      | 0            | 3    | Y         |        |        |           | Region 1 |           | 0     |
      | 0            | 3    | Y         |        |        |           | Region 1 |           | 310   |
      | 0            | 3    | Y         |        |        |           | Region 1 |           | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 0, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1 | 0         | 0     |
      | 0            | 2    | Y         |        |        |           | Region 1 | 0         | 310   |
      | 0            | 2    | Y         |        |        |           | Region 1 | 0         | 320   |
      | 0            | 3    | Y         |        |        |           | Region 1 | 0         | 0     |
      | 0            | 3    | Y         |        |        |           | Region 1 | 0         | 310   |
      | 0            | 3    | Y         |        |        |           | Region 1 | 0         | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 310, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 310          | 2    | Y         |        |        |           | Region 1 |           | 0     |
      | 310          | 2    | Y         |        |        |           | Region 1 |           | 310   |
      | 310          | 2    | Y         |        |        |           | Region 1 |           | 320   |
      | 310          | 3    | Y         |        |        |           | Region 1 |           | 0     |
      | 310          | 3    | Y         |        |        |           | Region 1 |           | 310   |
      | 310          | 3    | Y         |        |        |           | Region 1 |           | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 310, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 310          | 2    | Y         |        |        |           | Region 1 | 0         | 0     |
      | 310          | 2    | Y         |        |        |           | Region 1 | 0         | 310   |
      | 310          | 2    | Y         |        |        |           | Region 1 | 0         | 320   |
      | 310          | 3    | Y         |        |        |           | Region 1 | 0         | 0     |
      | 310          | 3    | Y         |        |        |           | Region 1 | 0         | 310   |
      | 310          | 3    | Y         |        |        |           | Region 1 | 0         | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 320, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 320          | 2    | Y         |        |        |           | Region 1 |           | 0     |
      | 320          | 2    | Y         |        |        |           | Region 1 |           | 310   |
      | 320          | 2    | Y         |        |        |           | Region 1 |           | 320   |
      | 320          | 3    | Y         |        |        |           | Region 1 |           | 0     |
      | 320          | 3    | Y         |        |        |           | Region 1 |           | 310   |
      | 320          | 3    | Y         |        |        |           | Region 1 |           | 320   |

    Examples: Waves 2 and 3, no telephone number, outcome_code is 320, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 320          | 2    | Y         |        |        |           | Region 1 | 0         | 0     |
      | 320          | 2    | Y         |        |        |           | Region 1 | 0         | 310   |
      | 320          | 2    | Y         |        |        |           | Region 1 | 0         | 320   |
      | 320          | 3    | Y         |        |        |           | Region 1 | 0         | 0     |
      | 320          | 3    | Y         |        |        |           | Region 1 | 0         | 310   |
      | 320          | 3    | Y         |        |        |           | Region 1 | 0         | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 0, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region   | rdmktnind | rhout |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1 |           | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1 |           | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1 |           | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1 |           | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1 |           | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1 |           | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1 |           | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1 |           | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1 |           | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1 |           | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1 |           | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1 |           | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1 |           | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1 |           | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1 |           | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1 |           | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1 |           | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1 |           | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 0, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region   | rdmktnind | rhout |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 0     |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 0     |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 0     |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 310   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 310   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 310   |
      | 0            | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 320   |
      | 0            | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 320   |
      | 0            | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 320   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 0     |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 0     |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 0     |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 310   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 310   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 310   |
      | 0            | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 320   |
      | 0            | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 320   |
      | 0            | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 310, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region   | rdmktnind | rhout |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1 |           | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1 |           | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1 |           | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1 |           | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1 |           | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1 |           | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1 |           | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1 |           | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1 |           | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1 |           | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1 |           | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1 |           | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1 |           | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1 |           | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1 |           | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1 |           | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1 |           | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1 |           | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 310, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region   | rdmktnind | rhout |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 0     |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 0     |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 0     |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 310   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 310   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 310   |
      | 310          | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 320   |
      | 310          | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 320   |
      | 310          | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 320   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 0     |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 0     |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 0     |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 310   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 310   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 310   |
      | 310          | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 320   |
      | 310          | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 320   |
      | 310          | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 320, rdmktnind is empty
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region   | rdmktnind | rhout |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1 |           | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1 |           | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1 |           | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1 |           | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1 |           | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1 |           | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1 |           | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1 |           | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1 |           | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1 |           | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1 |           | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1 |           | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1 |           | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1 |           | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1 |           | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1 |           | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1 |           | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1 |           | 320   |

    Examples: Waves 2 and 3 with telephone numbers, outcome_code is 320, rdmktnind is 0
      | outcome_code | wave | fieldcase | telno1  | telno2  | telNoAppt | region   | rdmktnind | rhout |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 0     |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 0     |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 0     |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 310   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 310   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 310   |
      | 320          | 2    | Y         | 0700000 |         |           | Region 1 | 0         | 320   |
      | 320          | 2    | Y         |         | 0700000 |           | Region 1 | 0         | 320   |
      | 320          | 2    | Y         |         |         | 0700000   | Region 1 | 0         | 320   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 0     |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 0     |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 0     |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 310   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 310   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 310   |
      | 320          | 3    | Y         | 0700000 |         |           | Region 1 | 0         | 320   |
      | 320          | 3    | Y         |         | 0700000 |           | Region 1 | 0         | 320   |
      | 320          | 3    | Y         |         |         | 0700000   | Region 1 | 0         | 320   |

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
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 0            | 2    | N         |        |        |           | Region 1 |           | 0     |
      | 0            | 2    | N         | 070000 |        |           | Region 1 |           | 0     |
      | 0            | 2    | N         |        | 070000 |           | Region 1 |           | 0     |
      | 0            | 2    | N         |        |        | 070000    | Region 1 |           | 0     |
      | 0            | 3    | N         |        |        |           | Region 1 |           | 0     |
      | 0            | 3    | N         | 070000 |        |           | Region 1 |           | 0     |
      | 0            | 3    | N         |        | 070000 |           | Region 1 |           | 0     |
      | 0            | 3    | N         |        |        | 070000    | Region 1 |           | 0     |

    Examples: Waves 2 and 3, outcome_code is 0, rdmktnind is 1 (thus making it ineligible)
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1 | 1          | 0     |
      | 0            | 2    | Y         | 070000 |        |           | Region 1 | 1          | 0     |
      | 0            | 2    | Y         |        | 070000 |           | Region 1 | 1          | 0     |
      | 0            | 2    | Y         |        |        | 070000    | Region 1 | 1          | 0     |
      | 0            | 3    | Y         |        |        |           | Region 1 | 1          | 0     |
      | 0            | 3    | Y         | 070000 |        |           | Region 1 | 1          | 0     |
      | 0            | 3    | Y         |        | 070000 |           | Region 1 | 1          | 0     |
      | 0            | 3    | Y         |        |        | 070000    | Region 1 | 1          | 0     |

    Examples: Waves 2 and 3, outcome_code is 110 (thus making it ineligible)
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 110          | 2    | Y         |        |        |           | Region 1 |           | 0     |
      | 110          | 2    | Y         | 070000 |        |           | Region 1 |           | 0     |
      | 110          | 2    | Y         |        | 070000 |           | Region 1 |           | 0     |
      | 110          | 2    | Y         |        |        | 070000    | Region 1 |           | 0     |
      | 110          | 3    | Y         |        |        |           | Region 1 |           | 0     |
      | 110          | 3    | Y         | 070000 |        |           | Region 1 |           | 0     |
      | 110          | 3    | Y         |        | 070000 |           | Region 1 |           | 0     |
      | 110          | 3    | Y         |        |        | 070000    | Region 1 |           | 0     |

    Examples: Waves 2 and 3, outcome_code is 0, rhout is 110 (thus making it ineligible)
      | outcome_code | wave | fieldcase | telno1 | telno2 | telNoAppt | region   | rdmktnind | rhout |
      | 0            | 2    | Y         |        |        |           | Region 1 |           | 110   |
      | 0            | 2    | Y         | 070000 |        |           | Region 1 |           | 110   |
      | 0            | 2    | Y         |        | 070000 |           | Region 1 |           | 110   |
      | 0            | 2    | Y         |        |        | 070000    | Region 1 |           | 110   |
      | 0            | 3    | Y         |        |        |           | Region 1 |           | 110   |
      | 0            | 3    | Y         | 070000 |        |           | Region 1 |           | 110   |
      | 0            | 3    | Y         |        | 070000 |           | Region 1 |           | 110   |
      | 0            | 3    | Y         |        |        | 070000    | Region 1 |           | 110   |
