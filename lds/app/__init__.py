from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from lds.logger import get_logger
from lds.app.config import Config


log = get_logger(__name__)

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = None
mail = Mail()
# bootstrap = Bootstrap()
# moment = Moment()


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
    # bootstrap.init_app(app)
    # moment.init_app(app)

    # Registering blueprints
    log.info('Registering blueprints')
    from lds.app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from lds.app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from lds.app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        # only runs when app not in debug or testing mode
        app.logger = log
        pass  # temporary while function is empty

    log.info('Web app instantiated')
    return app


from lds.app import models, events
