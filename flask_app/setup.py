from flask import render_template, abort, redirect, Blueprint, jsonify, request
from flask_wtf import Form
from flask.ext.security.utils import encrypt_password
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

from .auth import user_datastore

setup = Blueprint("setup", __name__, template_folder="templates")

def _has_users():
    return user_datastore.user_model.query.count() > 0


@setup.route("/setup", methods=['POST'])
def setup_submit():
    if _has_users():
        return "This site already has users defined in it", 403

    data = request.json
    user_datastore.create_user(email=data['email'], password=encrypt_password(data['password']))
    user_datastore.db.session.commit()
    return ""


@setup.route("/has_users")
def has_users():
    return jsonify({"hasUsers": _has_users()})
