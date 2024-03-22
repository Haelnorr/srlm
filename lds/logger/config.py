import os.path
import configparser
from lds.definitions import ROOT_DIR


class LogConfig:
    """Object storing the config data from logger.config"""
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(ROOT_DIR, 'config', 'logger.config'))

        self.log_dir = config['LOGGER']['LogDirectory']
        self.file_name = config['LOGGER']['FileName']
        self.level = get_level(config['LOGGER']['LogLevel'])
        self.clean = config['LOGGER']['WipeCurrentFile']


class MailConfig:
    """Object storing the config data for the mail server and mailing list"""
    def __init__(self):

        config = configparser.ConfigParser()
        config.read(os.path.join(ROOT_DIR, 'config', 'mail.config'))
        mailing_list = config['MAIL']['MailingList'].split(', ')

        self.mail_alerts_on = config['MAIL']['MailAlerts']
        self.mail_server = os.getenv('MAIL_SERVER')
        self.mail_port = int(os.getenv('MAIL_PORT') or 25)
        self.mail_use_tls = os.getenv('MAIL_USE_TLS') is not None
        self.mail_username = os.getenv('MAIL_USERNAME')
        self.mail_password = os.getenv('MAIL_PASSWORD')
        self.admins = mailing_list


def get_level(level):
    return {
        'notset': 0,
        'debug': 10,
        'info': 20,
        'warn': 30,
        'error': 40,
        'critical': 50
    }[level]
