Feature: Totalmobile delete jobs

  Scenario: A respondent completes a case online
    Given a respondent has completed case "12345" online for questionnaire "LMS2206_AA1"
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete jobs is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is deleted
    And "Successfully removed job LMS2206-AA1.12345 from Totalmobile" is logged as an information message

  Scenario: A case in Blaise that has not been started
    Given a case "12345" has not been started for questionnaire "LMS2206_AA1"
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete jobs is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is not deleted
