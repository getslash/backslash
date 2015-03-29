import random

from flask.ext.security import Security, SQLAlchemyUserDatastore

from .app import app
from .models import Role, User, db

# Setup Flask-Security
app.config.setdefault('SECURITY_PASSWORD_SALT', str(random.random()))
app.config.setdefault('SESSION_PROTECTION', None)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(app, user_datastore)

