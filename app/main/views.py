from . import main
from flask import render_template, url_for, abort, request, redirect, flash
from flask_login import login_required, current_user
from ..models import User
from .. import db
from ..emails import mail_message


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/notifications')
def notifications():
    return render_template('notifications.html')

@main.route('/notifications/<id>')
def notification_show(id):
    return render_template('single-news-page.html')    

