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

class CaseAllocationException(Exception):
    pass

class CaseReAllocationException(Exception):
    pass

class SpecialInstructionCreationFailedException(Exception):
    pass
