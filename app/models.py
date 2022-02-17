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


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @property
    def first_name(self):
        return self.username.split()[0]

    @property
    def avatar(self):
        return f"https://ui-avatars.com/api/?name={self.name.replace(' ',  '+')}"    

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