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
#      | 420          |
#      | 431          |
#      | 432          |
#      | 441          |
#      | 442          |
#      | 450          |
#      | 512          |
#      | 522          |
#      | 532          |
#      | 542          |
#      | 611          |
#      | 612          |
#      | 620          |
#      | 630          |
#      | 641          |
#      | 642          |
#      | 651          |
#      | 652          |
#      | 670          |
#      | 710          |
#      | 720          |
#      | 730          |
#      | 740          |
#      | 750          |
#      | 760          |
#      | 771          |
#      | 772          |
#      | 773          |
#      | 781          |
#      | 782          |
#      | 783          |
#      | 790          |


#  Scenario Outline: Blaise is NOT updated when Totalmobile sends a request with an outcome code of <outcome_code> and case has outcome code of <blaise_outcome_code>
#    Given there is a questionnaire "FRS2401" with case "12345" in Blaise
#    And the case has an outcome code of <blaise_outcome_code>
#    When Totalmobile sends an update for reference "FRS2401.12345"
#      | field_name    | value          |
#      | outcome_code  | <outcome_code> |
#    And <outcome_code> is NOT between 400 and 500
#    Then the case "12345" for questionnaire "FRS2401" has not been updated
#      | field_name | value          |
#      | hOut       | <outcome_code> |
#    And "Case 12345 for questionnaire FRS2401 has not been updated in Blaise (Blaise hOut=<blaise_outcome_code>, TM hOut=<outcome_code>)" is logged as an information message
#    And a "200 OK" response is sent back to Totalmobile
#    Examples: Blaise outcome code is 0
#      | blaise_outcome_code | outcome_code |
#      | 110                   | 730          |
#      | 110                   | 740          |
#      | 110                   | 750          |
#      | 110                   | 760          |
#      | 110                   | 771          |
#      | 110                   | 772          |
#      | 110                   | 773          |
#      | 110                   | 781          |
#      | 110                   | 782          |
#      | 110                   | 783          |
#      | 110                   | 790          |
#      | 110                   | 611          |
#      | 110                   | 612          |
#      | 110                   | 630          |
#      | 110                   | 641          |
#      | 110                   | 642          |
#      | 110                   | 651          |
#      | 110                   | 652          |
#      | 110                   | 670          |
#      | 110                   | 620          |
#      | 110                   | 512          |
#      | 110                   | 522          |
#      | 110                   | 532          |
#      | 110                   | 542          |
#      | 110                   | 310          |
#      | 110                   | 320          |
#      | 110                   | 330          |
#      | 210                   | 730          |
#      | 210                   | 740          |
#      | 210                   | 750          |
#      | 210                   | 760          |
#      | 210                   | 771          |
#      | 210                   | 772          |
#      | 210                   | 773          |
#      | 210                   | 781          |
#      | 210                   | 782          |
#      | 210                   | 783          |
#      | 210                   | 790          |
#      | 210                   | 611          |
#      | 210                   | 612          |
#      | 210                   | 630          |
#      | 210                   | 641          |
#      | 210                   | 642          |
#      | 210                   | 651          |
#      | 210                   | 652          |
#      | 210                   | 670          |
#      | 210                   | 620          |
#      | 210                   | 512          |
#      | 210                   | 522          |
#      | 210                   | 532          |
#      | 210                   | 542          |
#      | 210                   | 310          |
#      | 210                   | 320          |
#      | 210                   | 330          |
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
