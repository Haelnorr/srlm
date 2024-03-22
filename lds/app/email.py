from flask import current_app
from flask_mail import Message
from threading import Thread
from lds.app import mail


# Sending mail with the context of the app
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
    Thread(target=send_async, args=(current_app._get_current_object(), msg)).start()
