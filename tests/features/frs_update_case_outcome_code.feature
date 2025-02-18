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

  Scenario Outline: Totalmobile sends a request with an outcome code of 461 (soft refusal) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 461   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 461   |
      | qhAdmin.HOut | 461   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=461)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 510 (Ineligible) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 510   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 510   |
      | qhAdmin.HOut | 510   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=510)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 540 (Ineligible) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 540   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 540   |
      | qhAdmin.HOut | 540   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=540)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 551 (Ineligible) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 551   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 551   |
      | qhAdmin.HOut | 551   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=551)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 560 (Ineligible) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 560   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 560   |
      | qhAdmin.HOut | 560   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=560)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 580 (Ineligible) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 580   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 580   |
      | qhAdmin.HOut | 580   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=580)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 640 (Ineligible) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 640   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 640   |
      | qhAdmin.HOut | 640   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=640)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |
