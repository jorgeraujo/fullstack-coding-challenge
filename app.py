from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from views import translation_page
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from database import db
    db.init_app(app)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    migrate = Migrate(app, db)
    app.register_blueprint(translation_page, url_prefix='')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()