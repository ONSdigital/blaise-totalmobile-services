from dataclasses import dataclass
from typing import List, Optional, Type, TypeVar

from client.optimise import GetWorldsResponse

T = TypeVar("T", bound="TotalmobileWorldModel")


@dataclass
class World:
    region: str
    id: str


@dataclass
class TotalmobileWorldModel:
    worlds: List[World]

    _known_regions = [
        "Region 1",
        "Region 2",
        "Region 3",
        "Region 4",
        "Region 5",
        "Region 6",
        "Region 7",
        "Region 8",
    ]

    def get_world_id(self, region: Optional[str]):
        for world in self.worlds:
            if world.region == region:
                return world.id
        return None

    def get_available_ids(self) -> List[str]:
        return [world.id for world in self.worlds]

    @staticmethod
    def get_available_regions() -> List[str]:
        return TotalmobileWorldModel._known_regions

    @classmethod
    def import_worlds(cls: Type[T], world_dictionary: GetWorldsResponse) -> T:
        return cls(
            [
                World(
                    region=world_dictionary_item["identity"]["reference"],
                    id=world_dictionary_item["id"],
                )
                for world_dictionary_item in world_dictionary
                if world_dictionary_item["identity"]["reference"] in cls._known_regions
            ]
        )
