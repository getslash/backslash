from flask import request, jsonify
from flask.ext.security.utils import encrypt_password
from .app import app
from .auth import user_datastore


def _has_users():
    return user_datastore.user_model.query.count() > 0


@app.route("/setup", methods=['POST'])
def setup_submit():
    if _has_users():
        return "This site already has users defined in it", 403

    data = request.json
    user_datastore.create_user(email=data['email'], password=encrypt_password(data['password']))
    user_datastore.db.session.commit()
    return ""


@app.route("/has_users")
def has_users():
    return jsonify({"hasUsers": _has_users()})
