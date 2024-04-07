"""The API has a two key system for authorization. An app key required for all requests, and a user key required for
requests that are sensitive to user authentication (i.e. changing account details).
The key is sent in the request header as a Bearer token.
<pre>
Authorization: Bearer AUTH_TOKEN
</pre>
The app key is require for all requests (except for authenticating user details and getting the user key).
App keys are currently provided by the developer manually and expire after 3 months.
A valid app key can be used to generate a new key, replacing the old one and resetting the expiry.

The user key is used to authenticate a specific user, and can be retreived by using the API request below.
For requests requiring a user key, append it directly to the app key when making your request. Total key length
should be 66 characters.
"""
from flask import Blueprint
from api.srlm.app.api import bp

auth_bp = Blueprint('auth', __name__)
bp.register_blueprint(auth_bp, url_prefix='/auth')

from api.srlm.app.api.auth import routes, utils, permissions
