Feature: Delete jobs

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

  Scenario: Fails to get jobs from Totalmobile
    Given case "12345" for questionnaire "LMS2206_AA1" has been completed
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    And the Totalmobile service errors when retrieving jobs
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then "Unable to retrieve jobs from Totalmobile" is logged as an error message

  Scenario: Fails to get cases from Blaise
    Given case "12345" for questionnaire "LMS2206_AA1" has been completed
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    And the Blaise service is errors when retrieving cases
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then "Unable to retrieve cases from Blaise" is logged as an error message

  Scenario: Fails to find matching case
    Given there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    And case "12345" for questionnaire "LMS2206_AA1" does not exist in Blaise
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then "Unable to find case 12345 for questionnaire LMS2206_AA1 in Blaise" is logged as an error message

  Scenario: Fail to delete Totalmobile job
    Given case "12345" for questionnaire "LMS2206_AA1" has been completed
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    And the Totalmobile service errors when deleting jobs
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then "Unable to delete job reference 'LMS2206-AA1.12345` from Totalmobile" is logged as an error message