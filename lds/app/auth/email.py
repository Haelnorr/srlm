from flask import render_template
from flask import current_app
from lds.app import email
from lds.definitions import app_name


def send_password_reset_email(user):
    token = user.get_password_reset_token()
    email.send(f'{app_name} - Reset Your Password',
               sender=f"no-reply@{current_app.config['DOMAIN']}",
               recipients=[user.email],
               text_body=render_template('auth/reset_password_email.txt',
                                         user=user, token=token),
               html_body=render_template('auth/reset_password_email.html',
                                         user=user, token=token))


def send_new_user_email(user):
    token = user.get_password_reset_token()
    email.send(f'{app_name} - Account creation',
               sender=f"no-reply@{current_app.config['DOMAIN']}",
               recipients=[user.email],
               text_body=render_template('auth/new_user_email.txt',
                                         user=user, token=token, domain=current_app.config['DOMAIN']),
               html_body=render_template('auth/new_user_email.html',
                                         user=user, token=token, domain=current_app.config['DOMAIN']))
