"""For handling errors and returning standardized error messages"""
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from api.srlm.app.api import bp


def error_response(status_code, message=None, missing_resource=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    if missing_resource:
        payload['missing_resource'] = missing_resource
    return payload, status_code


@bp.errorhandler(HTTPException)
def handle_exception(e):
    return error_response(e.code, e.description)


class BadRequest(HTTPException):
    code = 400

    def __init__(self, details):
        self.details = details


@bp.errorhandler(BadRequest)
def bad_request(e):
    return error_response(e.code, e.details)


class UserAuthError(HTTPException):
    code = 403


@bp.errorhandler(UserAuthError)
def handle_user_auth_error(e):
    return error_response(e.code, 'User is not authenticated or does not have access to this resource')


class AppAuthError(HTTPException):
    code = 401


@bp.errorhandler(AppAuthError)
def handle_app_auth_error(e):
    return error_response(e.code, 'Invalid or missing app token')


class ResourceNotFound(HTTPException):
    code = 404

    def __init__(self, missing_resource):
        self.missing_resource = missing_resource


@bp.errorhandler(ResourceNotFound)
def handle_resource_not_found(e):
    return error_response(e.code, 'Requested resource cannot be found', e.missing_resource)
