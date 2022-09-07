class FakeTotalmobileService:
    def __init__(self):
        self._jobs = {}

    def add_job(self, reference: str) -> None:
        self._jobs[reference] = {}

    def remove_job(self, reference: str) -> None:
        self._assert_job_exists(reference)
        del self._jobs[reference]

    def job_exists(self, reference: str) -> bool:
        return reference in self._jobs

    def _assert_job_exists(self, reference: str) -> bool:
        if not self.job_exists(reference):
            raise _JobDoesNotExistError(
                f"Job '{reference}' does not exist"
            )


class _JobDoesNotExistError(Exception):
    pass
