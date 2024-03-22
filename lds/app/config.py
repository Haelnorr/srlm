import os
import configparser
from lds.definitions import ROOT_DIR


config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, 'config', 'mail.config'))
mailing_list = config['MAIL']['MailingList'].split(', ')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') # or '4bcc9d9906fb680fd7ee0b4458f7d604eeb51dffbbabd65736a9272238a5dd2c'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # or 'sqlite:///' + os.path.join(ROOT_DIR, 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    DOMAIN = os.getenv('DOMAIN')
    ADMINS = mailing_list

