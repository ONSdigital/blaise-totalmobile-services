from dataclasses import dataclass

@dataclass
class TotalMobileCaseModel:
     location: AddressModel

@dataclass
class AddressModel:
    addressLine1: str
    addressLine2: str
    addressLine3: str    


    def populate_questionnaire_case_data(cls, QuestionnaireCaseModel) -> bool:
        cls.location.addressLine1 = QuestionnaireCaseModel.address_line_1