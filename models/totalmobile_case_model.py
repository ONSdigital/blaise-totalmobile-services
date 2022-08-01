from dataclasses import dataclass

@dataclass
class TotalMobileCaseModel:
     location: AddressModel

@dataclass
class AddressModel:
    addressLine1: str
    addressLine2: str
    addressLine3: str    
