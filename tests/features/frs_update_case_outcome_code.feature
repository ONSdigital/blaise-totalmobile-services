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
    Examples: Blaise outcome code is 310
      | blaise_outcome_code | outcome_code |
      | 310                 | 730          |
      | 310                 | 740          |
      | 310                 | 750          |
      | 310                 | 760          |
      | 310                 | 771          |
      | 310                 | 772          |
      | 310                 | 773          |
      | 310                 | 781          |
      | 310                 | 782          |
      | 310                 | 783          |
      | 310                 | 790          |
      | 310                 | 611          |
      | 310                 | 612          |
      | 310                 | 630          |
      | 310                 | 641          |
      | 310                 | 642          |
      | 310                 | 651          |
      | 310                 | 652          |
      | 310                 | 670          |
      | 310                 | 620          |
      | 310                 | 512          |
      | 310                 | 522          |
      | 310                 | 532          |
      | 310                 | 542          |
      | 310                 | 310          |
      | 310                 | 320          |
      | 310                 | 330          |
    Examples: Blaise outcome code is 320
      | blaise_outcome_code | outcome_code |
      | 320                 | 730          |
      | 320                 | 740          |
      | 320                 | 750          |
      | 320                 | 760          |
      | 320                 | 771          |
      | 320                 | 772          |
      | 320                 | 773          |
      | 320                 | 781          |
      | 320                 | 782          |
      | 320                 | 783          |
      | 320                 | 790          |
      | 320                 | 611          |
      | 320                 | 612          |
      | 320                 | 630          |
      | 320                 | 641          |
      | 320                 | 642          |
      | 320                 | 651          |
      | 320                 | 652          |
      | 320                 | 670          |
      | 320                 | 620          |
      | 320                 | 512          |
      | 320                 | 522          |
      | 320                 | 532          |
      | 320                 | 542          |
      | 320                 | 310          |
      | 320                 | 320          |
      | 320                 | 330          |
    Examples: Blaise outcome code is 330
      | blaise_outcome_code | outcome_code |
      | 330                 | 730          |
      | 330                 | 740          |
      | 330                 | 750          |
      | 330                 | 760          |
      | 330                 | 771          |
      | 330                 | 772          |
      | 330                 | 773          |
      | 330                 | 781          |
      | 330                 | 782          |
      | 330                 | 783          |
      | 330                 | 790          |
      | 330                 | 611          |
      | 330                 | 612          |
      | 330                 | 630          |
      | 330                 | 641          |
      | 330                 | 642          |
      | 330                 | 651          |
      | 330                 | 652          |
      | 330                 | 670          |
      | 330                 | 620          |
      | 330                 | 512          |
      | 330                 | 522          |
      | 330                 | 532          |
      | 330                 | 542          |
      | 330                 | 310          |
      | 330                 | 320          |
      | 330                 | 330          |

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
#      | RefReas    | <outcome_code> |
    And "Outcome code and refusal reason updated (Questionnaire=FRS2401, Case Id=12345, Blaise hOut=<blaise_outcome_code>, Blaise RefReas=<outcome_code>)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples: Blaise outcome code is 0
      | blaise_outcome_code | outcome_code |
      | 0                   | 410          |
#      | 0                   | 420          |
#      | 0                   | 431          |
#      | 0                   | 432          |
#      | 0                   | 441          |
#      | 0                   | 442          |
#      | 0                   | 450          |
#    Examples: Blaise outcome code is 310
#      | blaise_outcome_code | outcome_code |
#      | 310                 | 410          |
#      | 310                 | 420          |
#      | 310                 | 431          |
#      | 310                 | 432          |
#      | 310                 | 441          |
#      | 310                 | 442          |
#      | 310                 | 450          |
#    Examples: Blaise outcome code is 320
#      | blaise_outcome_code | outcome_code |
#      | 320                 | 410          |
#      | 320                 | 420          |
#      | 320                 | 431          |
#      | 320                 | 432          |
#      | 320                 | 441          |
#      | 320                 | 442          |
#      | 320                 | 450          |
#    Examples: Blaise outcome code is 330
#      | blaise_outcome_code | outcome_code |
#      | 330                 | 410          |
#      | 330                 | 420          |
#      | 330                 | 431          |
#      | 330                 | 432          |
#      | 330                 | 441          |
#      | 330                 | 442          |
#      | 330                 | 450          |