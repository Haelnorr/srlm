import os

from api.lds.definitions.paths import ROOT_DIR
from api.lds.definitions.permissions import PERMISSIONS

app_name = os.getenv('SRLM_APP_NAME') or 'Slapshot: Rebound League Manager'
