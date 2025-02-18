Feature: update outcome code
  Background:
    Given the survey type is "FRS"

  Scenario Outline: Totalmobile sends a request with an outcome code of <outcome_code> when case has outcome code of <blaise_outcome_code
    Given there is a questionnaire "FRS2401" with case "12345" in Blaise
    And the case has an outcome code of <blaise_outcome_code>
    When Totalmobile sends an update for reference "FRS2401.12345"
      | field_name    | value          |
      | outcome_code  | <outcome_code> |
    And <outcome_code> is NOT between 400 and 500
    Then the case "12345" for questionnaire "FRS2401" has been updated with
      | field_name | value          |
      | hOut       | <outcome_code> |
    And "Outcome code updated (Questionnaire=FRS2401, Case Id=12345, Blaise hOut=<blaise_outcome_code>, TM hOut=<outcome_code>)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples: Blaise outcome code is 0
      | blaise_outcome_code | outcome_code |
      | 0                   | 730          |
      | 0                   | 740          |
      | 0                   | 750          |
      | 0                   | 760          |
      | 0                   | 771          |
      | 0                   | 772          |
      | 0                   | 773          |
      | 0                   | 781          |
      | 0                   | 782          |
      | 0                   | 783          |
      | 0                   | 790          |
      | 0                   | 611          |
      | 0                   | 612          |
      | 0                   | 630          |
      | 0                   | 641          |
      | 0                   | 642          |
      | 0                   | 651          |
      | 0                   | 652          |
      | 0                   | 670          |
      | 0                   | 620          |
      | 0                   | 512          |
      | 0                   | 522          |
      | 0                   | 532          |
      | 0                   | 542          |
      | 0                   | 310          |
      | 0                   | 320          |
      | 0                   | 330          |


  Scenario Outline: Totalmobile sends a request with an outcome code of <outcome_code> when case has outcome code of <blaise_outcome_code>
    Given there is a questionnaire "FRS2401" with case "12345" in Blaise
    And the case has an outcome code of <blaise_outcome_code>
    When Totalmobile sends an update for reference "FRS2401.12345"
      | field_name   | value          |
      | outcome_code | <outcome_code> |
    And <outcome_code> is between 400 and 500
    Then the case "12345" for questionnaire "FRS2401" has been updated with
      | field_name | value          |
      | hOut       | <outcome_code> |
    # TODO: Fix dis
#      | RefReas    | <outcome_code> |
    And "Outcome code and refusal reason updated (Questionnaire=FRS2401, Case Id=12345, Blaise hOut=<blaise_outcome_code>, Blaise RefReas=<blaise_outcome_code>, TM hOut=<outcome_code>)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples: Blaise outcome code is 0
      | blaise_outcome_code | outcome_code |
      | 0                   | 410          |
      | 0                   | 420          |
      | 0                   | 431          |
      | 0                   | 432          |
      | 0                   | 441          |
      | 0                   | 442          |
      | 0                   | 450          |