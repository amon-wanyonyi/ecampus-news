from email.policy import default
from app import create_app, db
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role
from decouple import config

import os

app = create_app(config('ENV', default="development"))

manager = Manager(app)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db, User=User, Role=Role)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db)


migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()