from uuid import uuid4

import pytest
from flask_app import models
from flask_app.auth import user_datastore
from flask_security.utils import verify_password


def test_setup_needed(clean_install, client):  # pylint: disable=unused-argument
    assert client.api.call.get_app_config()['setup_needed'] is True

def test_no_secret(client):
    cfg = client.api.call.get_app_config()
    for key in cfg:
        assert 'secret' not in key.lower()

def test_setup_no_longer_needed_after_setup(clean_install, client):  # pylint: disable=unused-argument
    client.api.call.setup(config={})
    assert client.api.call.get_app_config()['setup_needed'] is False


def test_setup_cannot_use_unknown_prefs(clean_install, client, db_context):  # pylint: disable=unused-argument
    client.api.call.setup(config={'bla': 2})
    with db_context():
        assert not models.AppConfig.query.filter_by(key='bla').count()


def test_admin_user_already_exists(client, clean_install, db_context, testuser_email):  # pylint: disable=unused-argument
    def get_password():
        with db_context():
            return models.User.query.filter_by(email=testuser_email).one().password
    old = get_password()
    client.api.call.setup(config={
        'admin_user_email': testuser_email,
        'admin_user_password': str(uuid4()),
    })
    assert get_password() == old


@pytest.mark.parametrize('with_clean_install', [True, False])
def test_admin_user_no_users(client, with_clean_install, request, db_context):  # pylint: disable=unused-argument

    admin_email = 'admin{}@somedomain.com'.format(uuid4())
    admin_password = '123456'

    with db_context():
        models.User.query.filter_by(email=admin_email).delete()
        models.db.session.commit()

    if with_clean_install:
        perform_clean_install(pytest_request=request, db_context=db_context)
    else:
        with db_context():
            some_user = models.User.query.first()
            user_datastore.add_role_to_user(some_user, 'admin')
            models.db.session.commit()
            assert models.User.query.filter(
                models.User.roles.any(models.Role.name == 'admin')).count()

    client.api.call.setup(config={
        'admin_user_email': admin_email,
        'admin_user_password': admin_password,
    })

    with db_context():
        query = models.User.query.filter_by(email=admin_email)
        if with_clean_install:
            user = query.one()
            assert user is not None
            assert verify_password(admin_password, user.password)
            assert user.password != admin_password
        else:
            assert not query.count()


##########################################################################
# Fixtures
##########################################################################


@pytest.fixture
def clean_install(request, db_context):
    perform_clean_install(request, db_context)


def perform_clean_install(pytest_request, db_context):
    with db_context():
        backup = {cfg.key: cfg.value for cfg in models.AppConfig.query.all()}
        roles = models.db.session.query(models.roles_users).all()
        models.db.session.execute(models.roles_users.delete())
        models.AppConfig.query.delete()
        models.db.session.commit()

    @pytest_request.addfinalizer
    def cleanup():              # pylint: disable=unused-variable
        with db_context():
            models.AppConfig.query.delete()
            for key, value in backup.items():
                models.db.session.add(models.AppConfig(key=key, value=value))
            models.db.session.execute(models.roles_users.delete())
            for role in roles:
                models.db.session.execute(models.roles_users.insert().values({
                    'user_id': role.user_id,
                    'role_id': role.role_id,
                }))
            models.db.session.commit()
