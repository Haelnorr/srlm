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


unauthorized = {
    401: BasicError()
}


forbidden = {
    403: BasicError()
}


not_found = {
    404: ErrorNotFound()
}
