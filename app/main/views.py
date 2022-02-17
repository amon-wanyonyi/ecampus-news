from . import main
from flask import render_template, url_for, abort, request, redirect, flash
from flask_login import login_required, current_user
from ..models import User
from .. import db
from ..emails import mail_message


@main.route('/')
def index():
    """main view function"""

    return render_template("index.html")
