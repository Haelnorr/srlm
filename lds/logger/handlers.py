import logging
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler, SMTPHandler
from lds.logger import LogConfig, MailConfig
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_config = LogConfig()
mail_config = MailConfig()
LOG_FILE = log_config.log_dir + '/' + log_config.file_name


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE.format(datetime.now()), when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_mail_handler():
    auth = None
    if mail_config.mail_username or mail_config.mail_password:
        auth = (mail_config.mail_username, mail_config.mail_password)
    secure = None
    if mail_config.mail_use_tls:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(mail_config.mail_server, mail_config.mail_port),
        fromaddr='no-reply@' + mail_config.mail_server,
        toaddrs=mail_config.admins, subject='LDS Manager - Error',
        credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    return mail_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_config.level)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    if mail_config.mail_alerts_on:
        logger.addHandler(get_mail_handler())
    logger.propagate = False
    return logger
