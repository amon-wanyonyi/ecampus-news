from . import main
from flask import render_template, url_for, abort, request, redirect, flash
from flask_login import login_required, current_user
from ..models import Notification, User
from .. import db
from ..emails import mail_message
from .forms import BlogForm


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/notifications')
@login_required
def notifications():
    notifications = Notification.get_all_notifications()
    pinned_notifications = Notification.get_pinned_notifications()
    return render_template('notifications.html', notifications=notifications, pinned_notifications=pinned_notifications)

@main.route('/notifications/<id>')
def notification_show(id):
    return render_template('single-news-page.html')    

@main.route('/notification/create', methods=['POST'])
@login_required
def notification_create():
    form = BlogForm()

    if form.validate_on_submit():

        blog = Notification(title=form.title.data, content=form.content.data,
                      user=current_user, pinned=form.pinned.data)

        db.session.add(blog)
        db.session.commit()

        flash("Notification added successfully", "success")

    return redirect(request.referrer or url_for('main.index'))  