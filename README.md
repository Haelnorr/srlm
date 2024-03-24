<h2>Endpoints</h2>

<h3>Auth</h3>
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
POST /api/tokens
</summary>
Requests an auth token for a user, provided a valid username and password. Returns 401 error if unauthorized
<pre>{
    "username": "admin",
    "password": "mypassword"
}</pre>
Response:
<pre>{
    "token": "a3b67df3547a49e6cd338a05c442d666"
}</pre>
Error:
<pre>{
    "error": "Unauthorized"
}</pre>
</details>

<h3>Users</h3>
<details>
    <summary>GET /api/users/{int:id}</summary>
    Gets the user data of a user specified by their user id
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
Modifies a user. Same format as creating a user, except fields are optional and password is excluded. # document how to change password.<br>
Error also in same format as creating a user<br>
</details>
