from app.utils import pretty_date
from flask_login import UserMixin
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), index=True)
    password_secure = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notifications = db.relationship('Notification', backref="user", lazy="dynamic")
    comments = db.relationship('Comment', backref="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @property
    def first_name(self):
        return self.username.split()[0]

    @property
    def avatar(self):
        return f"https://ui-avatars.com/api/?name={self.username.replace(' ',  '+')}"    

    @property
    def is_admin(self):
        return self.role_id == 1      

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_secure, password)

    def __repr__(self):
        return f'User: {self.username}'

    @login_manager.user_loader
    def load_user(user_id):
        """call back function that retrieves a user when a unique identifier is passed"""
        return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    users = db.relationship('User', backref="role", lazy="dynamic")

class Notification(db.Model):
    '''
    Notifications table
    '''
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    pinned = db.Column(db.Boolean, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='notification', lazy='dynamic')

    @property
    def formatted_time(self):
        from datetime import datetime
        return pretty_date(self.created_at)

    @classmethod
    def get_all_notifications(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_pinned_notifications(cls, limit=3):
        return cls.query.order_by(cls.created_at.desc()).filter_by(pinned=True).limit(limit).all()    

    @classmethod
    def delete_notification(cls, id):
        blog = Notification.query.filter_by(id=id).first()
        db.session.delete(blog)
        db.session.commit()

    def __repr__(self):
        return f'Notification {self.title}'


class Comment(db.Model):
    '''comments table'''
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)  

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @property
    def formatted_time(self):
        from datetime import datetime
        return self.created_at.strftime("%b %d, %Y")    

     # delete comment
    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

    # get all comments created by other users on my posts only 
    @classmethod
    def get_my_posts_comments(cls, user_id):
        comments = Comment.query.filter(Comment.blog.has(user_id=user_id))
        return comments        