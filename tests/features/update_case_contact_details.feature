Feature: Update contact details

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
      | DMktnIND        | 1            |
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