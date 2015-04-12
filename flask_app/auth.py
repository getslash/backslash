from flask.ext.security import SQLAlchemyUserDatastore

from .models import Role, User, db

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
