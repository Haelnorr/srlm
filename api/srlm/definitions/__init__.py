"""Basic project level definitions"""
import os

from api.srlm.definitions.paths import ROOT_DIR

app_name = os.getenv('SRLM_APP_NAME') or 'Slapshot: Rebound League Manager'
