"""Useful functions for interfacing with the database"""

from datetime import datetime
from api.srlm.app import db
from api.srlm.app.api.utils.errors import BadRequest, ResourceNotFound, FieldBadRequest


def ensure_exists(model, return_none=False, join_method='and', **kwargs):
    query = None
    if join_method == 'and':
        fail_message = f'{model.__name__} with {kwargs}'
        query = db.session.query(model).filter_by(**kwargs).first()
    elif join_method == 'or':
        fail_message = f"{model.__name__} identified by '{next(iter(kwargs.values()))}'"
        for key in kwargs:
            query = db.session.query(model).filter_by(**{key: kwargs[key]}).first()
            if query:
                break
    else:
        raise ValueError("'join_method' must be 'and' or 'or'")

    if not return_none and not query:
        raise ResourceNotFound(fail_message)
    else:
        return query


def force_fields(data, required_fields):
    missing = []
    for field in required_fields:
        if field not in data:
            missing.append(field)

    if len(missing) > 0:
        raise BadRequest(f"Required fields are missing: {missing}")


def force_unique(model, data, unique_fields, self_id=0, restrict_query=None):
    not_unique = []
    for key, value in data.items():
        if key in unique_fields:
            if restrict_query:
                query = db.session.query(model).filter_by(
                    **{key: value},
                    **restrict_query
                ).filter(model.id != self_id)
            else:
                query = db.session.query(model).filter_by(**{key: value}).filter(model.id != self_id)
            exists = db.session.query(query.exists()).scalar()
            if exists:
                not_unique.append(key)

    if len(not_unique) > 0:
        message = f'Some fields that must be unique are not: {not_unique}'
        if restrict_query:
            key = next(iter(restrict_query))
            value = restrict_query[key]
            message = message + f' (matches another record with {key}={value})'
        field_errors = []
        for field in not_unique:
            error = {
                'field': field,
                'error': 'Must be unique'
            }
            field_errors.append(error)
        raise FieldBadRequest(message, field_errors)


def force_date_format(data, valid_fields):
    date_format = "%Y-%m-%d"
    bad_fields = []
    for date_input in data:
        if date_input in valid_fields:
            try:
                datetime.strptime(data[date_input], date_format)
            except ValueError:
                bad_fields.append(date_input)
    if bad_fields:
        raise BadRequest(f'Date fields are in the wrong format. Should be YYYY-MM-DD. Fields: {bad_fields}')


def clean_data(data, valid_fields):
    cleaned = {}
    for key, value in data.items():
        if key in valid_fields:
            cleaned[key] = value

    if len(cleaned) == 0:
        raise BadRequest(f'No valid fields provided. Provide at least one of: {valid_fields}')
    return cleaned
