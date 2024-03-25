<h2>Endpoints</h2>

<details>
<summary><b>Auth</b></summary>
The API has a two key system for authorization. An app key required for all requests, and a user key required for requests that are sensitive to user authentication (i.e. changing account details).  
The key is sent in the request header as a Bearer token.
<pre>
Authorization: Bearer AUTH_TOKEN
</pre>
The app key is require for all requests (except for authenticating user details and getting the user key). 
App keys are currently provided by the developer manually and expire after 3 months. 
(In future there will be a way to get a new app key through the API. It will replace your existing one and 
reset the expiry date)

The user key is used to authenticate a specific user, and can be retreived by using the API request below. 
For requests requiring a user key, append it directly to the app key when making your request. Total key length 
should be 66 characters. User key can be included for requests that do not require it as it will be ignored.

<details>
<summary>
POST /api/tokens/user
</summary>
Requests an auth token for a user, provided a valid username and password. Returns 401 error if unauthorized.<br>
Username:password should be submitted using a Basic Authorization header and DOES NOT require an app code<br>
Tokens expire after 23 hours unless otherwise specified.
Response:
<pre>{
    "token": "a3b67df3547a49e6cd338a05c442d666"
}</pre>
Error:
<pre>{
    "error": "Unauthorized"
}</pre>
</details>
<details>
<summary>
DELETE /api/tokens/user
</summary>
Revokes the auth token of the current user. <b>Requires user auth token</b><br>
Useful for logging a user out<br>
Successful operation will return <code>204 NO CONTENT</code>
</details>
<details>
<summary>
POST /api/tokens/user/validate
</summary>
Checks if a user auth token is still valid. <b>Requires user auth token</b><br>
Useful for checking if user is logged in. Returns <code>{"error": "Unauthorized"}</code> if token is not valid.<br>
<pre>{
    "_links": {
        "user": "/api/users/2"
    },
    "expires": "Tue, 26 Mar 2024 03:16:34 GMT",
    "user": 2
}
</pre>
</details>
<details>
<summary>
GET /api/tokens/app
</summary>
Gets the token and expiry date of the current app token.<br>
Since it requires a valid app token to access, 
and only gives details on that token, only really useful for getting the expiry date<br>
Response:
<pre>{
    "expiry": "Tue, 23 Apr 2024 23:02:17 GMT",
    "token": "4ded8ce3796b368e93c5f87d36a7def051"
}
</pre>
Error:
<pre>{
    "error": "Unauthorized"
}</pre>
</details>
<details>
<summary>
POST /api/tokens/app
</summary>
Requests a new app token and resets the expiry date.<br>
Requires a valid app token to access, 
and only gives works on the app that token is assigned to.<br>
Response:
<pre>{
    "expiry": "Tue, 23 Apr 2024 23:02:17 GMT",
    "token": "4ded8ce3796b368e93c5f87d36a7def051"
}
</pre>
Error:
<pre>{
    "error": "Unauthorized"
}</pre>
</details>
</details>
<br><details>
<summary><b>Users</b></summary>
<details>
    <summary>GET /api/users/{int:id}</summary>
    Gets the user data of a user specified by their user id. The list of permissions in this result returns the keys 
only. For a full list see <code>GET /api/users/{int:id}/permissions</code>
    <br>
    Example response: 
    <pre>
{
    "id": 1,
    "username": "Admin",
    "email": "admin@email.com", # only returned if the user requested their own data
    "player": 1,                # can be null
    "discord": 34234523452345,  # can be null
    "permissions": [
        "admin"
    ],
    "matches_streamed": 0,
    "matches_reviewed": 0,
    "reset_pass": false,
    "_links": {
        "self": "/api/users/1",
        "player": "/api/players/1",         # can be null
        "discord": "/api/users/1/discord",  # can be null
        "permissions": "/api/users/1/permissions",
        "matches_streamed": "/api/users/1/matches_streamed",
        "matches_reviewed": "/api/users/1/matches_reviewed",
    }
}</pre>
    User not found:
<pre>
{
  "error": "Not Found"
}</pre>
</details>
<details>
    <summary>GET /api/users?page=1&per_page=10</summary>
    Gets list of all users. <code>page</code> and <code>per_page</code> are optional with defaults 1 and 10. Max per page is 100
    <pre>
{
    "items": [
        { ... user resource ... },
        { ... user resource ... },
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_pages": 20,
        "total_items": 195
    },
    "_links:" {
        "self": ".../api/users?page=1",
        "next": ".../api/users?page=2",
        "prev": null
    }
}</pre>
</details>
<details>
<summary>POST /api/users</summary>
Creates a new user and returns the user in the same form as <code>GET /api/users/{int:id}</code>; or returns an error. All fields listed below are mandatory
<pre>
{
    "username": string, must be unique,
    "email": string, must be unique,
    "password: string
}</pre>
Error example:
<pre>{
    "error": "Bad Request",
    "message": "must include username, email and password fields"
}</pre>
</details>
<details>
<summary>PUT /api/users/{int:id}</summary>
<b>Requires user auth token</b> - users are only authorized to change their own details<br>
Modifies a user. Same format as creating a user, except fields are optional and password cannot be changed using this method.<br>
If a users password is change, it will set the <code>reset_pass</code> field on that user to False.<br>
Error also in same format as creating a user<br>
</details>
<details>
<summary>POST /api/users/{int:id}/new_password</summary>
<b>Requires user auth token</b> - users are only authorized to change their own details<br>
Changes the users password. Set the <code>password</code> field to specify the new password<br>
Revokes the current token and returns a new one.
This will also set the <code>reset_pass</code> field on the to False.<br>
Error also in same format as creating a user<br>
</details>
<details>
<summary>POST /api/users/forgot_password</summary>
Requests a reset password email for the specified user. Specify the user by either <code>username</code> 
or <code>email</code> field. Only one is required. On success will send a password reset token to the users email, 
which can be used to receive a temporary token. <br>
<pre>{
    "_links": {
        "user": "/api/users/2"
    },
    "result": "success",
    "user": 2
}</pre>
</details>
<details>
<summary>GET /api/users/forgot_password/{temp_token}</summary>
Uses a temporary token sent to a user via email to get a temporary auth token. This will revoke the current token for
that user, and set an expiry on the new token of 5 minutes. Will also set a <code>reset_pass</code> boolean to true on that user. It is recommended to force the user to change their
password after doing this.<br>
<pre>{
    "expires": "Mon, 25 Mar 2024 04:01:56 GMT",
    "token": "e392ae1467472ee8a591a11915f723b0"
}
</pre>
</details>
<details>
<summary>GET /api/users/{int:id}/permissions</summary>
Gets a detailed list of the users permissions
<pre>{
    "username": "Admin",
    "permissions": [
        {
            "id": 1,
            "key": "team_mgr",
            "description": "Team Manager",
            "modifiers": {
                'team': 1
            },
            "_links": {
                "self": "/api/permissions/1"
            }
        }
    ],
    "_links": {
        "self": "/api/users/1/permissions"
    }
}</pre>
</details>
<details>
<summary>POST /api/users/{int:id}/permissions</summary>
Gives the user specified by {id} the permission defined by field <code>key</code>.
<br>Input:
<pre>{
    'key': 'admin',
    'modifiers': { # insert modifiers as a json }
}</pre>
On success returns the list of that users permissions.
</details>
<details>
<summary>PUT /api/users/{int:id}/permissions</summary>
Updates the the additional modifiers for user specified by {id} and the permission defined by field <code>key</code>.
<b>Overrides the modifiers tag completely with the new input</b>
<br>Input:
<pre>{
    'key': 'admin',
    'modifiers': { # insert modifiers as a json }
}</pre>
On success returns the list of that users permissions.
</details>
<details>
<summary>POST /api/users/{int:id}/permissions/revoke</summary>
Revokes the permission specified by <code>key</code>  for user specified by {id}
<br>Input:
<pre>{
    'key': 'admin'
}</pre>
On success returns the list of that users permissions.
</details>


</details>
<br><details>
<summary><b>Permissions</b></summary>
This section is for requests regarding the permissions table. For assigning permissions to users, check the users section.
<details>
<summary>GET /api/permissions/{id}</summary>
Returns a permission given its ID
<pre>{
    "id": 1,
    "key": "admin",
    "description": "Site Administrator",
    "users_count": 1,
    "_links": {
        "self": "/api/permissions/1"
    }
}</pre>
</details>
<details>
<summary>GET /api/permissions?page=1?per_page=10</summary>
Get a list of all permissions. <code>page</code> and <code>per_page</code> are optional with defaults 1 and 10. Max per page is 100
<pre>{
    "items": [
        { ... permission resource ... },
        { ... permission resource ... },
        ...
    ]
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 1,
        "total_pages": 1
    },
    "_links": {
        "self": "/api/permissions?page=1&per_page=10",
        "next": null,
        "prev": null
    }
}</pre>
</details>
<details>
<summary>POST /api/permissions</summary>
Creates a new permission. Input:
<pre>{
    'key': 'admin',
    'description: 'Site Administrator' # optional
}</pre>
Example output:
<pre>{
    "id": 3,
    "key": "leag_coord",
    "description": "League Coordinator",
    "users_count": 0,
    "_links": {
        "self": "/api/permissions/3"
    }
}</pre>
Example error:
<pre>{
    "error": "Bad Request",
    "message": "key already in use"
}</pre>
</details>
<details>
<summary>PUT /api/permissions/{id}</summary>
Exact same format as for adding a new permission, except that specifying a key is option
</details>
<details>
<summary>GET /api/permissions/{int:id}/users</summary>
Lists all the users who have the specified permission
<pre>{
    "key": "admin",
    "permission": "Site Administrator",
    "users": [
        {
            "_links": {
                "self": "/api/users/1"
            },
            "id": 1,
            "username": "Admin"
        }
    ],
    "_links": {
        "self": "/api/permissions/1/users"
    }    
}</pre>
</details>
</details>