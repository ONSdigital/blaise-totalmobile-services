from dataclasses import dataclass


@dataclass
class TotalmobileJobModel:
    instrument_name: str
    world_id: str
    case_data: dict
