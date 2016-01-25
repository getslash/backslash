import click
import logbook

from .bootstrapping import requires_env


@click.group()
def user():
    pass

@user.group()
def token():
    pass

@token.command()
@click.argument('user_email')
@requires_env("app")
def create(user_email):
    from flask_app.app import create_app
    from flask_app import models
    from flask_app.auth import get_or_create_user
    from flask_app import models
    from flask_app.blueprints.runtoken import create_new_runtoken

    app = create_app()

    with app.app_context():
        user = get_or_create_user({'email': user_email})
        if user.run_tokens.all():
            print('User', user_email, 'already has tokens. Skipping...')
            return
        token = create_new_runtoken(user)
        print('Created token', token, 'for', user_email)
        models.db.session.commit()


@token.command()
@requires_env("app")
def list():
    from flask_app.app import create_app
    from flask_app import models

    app = create_app()

    with app.app_context():
        for user in models.User.query.all():
            tokens = user.run_tokens.all()
            if not tokens:
                continue
            print(user.email, tokens[0].token)
