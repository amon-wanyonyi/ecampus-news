from flask import render_template
from . import main

@main.route('/about')
def index():
    return render_template('about.html')