Feature: update outcome code

  Scenario Outline: Totalmobile sends a request with an outcome code of 310 (non-contact) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 310   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has not been updated
    And "Case 12345 for questionnaire LMS2206_AA1 has not been updated in Blaise (Blaise hOut=<outcome_code>, TM hOut=310)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 110          |
      | 210          |
      | 310          |
      | 320          |
      | 430          |
      | 440          |
      | 460          |
      | 461          |
      | 541          |
      | 542          |
      | 561          |
      | 562          |
      | 580          |
      | 640          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 460 (hard refusal) when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 460   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name   | value |
      | hOut         | 460   |
      | qhAdmin.HOut | 460   |
      | DMktnIND     | 1     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=460)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

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
