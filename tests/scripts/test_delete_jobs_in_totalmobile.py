from delete_jobs_in_totalmobile import delete_all_totalmobile_jobs_in_active_worlds
from unittest import mock


@mock.patch("services.totalmobile_service.delete_jobs")
@mock.patch("services.totalmobile_service.get_jobs")
@mock.patch("services.totalmobile_service.get_worlds")
def test_delete_all_totalmobile_jobs_in_active_worlds(
        mock_get_worlds,
        mock_get_jobs,
        mock_delete_jobs,
):
    mock_get_worlds.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7")
        ],
    )

    mock_get_jobs.return_value = {

    }
