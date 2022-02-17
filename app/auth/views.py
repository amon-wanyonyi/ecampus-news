
from . import auth
from flask import render_template,redirect,url_for,request,flash
from ..models import User
from .. import db
from ..emails import mail_message
from flask_login import login_user,logout_user,login_required


@auth.route('/register',methods = ["GET","POST"])
def register():
    """Register view function"""
    if request.method == 'POST':
        post_username = request.form['username']
        post_email = request.form['email']
        post_password = request.form['password']
        new_post = User(username=post_username, email=post_email, password=post_password, role_id=2)

        db.session.add(new_post)
        db.session.commit()

        mail_message("Welcome to eCampus Application", "email/welcome",new_post.email)

        login_user(new_post)
        flash("Your account was created successfully","success")
        return redirect(request.args.get('next') or url_for('main.navigations'))

    return render_template('auth/register.html')



@auth.route('/login',methods = ["GET","POST"])
def login():
    """Login view function"""
    if request.method == 'POST':
        post_email = request.form['email']
        post_password = request.form['password']
        user=User.query.filter_by(email=post_email).first()
        if user is not None and user.verify_password(post_password):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.notifications'))
        flash("Incorrect credentials","error")

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    """Logout function"""
    logout_user()
    return redirect(url_for('main.index'))
