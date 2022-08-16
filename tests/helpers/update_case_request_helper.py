
def get_populated_update_case_request(
    reference="LMS2101-AA1.90001"
):
    return {
            "Result": {
                "Responses": [
                    {
                        "Responses": [
                            {
                                "Value": "12345",
                                "Element": {
                                    "Reference": "TelNo",
                                },
                            }
                        ],
                    },
                ],
                "Association": {
                    "Reference": reference,
                },
            }
        }


def get_update_case_request_without_association_element(
):
    return {
            "Result": {
                "Responses": [
                    {
                        "Responses": [
                            {
                                "Value": "12345",
                                "Element": {
                                    "Reference": "TelNo",
                                },
                            }
                        ],
                    },
                ],
            }
        }


def get_update_case_request_without_reference_element(
):
    return {
            "Result": {
                "Responses": [
                    {
                        "Responses": [
                            {
                                "Value": "12345",
                                "Element": {
                                    "Reference": "TelNo",
                                },
                            }
                        ],
                    },
                ],
                "Association": {
                },
            }
        }