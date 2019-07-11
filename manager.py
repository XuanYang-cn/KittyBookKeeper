from flask_script import Manager
from flask_migrate import MigrateCommand

from kitty import db, create_app

manager = Manager(create_app())
manager.add_command('db', MigrateCommand)


@manager.command
def create_all():
    db.create_all()


@manager.command
def drop_all():
    db.drop_all()


@manager.command
def recreate_all():
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()
