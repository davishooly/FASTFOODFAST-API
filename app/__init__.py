from flask import Flask
from flask_restful import Api
from instance.config import app_config
from .admin.admin_views import Foods

# chop config files


def create_app(config_mode):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_mode])
    app.config.from_pyfile('config.py')

    from .admin import admin_blueprint as admin_blp
    admin = Api(admin_blp)
    app.register_blueprint(admin_blp, url_prefix="/api/v1")

    admin.add_resource(Foods, '/fooditems')
    return app
