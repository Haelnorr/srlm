"""Provides marshmallow schemas for documentation support"""
from api.srlm.app import ma
from api.srlm.app.models import Permission


class Links(ma.Schema):
    self = ma.URL()


class PaginationArgs(ma.Schema):
    """Schema for defining pagination args"""
    page = ma.Int(missing=1)
    per_page = ma.Int(missing=10)
    total_pages = ma.Int(dump_only=True)
    total_items = ma.Int(dump_only=True)


class PaginationLinks(Links):
    next = ma.URL()
    prev = ma.URL()


class FilterSchema(ma.Schema):
    """Schema for defining filter arg"""
    f = ma.Str()


class BasicAuthSchema(ma.Schema):
    """Schema for defining the basic user auth login"""
    username = ma.Str(required=True)
    password = ma.Str(required=True)


class TokenSchema(ma.Schema):
    """Schema for defining Token responses"""
    token = ma.Str()
    expires = ma.DateTime()


class BasicSuccessSchema(ma.Schema):
    """Schema for defining basic success responses"""
    result = ma.Str()
    message = ma.Str()


class LinkSuccessSchema(BasicSuccessSchema):
    """Schema for defining success responses with a resource link provided"""
    location = ma.URL()


class UserVerifySchema(ma.Schema):
    """Schema for defining the response for verifying a user token"""
    class VerifyLinks(ma.Schema):
        user = ma.URL()

    user = ma.Int()
    expires = ma.DateTime()
    _links = ma.Nested(VerifyLinks())


class PermissionSchema(ma.SQLAlchemySchema):
    """Schema for defining the structure of Permissions requests"""
    class Meta:
        model = Permission
        ordered = True

    id = ma.auto_field(dump_only=True)
    key = ma.auto_field(required=True)
    description = ma.auto_field()
    users_count = ma.Int(dump_only=True)
    _links = ma.Nested(Links(), dump_only=True)


class PermissionCollection(ma.Schema):
    items = ma.List(ma.Nested(PermissionSchema()))
    _meta = ma.Nested(PaginationArgs())
    _links = ma.Nested(PaginationLinks())


class UpdatePermissionSchema(PermissionSchema):
    """Extends the PermissionSchema making the `key` field optional"""
    key = ma.auto_field(required=False)


class PermUsersSchema(ma.Schema):
    """Schema for defining the response listing users with a given permission"""

    class UsersWithPerm(ma.Schema):
        id = ma.Int()
        username = ma.String()
        _links = ma.Nested(Links())

    permission = ma.String()
    key = ma.String()
    users = ma.Nested(UsersWithPerm())
    _links = ma.Nested(Links())


