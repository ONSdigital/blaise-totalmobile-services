Feature: Update case

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

  Scenario: Error in retrieving case in Blaise
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    But the Blaise service errors when retrieving case
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
    Then "There was an error retrieving case 12345 for questionnaire LMS2206_AA1 in Blaise" is logged as an error message
    And a "500 Internal Server Error" response is sent back to Totalmobile

  Scenario: Reference is missing
    When Totalmobile sends an update with a missing reference
    Then "Unique reference is missing from the Totalmobile payload" is logged as an error message
    And a "400 Bad Request" response is sent back to Totalmobile

  Scenario Outline: Reference is in the incorrect format
    When Totalmobile sends an update with a malformed reference <reference>
    Then "Unique reference appeared to be malformed in the Totalmobile payload (reference='<reference>')" is logged as an error message
    And a "400 Bad Request" response is sent back to Totalmobile
    Examples:
      | reference         |
      | LMS2101_AA1-90001 |
      | LMS2101_AA1:90001 |
      | LMS2101_AA1.      |
      | .90001            |

  Scenario: Payload appears to be malformed
    When Totalmobile sends an update with a malformed payload
    Then "The Totalmobile payload appears to be malformed" is logged as an error message
    And a "400 Bad Request" response is sent back to Totalmobile

