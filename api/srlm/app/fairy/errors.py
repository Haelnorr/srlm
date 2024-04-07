import marshmallow as ma
from marshmallow import fields as fd


class BasicError(ma.Schema):
    error = fd.Str()
    message = fd.Str()


class ErrorNotFound(ma.Schema):
    error = fd.Str()
    message = fd.Str()
    resource = fd.Str()


bad_request = {
    400: BasicError()
}


auth_failed = {
    401: BasicError()
}


user_auth_failed = {
    403: BasicError()
}


not_found = {
    404: ErrorNotFound()
}
