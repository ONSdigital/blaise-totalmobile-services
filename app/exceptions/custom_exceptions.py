class QuestionnaireDoesNotExistError(Exception):
    pass


class QuestionnaireCaseError(Exception):
    pass


class QuestionnaireCaseDoesNotExistError(Exception):
    pass


class MissingReferenceError(Exception):
    pass


class BadReferenceError(Exception):
    pass


class InvalidTotalmobileUpdateRequestException(Exception):
    pass


class InvalidTotalmobileFRSRequestException(Exception):
    pass


class CaseReAllocationException(Exception):
    pass


class SpecialInstructionCreationFailedException(Exception):
    pass


class CaseNotFoundException(Exception):
    pass


class CaseResetFailedException(Exception):
    pass


class CaseAllocationException(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self._format_message())

    def _format_message(self):
        if self.message:
            return self.message
        return ""

    def __str__(self):
        return self._format_message()
