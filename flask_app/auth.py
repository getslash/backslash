from flask import request, jsonify, Blueprint
from flask.ext.security import SQLAlchemyUserDatastore
from flask_security.utils import verify_and_update_password, login_user
from flask_security.decorators import auth_token_required

from .models import Role, User, db


auth = Blueprint("auth", __name__, template_folder="templates")

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


@auth.route("/login", methods=['POST'])
def login():
    data = request.json
    user = user_datastore.get_user(data['email'])
    if not user:
        return "Invalid username or password", 401
    if not verify_and_update_password(data['password'], user):
        return "Invalid username or password", 401

    login_user(user)
    return jsonify({
        'auth_token': user.get_auth_token(),
        'email': user.email
    })


@auth.route("/reauth", methods=['POST'])
@auth_token_required
def reauth():
    return jsonify(request.json)
