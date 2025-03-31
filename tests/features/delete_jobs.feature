Feature: Delete jobs
  Background:
    Given the survey type is "LMS"

  Scenario Outline: Delete jobs from Totalmobile devices for cases in Blaise that no longer require a K2N
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is deleted
    And "completed in blaise" is provided as the reason for deleting job with reference "LMS2206-AA1.12345"
    And "Successfully removed job LMS2206-AA1.12345 from Totalmobile" is logged as an information message
    
    Examples: HOuts in Blaise that WILL trigger a delete request
      |outcome_code|
      |110         |
      |210         |
      |300         |    
      |360         |    
      |370         |    
      |371         |    
      |372         |    
      |380         |    
      |390         |    
      |411         |    
      |412         |    
      |413         |    
      |430         |    
      |440         |    
      |460         |    
      |461         |    
      |510         |    
      |540         |    
      |541         |    
      |542         |    
      |551         |    
      |560         |    
      |561         |    
      |562         |    
      |580         |    
      |631         |    
      |640         |    
      |791         |    
      |792         |    
      |793         |    
      |794         |    
      |795         |   

  Scenario Outline: Do not delete jobs from Totalmobile devices for cases in Blaise that still require a K2N
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is not deleted
    
    Examples: HOuts in Blaise that WILL NOT trigger a delete request
      |outcome_code|
      |0           | 
      |120         |
      |310         |
      |320         |

  Scenario Outline: Delete jobs from Totalmobile devices for cases in Blaise that have an unknown outcome code
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is deleted
    And "completed in blaise" is provided as the reason for deleting job with reference "LMS2206-AA1.12345"
    And "Successfully removed job LMS2206-AA1.12345 from Totalmobile" is logged as an information message

    Examples: HOuts which do not exist in Blaise that WILL trigger a delete request
      |outcome_code|
      |1           |
      |123         |
      |666         |

    Scenario Outline: Delete jobs from Totalmobile devices for cases in Blaise that do not require a K2N for all regions
      Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
      And the case has an outcome code of 110
      And there is an incomplete job in Totalmobile in region <region> with reference "LMS2206-AA1.12345"
      When delete_totalmobile_jobs_completed_in_blaise is run
      Then the Totalmobile job with reference "LMS2206-AA1.12345" is deleted
      And "completed in blaise" is provided as the reason for deleting job with reference "LMS2206-AA1.12345"
      And "Successfully removed job LMS2206-AA1.12345 from Totalmobile" is logged as an information message

      Examples:
      |region  |
      |Region 1|
      |Region 2|
      |Region 3|
      |Region 4|
      |Region 5|
      |Region 6|
      |Region 7|
      |Region 8|
      |Region 9|
      |Region 10|

  Scenario Outline: Do not delete jobs from Totalmobile devices for cases in Blaise that require a K2N for all regions
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of 310
    And there is an incomplete job in Totalmobile in region <region> with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is not deleted

    Examples:
    |region  |
    |Region 1|
    |Region 2|
    |Region 3|
    |Region 4|
    |Region 5|
    |Region 6|
    |Region 7|
    |Region 8|
    |Region 9|
    |Region 10|

  Scenario Outline: Do not delete jobs from Totalmobile devices for cases in Blaise that require a K2N for other regions
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of 110
    And there is an incomplete job in Totalmobile in region <region> with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is not deleted

    Examples:
    |region  |
    |Region 0|
    |Region 13|

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
    And the Blaise service errors when retrieving cases
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then "Unable to retrieve cases from Blaise for questionnaire LMS2206_AA1" is logged as an error message

  Scenario: Fails to find matching case
    Given there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    And case "12345" for questionnaire "LMS2206_AA1" does not exist in Blaise
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then "Unable to find case 12345 for questionnaire LMS2206_AA1 in Blaise" is logged as an error message

  Scenario: Fails to delete Totalmobile job
    Given case "12345" for questionnaire "LMS2206_AA1" has been completed
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    And the Totalmobile service errors when deleting jobs
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then "Unable to delete job reference 'LMS2206-AA1.12345` from Totalmobile" is logged as an error message

  Scenario: Incomplete Totalmobile jobs within 3 days of due date are deleted
    Given there is an incomplete job in Totalmobile with reference "LMS2209-AA1.12345"
    And job reference "LMS2209-AA1.12345" has a dueDate that ends in 3 days
    When delete_totalmobile_jobs_past_field_period is run
    Then the Totalmobile job with reference "LMS2209-AA1.12345" is deleted
    And "past field period" is provided as the reason for deleting job with reference "LMS2209-AA1.12345"

  Scenario: Incomplete Totalmobile jobs more than 3 days of due date are not deleted
    Given there is an incomplete job in Totalmobile with reference "LMS2209-AA1.12345"
    And job reference "LMS2209-AA1.12345" has a dueDate that ends in 4 days
    When delete_totalmobile_jobs_past_field_period is run
    Then the Totalmobile job with reference "LMS2209-AA1.12345" is not deleted

  Scenario: Recall jobs from Totalmobile devices for cases assigned cases due to be deleted
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has a complete outcome code
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345" assigned to "richmond.rice"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is recalled from "richmond.rice"

  Scenario: Incomplete Totalmobile jobs within 3 days of due date are recalled
    Given there is an incomplete job in Totalmobile with reference "LMS2209-AA1.12345" assigned to "richmond.rice"
    And job reference "LMS2209-AA1.12345" has a dueDate that ends in 3 days
    When delete_totalmobile_jobs_past_field_period is run
    Then the Totalmobile job with reference "LMS2209-AA1.12345" is recalled from "richmond.rice"

