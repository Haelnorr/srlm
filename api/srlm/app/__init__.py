from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from api.srlm.app.celery import make_celery
from api.srlm.logger import get_logger
from api.srlm.app.config import Config


log = get_logger(__name__)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()


def create_app(config_class=Config):
    # Starting web app and loading config
    log.info('Instantiating Flask web app')
    log.info('Starting app')
    app = Flask(__name__)
    log.info('Loading app config')
    app.config.from_object(config_class)
    if app.config['DEBUG']:
        app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Setting up app modules
    log.info('Starting database connection and setting up modules')
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    celery = make_celery(app)
    celery.set_default()

    # Registering blueprints
    log.info('Registering blueprints')
    with app.app_context():
        from api.srlm.app.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        # only runs when app not in debug or testing mode
        app.logger = log
        pass  # temporary while function is empty

    log.info('Web app instantiated')
    return app, celery


from api.srlm.app import models, events
from api.srlm.api_access import models
