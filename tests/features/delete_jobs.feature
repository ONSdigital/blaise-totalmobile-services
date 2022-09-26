Feature: Delete jobs

  Scenario Outline: Delete jobs from Totalmobile devices for cases in Blaise that no longer require a K2N
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And there is an incomplete job in Totalmobile with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" is deleted
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
      Then the Totalmobile job with reference "LMS2206-AA1.12345" in world <world_id> is deleted
      And "Successfully removed job LMS2206-AA1.12345 from Totalmobile" is logged as an information message

      Examples:
      |region  |world_id  |
      |Region 1|world-id-1|
      |Region 2|world-id-2|
      |Region 3|world-id-3|
      |Region 4|world-id-4|
      |Region 5|world-id-5|
      |Region 6|world-id-6|
      |Region 7|world-id-7|
      |Region 8|world-id-8|

  Scenario Outline: Do not delete jobs from Totalmobile devices for cases in Blaise that require a K2N for all regions
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of 310
    And there is an incomplete job in Totalmobile in region <region> with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" in world <world_id> is not deleted

    Examples:
    |region  |world_id  |
    |Region 1|world-id-1|
    |Region 2|world-id-2|
    |Region 3|world-id-3|
    |Region 4|world-id-4|
    |Region 5|world-id-5|
    |Region 6|world-id-6|
    |Region 7|world-id-7|
    |Region 8|world-id-8|

 Scenario Outline: Do not delete jobs from Totalmobile devices for cases in Blaise that require a K2N for other regions
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of 110
    And there is an incomplete job in Totalmobile in region <region> with reference "LMS2206-AA1.12345"
    When delete_totalmobile_jobs_completed_in_blaise is run
    Then the Totalmobile job with reference "LMS2206-AA1.12345" in world <world_id> is not deleted

    Examples:
    |region  |world_id  |
    |Region 0|world-id-0|
    |Region 9|world-id-9|

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