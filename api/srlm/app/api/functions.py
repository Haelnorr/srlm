from api.srlm.app import db
from api.srlm.app.api.errors import BadRequest, ResourceNotFound
import sqlalchemy as sa


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


def force_unique(model, data, unique_fields, restrict_query=None):
    not_unique = []
    for key, value in data.items():
        if key in unique_fields:
            if restrict_query:
                query = db.session.query(model).filter_by(
                    **{key: value},
                    **restrict_query
                )
            else:
                query = db.session.query(model).filter_by(**{key: value})
            exists = db.session.query(query.exists()).scalar()
            if exists:
                not_unique.append(key)

    if len(not_unique) > 0:
        message = f'Some fields that must be unique are not: {not_unique}'
        if restrict_query:
            key = next(iter(restrict_query))
            value = restrict_query[key]
            message = message + f' (matches another record with {key}={value})'
        raise BadRequest(message)


def clean_data(data, valid_fields):
    cleaned = {}
    for key, value in data.items():
        if key in valid_fields:
            cleaned[key] = value

    if len(cleaned) is 0:
        raise BadRequest(f'No valid fields provided. Provide at least one of: {valid_fields}')
    return cleaned
