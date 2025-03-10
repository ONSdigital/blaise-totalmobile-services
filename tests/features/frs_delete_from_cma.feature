Feature: delete case from CMA
  Background:
    Given the survey type is "FRS"

  Scenario Outline: Case is removed from CMA after a case has successfully updated in Blaise to <outcome_code> from Totalmobile request
    Given there is a questionnaire "FRS2401" with case "12345" in CMA
    When Totalmobile sends a FRS update for reference "FRS2401.12345"
      | field_name    | value          |
      | outcome_code  | <outcome_code> |
    Then the case "12345" for questionnaire "FRS2401" has been deleted from CMA
      | field_name | value          |
      | hOut       | <outcome_code> |
    And "Case 12345 for questionnaire FRS2401 with an outcome code of <outcome_code> will be recalled from CMA." is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 410          |
      | 420          |
      | 431          |
      | 432          |
      | 441          |
      | 442          |
      | 450          |
      | 512          |
      | 522          |
      | 532          |
      | 542          |
      | 611          |
      | 612          |
      | 620          |
      | 630          |
      | 641          |
      | 642          |
      | 651          |
      | 652          |
      | 670          |
      | 710          |
      | 720          |
      | 730          |
      | 740          |
      | 750          |
      | 760          |
      | 771          |
      | 772          |
      | 773          |
      | 781          |
      | 782          |
      | 783          |
      | 790          |


Scenario Outline: Case is NOT removed from CMA after a case has successfully updated in Blaise to <outcome_code> from Totalmobile request
    Given there is a questionnaire "FRS2401" with case "12345" in CMA
    When Totalmobile sends a FRS update for reference "FRS2401.12345"
      | field_name    | value          |
      | outcome_code  | <outcome_code> |
    Then the case "12345" for questionnaire "FRS2401" has NOT been deleted from CMA
      | field_name | value          |
      | hOut       | <outcome_code> |
    And "Totalmobile case has an outcome code of <outcome_code> and should not to be removed from CMA." is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 310          |
      | 320          |
      | 330          |


Scenario Outline: Case is NOT removed from CMA after a case failed to update in Blaise to <outcome_code> from Totalmobile request
    Given there is a questionnaire "FRS2401" with case "12345" in CMA
    When Totalmobile sends a FRS update for reference "FRS2401.12345" which fails to update Blaise
      | field_name    | value          |
      | outcome_code  | <outcome_code> |
    Then the case "12345" for questionnaire "FRS2401" has NOT been deleted from CMA
      | field_name | value          |
      | hOut       | <outcome_code> |
    And "Failed to update case 12345 for questionnaire FRS2401 in Blaise: Michael Scott is no longer welcome at Improv Club" is logged as an error message
    And a "500 Internal Server Error" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 410          |
      | 420          |
      | 431          |
      | 432          |
      | 441          |
      | 442          |
      | 450          |
      | 512          |
      | 522          |
      | 532          |
      | 542          |
      | 611          |
      | 612          |
      | 620          |
      | 630          |
      | 641          |
      | 642          |
      | 651          |
      | 652          |
      | 670          |
      | 710          |
      | 720          |
      | 730          |
      | 740          |
      | 750          |
      | 760          |
      | 771          |
      | 772          |
      | 773          |
      | 781          |
      | 782          |
      | 783          |
      | 790          |
