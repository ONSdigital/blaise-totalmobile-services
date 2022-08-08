from dataclasses import dataclass
from typing import List, TypeVar, Type

T = TypeVar('T')


@dataclass
class World:
    region: str
    id: str


@dataclass
class TotalmobileWorldModel:
    worlds: List[World]

    def get_world_id(self, region: str):
        for world in self.worlds:
            if world.region == region:
                return world.id
        return None

    def get_regions(self) -> List[str]:
        return [world.region for world in self.worlds]

    @classmethod
    def import_worlds(cls: Type[T], world_dictionary: dict[str, str]) -> T:
        return TotalmobileWorldModel(
            [World(region=world_dictionary_item["identity"]["reference"], id=world_dictionary_item["id"]) for world_dictionary_item in world_dictionary])



