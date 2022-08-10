Feature: Totalmobile update
    Scenario: Match a totalmobile update with data in blaise
        Given there is a questionnaire "LMS2206-AA1" with case "12345"
        When Totalmobile sends an update for reference "LMS2206-AA1.12345"
        Then "Successfully found questionnaire LMS2206-AA1 in Blaise" is logged as an information message
        And "Successfully found case 12345 for questionnaire LMS2206-AA1 in Blaise" is logged as an information message