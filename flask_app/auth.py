from flask.ext.security import Security, SQLAlchemyUserDatastore

from .app import app
from .models import Role, User, db

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(app, user_datastore, register_blueprint=False)
