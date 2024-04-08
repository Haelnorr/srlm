"""Main package for Slapshot: Rebound League Manager"""

import api.srlm.definitions
import api.srlm.app
import api.srlm.logger
import api.srlm.api_access

from api.srlm.run import asgi_app as asgi
from api.srlm.run import celery
