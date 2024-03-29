<h2>Endpoints</h2>
All requests return a JSON with some information on the outcome. Successful GET requests are documented under their 
respective headings. For more details on success/error responses, see the sections at the bottom.
<h3>Site Access</h3>
<details>
<summary><b>Auth</b></summary>
The API has a two key system for authorization. An app key required for all requests, and a user key required for 
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

<details>
<summary>
<code>POST /api/tokens/user</code>
</summary>
Requests an auth token for a user, provided a valid username and password. Returns 401 error if unauthorized.<br>
Username:password should be submitted using a Basic Authorization header and DOES NOT require an app code<br>
Tokens expire after 14 days unless otherwise specified.
<pre>{
    "token": "a3b67df3547a49e6cd338a05c442d666"
}</pre>
</details>
<details>
<summary>
<code>DELETE /api/tokens/user</code>
</summary>
Revokes the auth token of the current user. <b>Requires user auth token</b><br>
Useful for logging a user out<br>
</details>
<details>
<summary>
<code>POST /api/tokens/user/validate</code>
</summary>
Checks if user auth token submitted is still valid. <b>Requires user auth token</b><br>
Useful for checking if user is logged in. Returns <code>403 FORBIDDEN</code> if token is not valid.<br>
<pre>{
    "user": 2,
    "expires": "Tue, 26 Mar 2024 03:16:34 GMT",
    "_links": {
        "user": "/api/users/2"
    }
}
</pre>
</details>
<details>
<summary>
<code>GET /api/tokens/app</code>
</summary>
Gets the token and expiry date of the current app token.<br>
Since it requires a valid app token to access, 
and only gives details on that token, only really useful for getting the expiry date<br>

<pre>{
    "expiry": "Tue, 23 Apr 2024 23:02:17 GMT",
    "token": "4ded8ce3796b368e93c5f87d36a7def051"
}
</pre>
</details>
<details>
<summary>
<code>POST /api/tokens/app</code>
</summary>
Requests a new app token and resets the expiry date.<br>
Requires a valid app token to access, 
and cannot be used to reset another authorized app's token.<br>
<pre>{
    "expiry": "Tue, 23 Apr 2024 23:02:17 GMT",
    "token": "4ded8ce3796b368e93c5f87d36a7def051"
}
</pre>
</details>
</details>
<br><details>
<summary><b>Users</b></summary>
<ul>
<details>
<summary><u>General</u></summary>
<ul>
<details>
    <summary><code>GET /api/users</code></summary>
    Gets list of all users. Optional args and defaults:<code>page=1, per_page=10 (max 100)</code>
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
    <summary><code>GET /api/users/{id}</code></summary>
    Gets the user data of a user specified by their user id. The list of permissions in this result returns the keys 
only. For a full list see <code>GET /api/users/{int:id}/permissions</code><br>
<code>email</code> is only returned if that user's token is submitted in the request
    <pre>{
    "id": 1,
    "username": "Admin",
    "email": "admin@email.com", # only returned if the user requested their own data
    "player": 1,
    "discord": 34234523452345,
    "permissions": [
        "admin"
    ],
    "matches_streamed": 0,
    "matches_reviewed": 0,
    "reset_pass": false,
    "_links": {
        "self": "/api/users/1",
        "player": "/api/players/1",
        "discord": "/api/users/1/discord",
        "permissions": "/api/users/1/permissions",
        "matches_streamed": "/api/users/1/matches_streamed",
        "matches_reviewed": "/api/users/1/matches_reviewed",
    }
}</pre>
</details>
<details>
<summary><code>POST /api/users</code></summary>
Creates a new user. Returns a <code>201 CREATED</code>
<pre>
{
    "username": string, must be unique,
    "email": string, must be unique,
    "password: string
}</pre>
</details>
<details>
<summary><code>PUT /api/users/{int:id}</code></summary>
<b>Requires user auth token</b> - users are only authorized to change their own details<br>
Modifies a user. Returns <code>200 OK</code><br>
<pre># <em>italicised</em> fields are optional 
{
    <em>"username": "Admin"</em>,
    <em>"email": "admin@email.com"</em>
}</pre>
</details>
</ul>
</details>
<details>
<summary><u>Passwords</u></summary>
<ul>
<details>
<summary><code>POST /api/users/{id}/new_password</code></summary>
<b>Requires user auth token</b> - users are only authorized to change their own details<br>
Changes the users password. 
This will also set the re-issue the user token and set the <code>reset_pass</code> field on the user to False.<br>
Response is the new token.
<pre>{
    "password": "newpassword"
}</pre>
</details>
<details>
<summary><code>POST /api/users/forgot_password</code></summary>
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
<summary><code>GET /api/users/forgot_password/{temp_token}</code></summary>
Uses a temporary token sent to a user via email to get a temporary auth token. This will revoke the current token for
that user, and set an expiry on the new token of 5 minutes. Will also set a <code>reset_pass</code> boolean to true on that user. It is recommended to force the user to change their
password after doing this.<br>
<pre>{
    "expires": "Mon, 25 Mar 2024 04:01:56 GMT",
    "token": "e392ae1467472ee8a591a11915f723b0"
}
</pre>
</details>
</ul>
</details>
<details>
<summary><u>Permissions</u></summary>
<ul>
<details>
<summary><code>GET /api/users/{id}/permissions</code></summary>
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
<summary><code>POST /api/users/{id}/permissions</code></summary>
Gives the user the permission defined by field <code>key</code>.<br>
Success returns <code>201 CREATED</code>
<pre>{
    'key': 'admin',
    'modifiers': { # insert modifiers as a json }
}</pre>
</details>
<details>
<summary><code>PUT /api/users/{id}/permissions</code></summary>
Updates the additional modifiers for user specified by {id} and the permission defined by field <code>key</code>.
<b>Overrides the modifiers tag completely with the new input</b>
<pre>{
    'key': 'admin',
    'modifiers': { # insert modifiers as a json }
}</pre>
</details>
<details>
<summary><code>POST /api/users/{id}/permissions/revoke</code></summary>
Revokes the permission specified by <code>key</code>  for user specified by {id}
<pre>{
    'key': 'admin'
}</pre>
</details>
</ul>
</details>
<details>
<summary><u>Discord</u></summary>
<ul>
<details>
<summary><code>GET /api/users/{id}/discord</code></summary>
Gets the user's linked discord profile. If request sent including user auth code, will also return
the access and refresh tokens
<pre>{
    "user": "Haelnorr",
    "discord_id": "1230918231",
    "token_expiration": "Tue, 26 Mar 2024 03:16:34 GMT",
    "access_token": "132f4d1234df1234d123e4213df234f",
    "refresh_token": "12387n293mo4if28734j9rm28d34r",
    "_links": {
        "self": "/api/users/2/discord",
        "user": "/api/users/2"
    }
}</pre>
</details>
<details>
<summary><code>POST /api/users/{id}/discord</code></summary>
Creates a new entry in the database recording the users discord information. User must be authenticated.<br>
<pre>{
    'discord_id': '123491203481209348123',
    'access_token': '31r234d123ecdx134fe234d',
    'refresh_token': '12w1ce2f234cs243ew',
    'expires_in': 604800
}</pre>
</details>
<details>
<summary><code>PUT /api/users/{id}/discord</code></summary>
Update a users discord information. User must be authenticated.
<pre># All fields optional
{
    'discord_id': '123491203481209348123',
    'access_token': '31r234d123ecdx134fe234d',
    'refresh_token': '12w1ce2f234cs243ew',
    'expires_in': 604800
}</pre>
</details>
<details>
<summary><code>DELETE /api/users/{id}/discord</code></summary>
Removes a users discord information. User must be authenticated. Returns <code>200 OK</code> on success
</details>
</ul>
</details>
<details>
<summary><u>Twitch</u></summary>
<ul>
<details>
<summary><code>GET /api/users/{id}/twitch</code></summary>
Gets the user's linked Twitch profile. If request sent including user auth code, will also return
the access and refresh tokens
<pre>{
    "user": "Haelnorr",
    "twitch_id": "1230918231",
    "token_expiration": "Tue, 26 Mar 2024 03:16:34 GMT",
    "access_token": "132f4d1234df1234d123e4213df234f",
    "refresh_token": "12387n293mo4if28734j9rm28d34r",
    "_links": {
        "self": "/api/users/2/twitch",
        "user": "/api/users/2"
    }
}</pre>
</details>
<details>
<summary><code>POST /api/users/{id}/twitch</code></summary>
Creates a new entry in the database recording the users twitch information. User must be authenticated. Returns <code>201 CREATED</code> on success<br>
<pre>{
    'twitch_id': '123491203481209348123',
    'access_token': '31r234d123ecdx134fe234d',
    'refresh_token': '12w1ce2f234cs243ew',
    'expires_in': 604800
}</pre>
</details>
<details>
<summary><code>PUT /api/users/{id}/twitch</code></summary>
Update a users twitch information. User must be authenticated. Returns <code>200 OK</code> on success
<pre># all fields optional
{
    'twitch_id': '123491203481209348123',
    'access_token': '31r234d123ecdx134fe234d',
    'refresh_token': '12w1ce2f234cs243ew',
    'expires_in': 604800
}</pre>
</details>
<details>
<summary><code>DELETE /api/users/{id}/twitch</code></summary>
Removes a users twitch information. User must be authenticated. Returns <code>200 OK</code> response on success
</details>
</ul>
</details>
</ul>


</details>
<br><details>
<summary><b>Permissions</b></summary>
This section is for requests regarding the permissions table. For assigning permissions to users, check the users section.
<ul>
<details>
<summary><code>GET /api/permissions/{id_or_key}</code></summary>
Returns a permission given its ID or unique key
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
<summary><code>GET /api/permissions</code></summary>
Get a list of all permissions. Optional args and defaults:<code>page=1, per_page=10 (max 100)</code>
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
<summary><code>POST /api/permissions</code></summary>
Creates a new permission.
<pre># Italicised fields are optional
{
    'key': 'admin',
    <em>'description: 'Site Administrator'</em>
}</pre>
</details>
<details>
<summary><code>PUT /api/permissions/{id_or_key}</code></summary>
Updates an existing permission
<pre># Italicised fields are optional
{
    <em>'key': 'admin',</em>
    <em>'description: 'Site Administrator'</em>
}</pre>
</details>
<details>
<summary><code>GET /api/permissions/{id_or_key}/users</code></summary>
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
</ul>
</details>
<br>
<h3>League Management</h3>
<br><details>
<summary><b>Leagues</b></summary>
<ul>
<details>
<summary><code>GET /api/leagues</code></summary>
Returns a list of all leagues. Optional args and defaults:<code>page=1, per_page=10 (max 100)</code>
<pre>{
    "items": [
        { ... league item ... },
        { ... league item ... },
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 2,
        "total_pages": 1
    },
    "_links": {
        "next": null,
        "prev": null,
        "self": "/api/leagues?page=1&per_page=10"
    }
}</pre>
</details>
<details>
<summary><code>GET /api/leagues/{id_or_acronym}</code></summary>
Returns a specified league
<pre>{
    "id": 1,
    "name": "Oceanic Slapshot League",
    "acronym": "OSL",
    "seasons_count": 18,
    "divisions_count": 3,
    "_links": {
        "self": "/api/leagues/1",
        "seasons": "/api/leagues/1/seasons",
        "divisions": "/api/leagues/1/divisions"
    }
}</pre>
</details>
<details>
<summary><code>POST /api/leagues</code></summary>
Creates a new league with the specified details.
<pre>{
    "name": "Oceanic Slapshot League",
    "acronym": "OSL"
}</pre>
<pre>{
    "id": 1,
    "name": "Oceanic Slapshot League",
    "acronym": "OSL",
    "seasons_count": 18,
    "divisions_count": 3,
    "_links": {
        "self": "/api/leagues/1",
        "seasons": "/api/leagues/1/seasons",
        "divisions": "/api/leagues/1/divisions"
    }
}</pre>
</details>
<details>
<summary><code>PUT /api/leagues/{id_or_acronym}</code></summary>
Updates a league with the specified details.
<pre># Italicised fields are optional
{
    <em>"name": "Oceanic Slapshot League",</em>
    <em>"acronym": "OSL"</em>
}</pre>
<pre>{
    "id": 1,
    "name": "Oceanic Slapshot League",
    "acronym": "OSL",
    "seasons_count": 18,
    "divisions_count": 3,
    "_links": {
        "self": "/api/leagues/1",
        "seasons": "/api/leagues/1/seasons",
        "divisions": "/api/leagues/1/divisions"
    }
}</pre>
</details>
<details>
<summary><code>GET /api/leagues/{id_or_acronym}/seasons</code></summary>
Gets a list of seasons in the specified league. Optional args and defaults: <code>page=1, per_page=10 (max 100)</code>
<pre>{
    "league": "Oceanic Slapshot League",
    "acronym": "OSL",
    "items": [
        { ... season item ... },
        { ... season item ... },
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 18,
        "total_pages": 2
    },
    "_links": {
        "next": "/api/leagues/1/seasons?page=2&per_page=10",
        "prev": null,
        "self": "/api/leagues/1/seasons?page=1&per_page=10"
    }
}</pre>
</details>
<details>
<summary><code>GET /api/leagues/{id_or_acronym}/divisions</code></summary>
Gets a list of divisions in the specified league. Optional args and defaults: <code>page=1, per_page=10 (max 100)</code>
<pre>{
    "league": "Oceanic Slapshot League",
    "acronym": "OSL",
    "items": [
        { ... division item ... },
        { ... division item ... },
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 3,
        "total_pages": 1
    },
    "_links": {
        "next": null,
        "prev": null,
        "self": "/api/leagues/1/divisions?page=1&per_page=10"
    }
}</pre>
</details>
</ul>
</details>
<br><details>
<summary><b>Seasons</b></summary>
<ul>
<details>
<summary><code>GET /api/seasons</code></summary>
Returns a list of all seasons. Optional args and defaults:<code>page=1, per_page=10 (max 100)</code>
<pre>{
    "items": [
        { ... season item ... },
        { ... season item ... },
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 2,
        "total_pages": 1
    },
    "_links": {
        "next": null,
        "prev": null,
        "self": "/api/seasons?page=1&per_page=10"
    }
}</pre>
</details>
<details>
<summary><code>GET /api/seasons/{id}</code></summary>
Returns a specified season
<pre>{
    "id": 1,
    "name": "Season 1",
    "acronym": "S1",
    "league": "OSL",
    "match_type": "League",
    "divisions_count": 1,
    "start_date": null
    "end_date": null,
    "finals_end": null,
    "finals_start": null,
    "_links": {
        "divisions": "/api/seasons/1/divisions",
        "league": "/api/leagues/1",
        "match_type": null,
        "self": "/api/seasons/1"
    }
}</pre>
</details>
<details>
<summary><code>POST /api/seasons</code></summary>
Creates a new season with the specified details. <code>match_type</code> specifies the preset for lobby settings 
(i.e. periods, length, game type etc.)<br>
There can be multiple seasons with the same name or acronym, but not in the same league.
<pre># Italicised fields are optional
# Date input should be in the format YYYY-MM-DD
{
    "name": "Season 18",
    "acronym": "S18",
    "league": "osl", # can be ID or acronym
    "match_type": "league", # can be ID or name
    <em>"start_date": "2024-04-24",</em>
    <em>"end_date": "2024-05-24",</em>
    <em>"finals_start": "2024-05-24",</em>
    <em>"finals_end": "2024-06-15"</em>
}</pre>
</details>
<details>
<summary><code>PUT /api/seasons/{id}</code></summary>
Updates a season with the specified details.
<pre># Italicised fields are optional
# Date input should be in the format YYYY-MM-DD
{
    <em>"name": "Season 18",</em>
    <em>"acronym": "S18",</em>
    <em>"start_date": "2024-04-24",</em>
    <em>"end_date": "2024-05-24",</em>
    <em>"finals_start": "2024-05-24",</em>
    <em>"finals_end": "2024-06-15"</em>
}</pre>
</details>
<details>
<summary><code>GET /api/seasons/{id}/divisions</code></summary>
Gets a list of divisions in the specified season. Optional args and defaults: <code>page=1, per_page=10 (max 100)</code>
<pre>{
    "season": "Season 1",
    "acronym": "S1",
    "league": "OSL",
    "items": [
        { ... season_division item ... }
        { ... season_division item ... }
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 1,
        "total_pages": 1
    },
    "_links": {
        "next": null,
        "prev": null,
        "self": "/api/seasons/1/divisions?page=1&per_page=10"
    }
}</pre>
</details>
</ul>
</details>
<br><details>
<summary><b>Divisions</b></summary>
<ul>
<details>
<summary><code>GET /api/divisions</code></summary>
Returns a list of all divisions. Optional args and defaults:<code>page=1, per_page=10 (max 100)</code>
<pre>{
    "items": [
        { ... division item ... },
        { ... division item ... },
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 3,
        "total_pages": 1
    },
    "_links": {
        "next": null,
        "prev": null,
        "self": "/api/divisions?page=1&per_page=10"
    }
}</pre>
</details>
<details>
<summary><code>GET /api/divisions/{id}</code></summary>
Returns a specified division
<pre>{
    "id": 1,
    "name": "Pro League",
    "acronym": "PL",
    "league": "OSL",
    "description": "Where the Pros at",
    "seasons_count": 1,
    "_links": {
        "league": "/api/leagues/1",
        "seasons": "/api/divisions/1/seasons",
        "self": "/api/leagues/1"
    }
}</pre>
</details>
<details>
<summary><code>POST /api/divisions</code></summary>
Creates a new division with the specified details. <br>
There can be multiple divisions with the same name or acronym, but not in the same league.
<pre># Italicised fields are optional
{
    "name": "Open League",
    "acronym": "OL",
    "league": "osl", # can be ID or acronym
    <em>"description": "Where players new to the game can start"</em>
}</pre>
</details>
<details>
<summary><code>PUT /api/divisions/{id}</code></summary>
Updates a division with the specified details.
<pre># Italicised fields are optional
{
    <em>"name": "Open League",</em>
    <em>"acronym": "OL",</em>
    <em>"description": "Where players new to the game can start"</em>
}</pre>
</details>
<details>
<summary><code>GET /api/divisions/{id}/seasons</code></summary>
Gets a list of divisions in the specified season. Optional args and defaults: <code>page=1, per_page=10 (max 100)</code>
<pre>{
    "division": "Pro League",
    "acronym": "PL",
    "league": "OSL",
    "seasons": [
        {
            "name": "Season 1",
            "acronym": "S1",
            "id": 1,
            "_links": {
                "self": "/api/seasons/1"
            }
        }
    ],
    "_links": {
        "league": "/api/leagues/1",
        "self": "/api/divisions/1/seasons"
    }
}</pre>
</details>
</ul>
</details>
<br><details>
<summary><b>Players</b></summary>
<ul>
<details>
<summary><code>GET /api/players/{id}</code></summary>
Gets the specified player.
<pre>{
    "player_name": "Eagle",
    "slap_id": 155,
    "user": null,
    "current_team": null,
    "teams": 0,
    "first_season": "Season 1 Single League",
    "rookie": true,
    "free_agent_seasons": 0,
    "next_name_change": null,
    "_links": {
        "current_team": null,
        "first_season": "/api/season_division/1",
        "free_agent_seasons": "/api/players/1/free_agent",
        "self": "/api/players/1",
        "teams": "/api/players/1/teams",
        "user": "/api/users/1"
    }
}</pre>
</details>
<details>
<summary><code>GET /api/players</code></summary>
Gets the collection of all players
<pre>{
    "items": [
        { ... player item ... }
        { ... player item ... }
        ...
    ],
    "_meta": {
        "page": 1,
        "per_page": 10,
        "total_items": 363,
        "total_pages": 37
    },
    "_links": {
        "next": "/api/players?page=2&per_page=10",
        "prev": null,
        "self": "/api/players?page=1&per_page=10"
    }
}</pre>
</details>
<details>
<summary><code>POST /api/players</code></summary>
Creates a new user.
<pre># Italicised fields are optional
{
    "player_name": "BestRookie",
    <em>"slap_id": 1213456,</em>
    <em>"rookie": true,</em>
    <em>"first_season_id": 42</em>
}</pre>
</details>
<details>
<summary><code>PUT /api/players/{id}</code></summary>
Updates a user.
<pre># Italicised fields are optional
{
    <em>"player_name": "BestRookie",</em>
    <em>"slap_id": 1213456,</em>
    <em>"rookie": true,</em>
    <em>"first_season_id": 42</em>
}</pre>
</details>
</ul>
</details>
<br>

<h3>Responses</h3>
<details>
<summary><b>Success Responses</b></summary>
Some requests will respond with a more generic response format instead of a detailed object with lots of information.
Information from these responses are still helpful, and follow this format:
<pre># Example of a '200 OK' response
{
    "result": "OK",
    "message": "Division Open League updated",
    "location": "/api/divisions/3"
}</pre>
</details>
<br><details>
<summary><b>Error Responses</b></summary>
All error responses should have the corresponding HTTP response code as well as a body that follows this format:
<pre># Example 404 error response
{
    "error": "Not Found",
    "message": "Requested resource cannot be found",
    "missing_resource": "User with ID 5" # this field is only found on 404 errors
}</pre>
If an error occurs and you do not get a response that follows this format, please open an issue with details on how to 
reproduce the problem.
<ul></ul>
</details>