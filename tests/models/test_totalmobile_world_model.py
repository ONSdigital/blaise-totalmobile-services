from models.totalmobile_world_model import TotalmobileWorldModel, WorldId


def test_import_world_ids_returns_a_populated_model():
    world_ids = [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "identity": {
            "reference": "Region 1"
        },
        "type": "foo"
    },
    {
        "id": "8fa85f64-5717-4562-b3fc-2c963f66afa7",
        "identity": {
            "reference": "Region 2"
        },
        "type": "foo"
    },
]
    result = TotalmobileWorldModel.import_world_ids(world_ids)

    assert result.world_ids[0].region == "Region 1"
    assert result.world_ids[0].id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    assert result.world_ids[1].region == "Region 2"
    assert result.world_ids[1].id == "8fa85f64-5717-4562-b3fc-2c963f66afa7"


def test_get_world_id_returns_the_correct_id_for_region():
    totalmobile_world_model = TotalmobileWorldModel(
        world_ids=[WorldId(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
                   WorldId(region="Region 2", id="8fa85f64-5717-4562-b3fc-2c963f66afa7")]
    )

    result = totalmobile_world_model.get_world_id("Region 1")

    assert result == "3fa85f64-5717-4562-b3fc-2c963f66afa6"