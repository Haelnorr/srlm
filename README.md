# LDS Web Manager - Base Kit

This package provides a base kit for developing web based applications, with support for users, user management and 
database functionality. It also provides email support and logging (both developer logs and application event logs).

**Setup Instructions**  
Setup Python Environment by running command `pip install -r requirements.txt`  
**It is recommended that you do this inside a VENV**  
To initialize the database, run the command `flask db upgrade`  
Once completed, follow the following steps:  
1. Run `flask shell` in the VENV command line to start a python shell with the context of the flask app and then enter the following commands
2. `u = User(username='admin', permissions=1)`
3. `u.set_password('yournewpassword')`
4. `db.session.add(u)`
5. `db.session.commit()`

This will add a superuser with the name 'admin' that will let you manage and create other users.  
**IMPORTANT: Super users can ONLY be created from the command line, and will have full access to any feature of the site regardless of other permission flags.**

**Config**  
To set the name of your application, go to`/lds/definitions/__init.py__`
and change the `app_name` variable  
Log config can be set in the `logger.config` file  
Mailing alerts can be configured in the `mail.config` file  
Environment variables can be set in `.env` (or you can set your own environment variables in place of using the `.env` file)  
**IMPORTANT: Flask requires a secret key to be set. Use the `SECRET_KEY` environment variable, and it is recommended to generate a random string for this and keep it hidden



# Modules
**LDS**
 - \_\_init__.py - imports all the modules for use in the application
 - exceptions.py - definitions of custom error exceptions
 - wsgi.py - where the app is called and initialized, also defines a shell context processor for command line interaction

**App**
 - \_\_init__.py - where the instance of the app is defined and loaded with config and modules
 - config.py - handles config for the application and attachment of databases to be used
 - email.py - functions for handling asyc sending of emails from the application
 - events.py - functions for logging and fetching of application events
 - models.py - class definitions of database objects (e.g. Users, Events)

**App/Auth** - For handling the user account functionality
 - \_\_init__.py - used for importing the auth module into the flask app
 - email.py - functions for sending emails to users for password reset
 - forms.py - contains the classes used for building the Flask forms used by the auth module
 - functions.py - handy functions for handling user data
 - routes.py - contains the methods for handling user traffic and page loading of the auth module  

**App/Errors** - For handling HTTP errors
 - \_\_init__.py - used for importing the errors module into the flask app
 - handlers.py - contains handlers for defined HTTP errors (e.g. 404)

**App/Main** - For the main site pages
 - \_\_init__.py - used for importing the errors module into the flask app
 - forms.py - empty; place for any FlaskForm class definitions used in the main site pages
 - routes.py - contains the methods for handling user traffic and page loading of the main site pages

**App/Static** - For any static files (e.g. CSS files)
 - base.css - base site CSS
 - forms.css - for styling of forms
 - main.css - for CSS specific to page content of main site pages

**App/Templates**  
This directory contains all the html templates used in producing the web pages that end users will see. They are 
called up by the functions in each modules `routes.py`, and can be extended by other templates. See documentation for 
Jinja2 and/or Flask for specifics on how these operate.

**Definitions**
 - \_\_init__.py - used for importing of the definitions module and defining the application name
 - paths.py - method used to return the root directory of the project
 - permissions.py - defining of the permission flags and their values for easy use across the codebase

**Logger**
 - \_\_init__.py - used for importing of the logger module across the codebase
 - config.py - handles importing of the logger config from file and setting parameters
 - handlers.py - defines functions for handlers to be added to the logger, and a get_logger function for use across the codebase


