import sqlalchemy as sa

from api.srlm.app.api.errors import error_response
from api.srlm.app.api.functions import ensure_exists
from api.srlm.app.spapi.slapid import get_slap_id
from api.srlm.logger import get_logger
from api.srlm.logger import LogConfig
from api.srlm.definitions import ROOT_DIR
from datetime import datetime
from dotenv import load_dotenv
import os.path
from asgiref.wsgi import WsgiToAsgi


load_dotenv(os.path.join(ROOT_DIR, '.env'))


# Checks if the current log file is set to be wiped on program load and wipes the file if true
log_config = LogConfig()
if log_config.clean == 'true':
    log_path = (log_config.log_dir + '/' + log_config.file_name).format(datetime.now())
    open(log_path, 'w').close()
log = get_logger(__name__)

log.info('Starting web app')
from api.srlm.app import create_app, db
from api.srlm.app.models import User, Permission, UserPermissions, League, Season, Division, SeasonDivision, Player, Team
from api.srlm.api_access.models import AuthorizedApp
app = create_app()
log.info('Web app started, accepting requests')

asgi_app = WsgiToAsgi(app)


@app.errorhandler(404)
def handle_404(e):
    return error_response(e.code, 'Requested resource cannot be found. Check that the URL is correct')


# Shell context processor for development purposes


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'sa': sa,
        'User': User,
        'Permission': Permission,
        'UserPermissions': UserPermissions,
        'League': League,
        'Season': Season,
        'Division': Division,
        'SeasonDivision': SeasonDivision,
        'Player': Player,
        'Team': Team,
        'AuthorizedApp': AuthorizedApp,
        'get_slap_id': get_slap_id,
    }

