#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    manager.py
    ~~~~~~~~~~~

    flask manager script

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from flask_script import Server, Manager, prompt_bool
from flask_migrate import Migrate,MigrateCommand
from app_info import app,db
from bayMax import sql_model

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command("runserver", Server('0.0.0.0', port=5000))
manager.add_command("migratedb",MigrateCommand)

@manager.shell
def make_shell_context():
    """
    Create a python GLI

    :return: Default import object
    type:'Dict'
    """
    return dict(app=app)
@manager.command
def createall():
    db.create_all(bind=['knowladge_map'])
@manager.command
def dropall():

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == "__main__":
    manager.run()
