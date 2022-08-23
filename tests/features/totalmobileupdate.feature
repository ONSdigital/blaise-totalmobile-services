Feature: Totalmobile update

  Scenario Outline: Totalmobile sends a request with an outcome code of 300 when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name          | value        |
      | outcome_code        | 300          |
      | contact_name        | Tom Barnes   |
      | home_phone_number   | 02920 778822 |
      | mobile_phone_number | 07898 888222 |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with
      | field_name      | value        |
      | dMktnName       | Tom Barnes   |
      | qDataBag.TelNo  | 02920 778822 |
      | qDataBag.TelNo2 | 07898 888222 |
    And "Contact information updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=300)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with no contact details when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345" with an outcome of 300 but no contact information
    Then the case "12345" for questionnaire "LMS2206_AA1" has not been updated
    And "Contact information has not been updated as no contact information was provided (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=300)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 300 when case has outcome code of <outcome_code>
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 300   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has not been updated
    And "Case 12345 for questionnaire LMS2206_AA1 has not been updated in Blaise (Blaise hOut=<outcome_code>, TM hOut=300)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 110          |
      | 210          |
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
      | field_name | value |
      | hOut       | 460   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=460)" is logged as an information message
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
      | field_name | value |
      | hOut       | 461   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=461)" is logged as an information message
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
      | field_name | value |
      | hOut       | 510   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=510)" is logged as an information message
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
      | field_name | value |
      | hOut       | 540   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=540)" is logged as an information message
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
      | field_name | value |
      | hOut       | 551   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=551)" is logged as an information message
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
      | field_name | value |
      | hOut       | 560   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=560)" is logged as an information message
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
      | field_name | value |
      | hOut       | 580   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=580)" is logged as an information message
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
      | field_name | value |
      | hOut       | 640   |
    And "Outcome code updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=640)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario: Questionnaire and case is found in Blaise
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
    Then "Successfully found questionnaire LMS2206_AA1 in Blaise" is logged as an information message
    And "Successfully found case 12345 for questionnaire LMS2206_AA1 in Blaise" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile

  Scenario: Reference is not matched with a questionnaire in Blaise
    Given there is no questionnaire "LMS2206_AA1" in Blaise
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
    Then "Could not find questionnaire LMS2206_AA1 in Blaise" is logged as an error message
    And a "404 Not Found" response is sent back to Totalmobile

  Scenario: Reference is not matched with a case in Blaise
    Given there is a questionnaire "LMS2206_AA1" in Blaise
    But there is no case "12345" for questionnaire "LMS2206_AA1" in Blaise
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
    Then "Could not find case 12345 for questionnaire LMS2206_AA1 in Blaise" is logged as an error message
    And a "404 Not Found" response is sent back to Totalmobile

  Scenario: Reference is missing
    When Totalmobile sends an update with missing reference
    Then "Unique reference is missing from totalmobile payload" is logged as an error message
    And a "400 Bad Request" response is sent back to Totalmobile