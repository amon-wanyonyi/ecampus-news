from . import main
from flask import render_template, url_for, abort, request, redirect, flash
from flask_login import login_required, current_user
from ..models import Notification, User, Comment
from .. import db
from ..emails import mail_message
from .forms import BlogForm,CommentForm,ProfileForm,EditBlogForm


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
    notification = Notification.query.get(id)
    form = CommentForm()
    if not notification:
        abort(404)
    return render_template('single-news-page.html', Comment=Comment, commentForm=form, notification=notification)    

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

# comments
@main.route("/notification/<id>/comment", methods=["POST"])
@login_required
def save_comment(id):
    notification = Notification.query.get(id)
    form = CommentForm()
    if not notification:
        abort(404)
    
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, user=current_user, notification=notification)
        comment.save_comment()
        flash("Your comment was saved successfully", "success")

    return redirect(request.referrer or url_for('main.index'))      

@main.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
    if not current_user.is_admin:
        abort(403)
    notifications = Notification.get_all_notifications()
    users = User.query.order_by(User.created_at.desc()).limit(100).all()
    return render_template('dashboard.html', users=users, notifications=notifications)    

@main.route('/profile', methods=["GET","POST"])
@login_required
def profile():
    profile_form = ProfileForm()
    # return profile_form.data
    if profile_form.validate_on_submit():
        User.query.filter_by(id=current_user.id).update({'username':profile_form.username.data})
        db.session.commit()
        flash("Your details have been updated", "success")
        return redirect(url_for('main.profile'))

    return render_template('profile.html', form=profile_form, Comment = Comment) 

@main.route('/user/<id>/update', methods=["POST"])
@login_required
def user_update(id):
    user = User.query.get(id)
    if not user:
        abort(404)

    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        role_id = request.form['role_id'] or user.role_id
        User.query.filter_by(id=user.id).update({'username':profile_form.username.data, 'role_id': role_id})
        db.session.commit()
        flash("User details have been updated", "success")
    return redirect(url_for('main.dashboard'))      


@main.route("/user/<id>/delete", methods=["GET"])
@login_required
def delete_user(id):
    user = User.query.get(id)
    if not user or user.id is current_user.id:
        abort(404)
    
    User.delete_user(id) 

    return redirect(request.referrer or url_for('main.dashboard'))          

@main.route('/profile/update-password', methods=["POST"])
@login_required
def password_update():
    old_password = request.form['old_password']
    password = request.form['password']
    if current_user.verify_password(old_password):
        User.query.filter_by(id=current_user.id).password = password
        db.session.commit()
        flash("Your password has been updated", "success")
    else:
        flash("Please provide the correct old password", "error")    
    return redirect(url_for('main.profile')) 

# delete notification
@main.route("/notification/<id>/delete", methods=["GET"])
@login_required
def delete_notification(id):
    notification = Notification.query.get(id)
    if not notification or notification.user_id is not current_user.id:
        abort(404)
    
    Notification.delete_notification(id) 

    return redirect(request.referrer or url_for('main.index'))  


@main.route('/blog/<id>/update', methods=['POST'])
@login_required
def notification_update(id):
    form = EditBlogForm()
    blog = Notification.query.get(id)
    if not blog:
        abort(404)

    if form.validate_on_submit():
        Notification.query.filter_by(id=id).update({"title":form.title.data, "content":form.content.data, 
            "pinned":form.pinned.data})
        db.session.commit()
        flash("Notification updated successfully", "success")

    return redirect(request.referrer or url_for('main.index'))    