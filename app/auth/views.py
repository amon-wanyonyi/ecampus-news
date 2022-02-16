from crypt import methods
from flask import render_template
from . import auth

@auth.route('/login', methods = ['GET', 'POST'])
def index():
    return render_template('login.html')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template('signup.html')    