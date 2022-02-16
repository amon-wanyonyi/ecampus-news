from flask import render_template
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/notifications')
def notifications():
    return render_template('notifications.html')

@main.route('/notifications/<id>')
def notification_show(id):
    return render_template('single-news-page.html')    