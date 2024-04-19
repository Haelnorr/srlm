from api.srlm.app import ma


class BasicError(ma.Schema):
    error = ma.Str()
    message = ma.Str()


class ErrorNotFound(ma.Schema):
    error = ma.Str()
    message = ma.Str()
    resource = ma.Str()


class BadFieldRequest(BasicError):
    class Field(ma.Schema):
        field = ma.Str()
        error = ma.Str()
    fields = ma.List(ma.Nested(Field()))


bad_request = {
    400: BasicError(),
    409: BadFieldRequest()
}

unauthorized = {
    401: BasicError()
}


forbidden = {
    403: BasicError()
}


not_found = {
    404: ErrorNotFound()
}
