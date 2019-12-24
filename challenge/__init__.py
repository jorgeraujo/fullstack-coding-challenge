from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from unbabel.api import UnbabelApi
from config import UNBABEL_API_USERNAME, UNBABEL_API_KEY, SQLALCHEMY_DATABASE_URI
import os


# Create instances of the extensions
db = SQLAlchemy()
socketio = SocketIO()
ma = Marshmallow()

#initialize unbabel api 
uapi = UnbabelApi(UNBABEL_API_USERNAME, UNBABEL_API_KEY, sandbox=True)


def initialize_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    migrate = Migrate(app, db)
    socketio.init_app(app)
    

def register_blueprints(app):
    from challenge.translation_api import translation_api
    from challenge.translation_page import translation_page
    app.register_blueprint(translation_page, url_prefix='')
    app.register_blueprint(translation_api, url_prefix='/')


# Application Factory Function
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    initialize_extensions(app)
    register_blueprints(app)
    return app

