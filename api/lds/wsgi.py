import sqlalchemy as sa
from api.lds.logger import get_logger
from api.lds.logger import LogConfig
from api.lds.definitions import ROOT_DIR
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
from api.lds.app import create_app, db, events
import api.lds.app.models as md
app = create_app()
log.info('Web app started, accepting requests')

asgi_app = WsgiToAsgi(app)


# Shell context processor for development purposes


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'sa': sa,
        'md': md,
        'get_events': events.get_events,
    }

