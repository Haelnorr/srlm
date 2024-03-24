#Endpoints

###Users
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
Modifies a user. Same format as creating a user, except fields are optional and password is excluded. # document how to change password.<br>
Error also in same format as creating a user
</details>