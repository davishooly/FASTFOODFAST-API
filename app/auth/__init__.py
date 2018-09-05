from flask import Blueprint

from .auth_views import SignUp, Login

auth_blueprint = Blueprint("auth", __name__)
