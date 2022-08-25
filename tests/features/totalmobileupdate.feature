Feature: Totalmobile update

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