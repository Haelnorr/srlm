"""Functions for returning standardized success responses"""

from flask import url_for
from werkzeug.http import HTTP_STATUS_CODES


def create_success(message, api, **kwargs):
    payload = {
        'result': HTTP_STATUS_CODES.get(201),
        'message': message,
        'location': url_for(api, **kwargs)
    }
    return payload, 201


def request_success(message, api, **kwargs):
    payload = {
        'result': HTTP_STATUS_CODES.get(200),
        'message': message,
        'location': url_for(api, **kwargs)
    }
    return payload, 200
