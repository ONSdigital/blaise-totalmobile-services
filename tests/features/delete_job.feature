Feature: Delete job

  Scenario: A case in Blaise has been completed
    Given case "12345" for questionnaire "LMS2206_AA1" has been completed
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is deleted
    And "Successfully removed job LMS2206-AA1.12345 from Totalmobile" is logged as an information message

  Scenario: A case in Blaise has not been completed
    Given case "12345" for questionnaire "LMS2206_AA1" has not been completed
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is not deleted
