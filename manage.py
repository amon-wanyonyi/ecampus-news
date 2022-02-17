from email.policy import default
from app import create_app, db
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Notification, User, Role
from app.main.forms import BlogForm
from decouple import config


app = create_app(config('ENV', default="development"))

manager = Manager(app)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db, User = User, Role = Role, Notification = Notification)

@manager.command
def seed():
    "Add seed data to the database."
    roles = [Role(name="Admin"), Role(name="User")]
    
    db.session.add_all(roles)
    db.session.commit()

@app.context_processor
def inject_user():
    blog_form = BlogForm()
    return dict(blog_form=blog_form)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()