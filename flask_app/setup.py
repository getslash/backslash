from flask import render_template, abort, redirect, Blueprint
from flask_wtf import Form
from flask.ext.security.utils import encrypt_password
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

from .auth import user_datastore

setup = Blueprint("setup", __name__, template_folder="templates")

class MyForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'password', validators=[DataRequired(), EqualTo("confirm_password", "Passwords must match")])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])


def _has_users():
    return user_datastore.user_model.query.count() > 0


@setup.route("/setup", methods=['POST'])
def setup_submit():
    form = MyForm()
    if form.validate_on_submit():
        if _has_users():
            abort(403)

        user_datastore.create_user(email=form.email.data, password=encrypt_password(form.password.data))
        user_datastore.db.session.commit()
        return redirect("/")
    else:
        return render_template("setup.html", has_users=_has_users(), form=form, errors=form.errors)


@setup.route("/setup", methods=['GET'])
def setup_app():
    form = MyForm()
    return render_template("setup.html", has_users=_has_users(), form=form, errors={})
