from flask import render_template, current_app
from flask_mail import Message
from . import mail
from decouple import config
from time import sleep  
from threading import Thread  


sender_email = config("MAIL_USERNAME", default="")

def mail_message(subject,template,to,**kwargs):

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)


def send_async_email(app, msg):
    with app.app_context():
        # block only for testing parallel thread
        for i in range(10, -1, -1):
            sleep(2)
            print('time:', i)
        print('====> sending async')
        mail.send(msg)


def mail_async_message(subject,template,to,**kwargs):
    app = current_app._get_current_object()

    msg = Message(subject, sender=("ECampus", sender_email), recipients=[to])
    msg.html = render_template(template + ".html",**kwargs)

    thr = Thread(target=send_async_email, args=[app, msg])

    thr.start()    