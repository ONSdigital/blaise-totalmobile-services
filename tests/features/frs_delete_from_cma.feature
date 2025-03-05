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

#
#  Scenario Outline: Outcome code and refusal reason are updated when Totalmobile sends a request with an outcome code of <outcome_code>, <refusal_reason_code>, and Blaise case has outcome code of <blaise_outcome_code>
#    Given there is a questionnaire "FRS2401" with case "12345" in Blaise
#    And the case has an outcome code of <blaise_outcome_code>
#    When Totalmobile sends an update for reference "FRS2401.12345" with a refusal
#      | field_name      | value                  |
#      | outcome_code    | <outcome_code>         |
#      | refusal_reason  | <refusal_reason_code>  |
#    And <outcome_code> is between 400 and 500
#    Then the case "12345" for questionnaire "FRS2401" has been updated with
#      | field_name          | value                 |
#      | hOut                | <outcome_code>        |
#      | qDataBag.RefReas    | <refusal_reason_code> |
#    And "Outcome code and refusal reason updated (Questionnaire=FRS2401, Case Id=12345, Blaise hOut=<blaise_outcome_code>, TM RefReas=<refusal_reason_code>, TM hOut=<outcome_code>)" is logged as an information message
#    And a "200 OK" response is sent back to Totalmobile
#    Examples: Blaise outcome code is 0
#      | blaise_outcome_code | outcome_code | refusal_reason_code  |
#      | 0                   | 410          | 431                  |
#      | 0                   | 410          | 432                  |
#      | 0                   | 410          | 441                  |
#      | 0                   | 410          | 442                  |
#      | 0                   | 410          | 450                  |
#      | 0                   | 420          | 431                  |
#      | 0                   | 420          | 432                  |
#      | 0                   | 420          | 441                  |
#      | 0                   | 420          | 442                  |
#      | 0                   | 420          | 450                  |
