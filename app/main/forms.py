from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, IntegerField, EmailField,BooleanField
from wtforms.validators import InputRequired

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])
    pinned = BooleanField('Pinned')

class EditBlogForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])
    pinned = BooleanField('Pinned')

# comment form
class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a Comment', validators=[InputRequired()])


class ProfileForm(FlaskForm):
    """Profile form"""
    email = EmailField('Email',validators=[InputRequired()])
    name = StringField('Name',validators=[InputRequired()])
    about = TextAreaField('About')