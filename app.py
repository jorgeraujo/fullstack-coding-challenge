from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from views import translation_page, translation_api
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from database import db
    db.init_app(app)
    from marsh_mallow import ma
    ma.init_app(app)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    migrate = Migrate(app, db)
    app.register_blueprint(translation_page, url_prefix='')
    app.register_blueprint(translation_api, url_prefix='/')
    return app

app = create_app()

if __name__ == '__main__':
    app.run()