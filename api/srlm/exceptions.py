class QueryEmpty(Exception):
    def __init__(self, errors):
        super().__init__("Query returned empty")

        self.errors = errors


class ActionFailed(Exception):
    def __init__(self, message, errors):
        message = message + ' ' + ' | '.join(errors)
        super().__init__(message)

        self.error = message
