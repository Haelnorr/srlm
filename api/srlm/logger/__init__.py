"""
This package sets up the logging system for the project and makes loggers available by use of the 'get_logger(__name__)' function

"""

from api.srlm.logger.config import LogConfig, MailConfig
from api.srlm.logger.handlers import get_logger
