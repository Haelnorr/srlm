"""Functions for sending emails"""
import os
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from api.srlm.app import mail

# TODO CONVERT TO CELERY
# Sending mail with the context of the app
from api.srlm.definitions import app_name


def send_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # Sending the mail request to a separate thread for asynchronous processing
    # Requires access to the protected member '_get_current_object()' as
    # current_app is a proxy and has no value outside of the context of the main thread
    Thread(target=send_async, args=(current_app._get_current_object(), msg)).start()  # noqa TODO


def send_password_reset_email(user):  # TODO change
    token = user.get_password_reset_token()
    print(token)
    send(f'{app_name} - Reset Your Password',
         sender=os.getenv('OUTGOING_MAIL_ADDRESS'),
         recipients=[user.email],
         text_body=render_template('auth/reset_password_email.txt',
                                   user=user, token=token),
         html_body=render_template('auth/reset_password_email.html',
                                   user=user, token=token))


def send_new_user_email(user):  # TODO change
    token = user.get_password_reset_token()
    send(f'{app_name} - Account creation',
         sender=os.getenv('OUTGOING_MAIL_ADDRESS'),
         recipients=[user.email],
         text_body=render_template('auth/new_user_email.txt',
                                   user=user, token=token, domain=current_app.config['DOMAIN']),
         html_body=render_template('auth/new_user_email.html',
                                   user=user, token=token, domain=current_app.config['DOMAIN']))
