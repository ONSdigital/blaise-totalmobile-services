from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World


def test_import_worlds_returns_a_populated_model():
    worlds = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {"reference": "Region 1"},
            "type": "foo",
        },
        {
            "id": "8fa85f64-5717-4562-b3fc-2c963f66afa7",
            "identity": {"reference": "Region 2"},
            "type": "foo",
        },
    ]
    result = TotalmobileWorldModel.import_worlds(worlds)

    assert result.worlds[0].region == "Region 1"
    assert result.worlds[0].id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    assert result.worlds[1].region == "Region 2"
    assert result.worlds[1].id == "8fa85f64-5717-4562-b3fc-2c963f66afa7"


def test_get_available_regions_returns_a_list_of_available_regions():
    totalmobile_world_model = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="8fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="Region 3", id="4fa85f64-5717-4562-b3fc-2c963f66afa8"),
            World(region="Region 4", id="2fa85f64-5717-4562-b3fc-2c963f66afa9"),
            World(region="Region 5", id="7fa85f64-5717-4562-b3fc-2c963f66afa2"),
        ]
    )

    result = totalmobile_world_model.get_available_regions()

    assert result == ["Region 1", "Region 2", "Region 3", "Region 4", "Region 5"]


def test_get_available_ids_returns_a_list_of_available_ids():
    totalmobile_world_model = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="8fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="Region 3", id="4fa85f64-5717-4562-b3fc-2c963f66afa8"),
            World(region="Region 4", id="2fa85f64-5717-4562-b3fc-2c963f66afa9"),
            World(region="Region 5", id="7fa85f64-5717-4562-b3fc-2c963f66afa2"),
        ]
    )

    result = totalmobile_world_model.get_available_ids()

    assert result == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "8fa85f64-5717-4562-b3fc-2c963f66afa7",
        "4fa85f64-5717-4562-b3fc-2c963f66afa8",
        "2fa85f64-5717-4562-b3fc-2c963f66afa9",
        "7fa85f64-5717-4562-b3fc-2c963f66afa2",
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
