Feature: Update call history

  Scenario Outline: Totalmobile sends a request with an outcome code of 460 (hard refusal) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 460   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=460)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 460 (hard refusal) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 460   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=460)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 461 (soft refusal) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 461   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=461)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 461 (soft refusal) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 461   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=461)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |


  Scenario Outline: Totalmobile sends a request with an outcome code of 510 (ineligible) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 510   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=510)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 510 (ineligible) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 510   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=510)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |


  Scenario Outline: Totalmobile sends a request with an outcome code of 540 (ineligible) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 540   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=540)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 540 (ineligible) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 540   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=540)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 551 (ineligible) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 551   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=551)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 551 (ineligible) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 551   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=551)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 560 (ineligible) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 560   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=560)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 560 (ineligible) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 560   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=560)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 580 (ineligible) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 580   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=580)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 580 (ineligible) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 580   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=580)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 640 (ineligible) when the case has no pre-existing call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has no pre-existing call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 640   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
      | catiMana.CatiCall.RegsCalls[5].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[5].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=640)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |

  Scenario Outline: Totalmobile sends a request with an outcome code of 640 (ineligible) when the case has call history
    Given there is a questionnaire "LMS2206_AA1" with case "12345" in Blaise
    And the case has an outcome code of <outcome_code>
    And the case has call history
    When Totalmobile sends an update for reference "LMS2206-AA1.12345"
      | field_name   | value |
      | outcome_code | 640   |
    Then the case "12345" for questionnaire "LMS2206_AA1" has been updated with call history
      | field_name                                | value |
      | catiMana.CatiCall.RegsCalls[1].WhoMade    | KTN   |
      | catiMana.CatiCall.RegsCalls[1].DialResult | 5     |
    And "Outcome code and call history updated (Questionnaire=LMS2206_AA1, Case Id=12345, Blaise hOut=<outcome_code>, TM hOut=640)" is logged as an information message
    And a "200 OK" response is sent back to Totalmobile
    Examples:
      | outcome_code |
      | 0            |
      | 310          |
      | 320          |