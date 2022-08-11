Feature: Totalmobile update
    Scenario: Match a totalmobile update with data in blaise
        Given there is a questionnaire "LMS2206-AA1" with case "12345"
        When Totalmobile sends an update for reference "LMS2206-AA1.12345"
        Then "Successfully found questionnaire LMS2206-AA1 in Blaise" is logged as an information message
        And "Successfully found case 12345 for questionnaire LMS2206-AA1 in Blaise" is logged as an information message
        And a "200 OK" response is sent back to Totalmobile

    Scenario: Reference is not matched with a questionnaire in Blaise
        Given there is no questionnaire in Blaise for reference "LMS2206-AA1"
        When Totalmobile sends an update for reference "LMS2206-AA1.12345"
        Then "Could not find questionnaire LMS2206-AA1 in Blaise" is logged as an error message
        And a "404 Not Found" response is sent back to Totalmobile

    # Scenario: Reference is not matched with a case in Blaise
    #     Given there is no case in Blaise for reference "12345"
    #     When Totalmobile sends an update for reference "LMS2206-AA1.12345"
    #     Then "Could not find case 12345 for questionnaire LMS2206_AA1 in Blaise" is logged as an error message

    Scenario: Reference is missing
        When Totalmobile sends an update with missing reference
        Then "Unique reference is missing from totalmobile payload" is logged as an error message
        And a "400 Bad Request" response is sent back to Totalmobile