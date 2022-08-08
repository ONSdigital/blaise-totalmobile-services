from dataclasses import dataclass
from typing import List, TypeVar, Type

T = TypeVar('T')


@dataclass
class WorldId:
    region: str
    id: str


@dataclass
class TotalmobileWorldModel:
    world_ids: List[WorldId]

    @classmethod
    def import_world_ids(cls: Type[T], world_id_dictionary: dict[str, str]) -> T:
        return TotalmobileWorldModel(
            [WorldId(region=world_id_dictionary_item["identity"]["reference"], id=world_id_dictionary_item["id"]) for world_id_dictionary_item in world_id_dictionary])

    def get_world_id(self, region: str):
        for world_id in self.world_ids:
            if world_id.region == region:
                return world_id.id
        return None

