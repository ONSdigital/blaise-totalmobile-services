class FakeTotalmobileService:
    def __init__(self):
        self._jobs = {}

    def add_job(self, reference: str) -> None:
        self._jobs[reference] = {}

    def remove_job(self, reference: str) -> None:
        del self._jobs[reference]

    def job_exists(self, reference: str) -> bool:
        return reference in self._jobs
