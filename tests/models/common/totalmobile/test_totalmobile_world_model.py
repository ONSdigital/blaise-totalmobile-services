from models.common.totalmobile.totalmobile_world_model import (
    TotalmobileWorldModel,
    World,
)


def test_import_worlds_returns_a_populated_model_for_known_regions():
    # arrange
    worlds = [
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa0",
            "identity": {"reference": "default"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa1",
            "identity": {"reference": "Region 1"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa2",
            "identity": {"reference": "Region 2"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa3",
            "identity": {"reference": "Region 3"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa4",
            "identity": {"reference": "Region 4"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa5",
            "identity": {"reference": "Region 5"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {"reference": "Region 6"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa7",
            "identity": {"reference": "Region 7"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa8",
            "identity": {"reference": "Region 8"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa9",
            "identity": {"reference": "Region 9"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa10",
            "identity": {"reference": "Region 10"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa11",
            "identity": {"reference": "Region 11"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa12",
            "identity": {"reference": "Region 12"},
            "type": "foo",
        },
    ]

    # act
    result = TotalmobileWorldModel.import_worlds(worlds)

    # assert
    assert len(result.worlds) == 12
    assert result.worlds[0].region == "Region 1"
    assert result.worlds[0].id == "8fa85f64-5717-4562-b3fc-2c963f66afa1"

    assert result.worlds[1].region == "Region 2"
    assert result.worlds[1].id == "8fa85f64-5717-4562-b3fc-2c963f66afa2"

    assert result.worlds[2].region == "Region 3"
    assert result.worlds[2].id == "8fa85f64-5717-4562-b3fc-2c963f66afa3"

    assert result.worlds[3].region == "Region 4"
    assert result.worlds[3].id == "8fa85f64-5717-4562-b3fc-2c963f66afa4"

    assert result.worlds[4].region == "Region 5"
    assert result.worlds[4].id == "8fa85f64-5717-4562-b3fc-2c963f66afa5"

    assert result.worlds[5].region == "Region 6"
    assert result.worlds[5].id == "8fa85f64-5717-4562-b3fc-2c963f66afa6"

    assert result.worlds[6].region == "Region 7"
    assert result.worlds[6].id == "8fa85f64-5717-4562-b3fc-2c963f66afa7"

    assert result.worlds[7].region == "Region 8"
    assert result.worlds[7].id == "8fa85f64-5717-4562-b3fc-2c963f66afa8"

    assert result.worlds[8].region == "Region 9"
    assert result.worlds[8].id == "8fa85f64-5717-4562-b3fc-2c963f66afa9"

    assert result.worlds[9].region == "Region 10"
    assert result.worlds[9].id == "8fa85f64-5717-4562-b3fc-2c963f66afa10"

    assert result.worlds[10].region == "Region 11"
    assert result.worlds[10].id == "8fa85f64-5717-4562-b3fc-2c963f66afa11"

    assert result.worlds[11].region == "Region 12"
    assert result.worlds[11].id == "8fa85f64-5717-4562-b3fc-2c963f66afa12"

def test_import_worlds_filters_unknown_regions_and_only_returns_known_regions():
    # arrange
    worlds = [
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa11",
            "identity": {"reference": "Mordor"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa1",
            "identity": {"reference": "Region 1"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa22",
            "identity": {"reference": "The Shire"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa2",
            "identity": {"reference": "Region 2"},
            "type": "foo",
        },
    ]

    # act
    result = TotalmobileWorldModel.import_worlds(worlds)

    # assert
    assert len(result.worlds) == 2
    assert result.worlds[0].region == "Region 1"
    assert result.worlds[0].id == "8fa85f64-5717-4562-b3fc-2c963f66afa1"

    assert result.worlds[1].region == "Region 2"
    assert result.worlds[1].id == "8fa85f64-5717-4562-b3fc-2c963f66afa2"

def test_get_available_regions_returns_a_list_of_available_regions():

    # arrange & act
    result = TotalmobileWorldModel.get_available_regions()

    # assert
    assert result == [
        "Region 1",
        "Region 2",
        "Region 3",
        "Region 4",
        "Region 5",
        "Region 6",
        "Region 7",
        "Region 8",
        "Region 9",
        "Region 10",
        "Region 11",
        "Region 12",
    ]


def test_get_available_ids_returns_a_list_of_available_ids():
    # arrange
    totalmobile_world_model = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="8fa85f64-5717-4562-b3fc-2c963f66afa1"),
            World(region="Region 2", id="8fa85f64-5717-4562-b3fc-2c963f66afa2"),
            World(region="Region 3", id="8fa85f64-5717-4562-b3fc-2c963f66afa3"),
            World(region="Region 4", id="8fa85f64-5717-4562-b3fc-2c963f66afa4"),
            World(region="Region 5", id="8fa85f64-5717-4562-b3fc-2c963f66afa5"),
            World(region="Region 6", id="8fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 7", id="8fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="Region 8", id="8fa85f64-5717-4562-b3fc-2c963f66afa8"),
            World(region="Region 9", id="8fa85f64-5717-4562-b3fc-2c963f66afa9"),
            World(region="Region 10", id="8fa85f64-5717-4562-b3fc-2c963f66afa10"),
            World(region="Region 11", id="8fa85f64-5717-4562-b3fc-2c963f66afa11"),
            World(region="Region 12", id="8fa85f64-5717-4562-b3fc-2c963f66afa12"),
        ]
    )

    # act
    result = totalmobile_world_model.get_available_ids()

    # assert
    assert result == [
        "8fa85f64-5717-4562-b3fc-2c963f66afa1",
        "8fa85f64-5717-4562-b3fc-2c963f66afa2",
        "8fa85f64-5717-4562-b3fc-2c963f66afa3",
        "8fa85f64-5717-4562-b3fc-2c963f66afa4",
        "8fa85f64-5717-4562-b3fc-2c963f66afa5",
        "8fa85f64-5717-4562-b3fc-2c963f66afa6",
        "8fa85f64-5717-4562-b3fc-2c963f66afa7",
        "8fa85f64-5717-4562-b3fc-2c963f66afa8",
        "8fa85f64-5717-4562-b3fc-2c963f66afa9",
        "8fa85f64-5717-4562-b3fc-2c963f66afa10",
        "8fa85f64-5717-4562-b3fc-2c963f66afa11",
        "8fa85f64-5717-4562-b3fc-2c963f66afa12",
    ]


def test_get_world_id_returns_the_correct_id_for_region():
    totalmobile_world_model = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="8fa85f64-5717-4562-b3fc-2c963f66afa7"),
        ]
    )

    result = totalmobile_world_model.get_world_id("Region 1")

    assert result == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
