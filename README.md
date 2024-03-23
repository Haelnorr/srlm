This will be expanded on properly later, in the meantime here's the rub:


**GET /auth/user/?**  
Returns user information on user via providing the user ID  
Response is a json:  
```
{  
    "user_id": 1,
    "username": "Admin",  
    "email": "admin@email.com",  
    "permissions": [ "admin" ]  
}
```
&nbsp;  
**POST /auth/authenticate_user**  
Checks if a user can be authenticated given a username and password. Body should be sent as a JSON  
```
{
    "username": "Admin",
    "password": "1234"
}
```