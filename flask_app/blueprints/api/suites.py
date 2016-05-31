import requests

from flask.ext.security import current_user
from flask.ext.simple_api import error_abort
from sqlalchemy.exc import IntegrityError

from ...models import Suite, db, SuiteItem
from ...utils.rendering import render_api_object
from .blueprint import API


@API(require_real_login=True)
def create_suite(name: str):
    if not name:
        error_abort('Invalid suite name')
    returned = Suite(name=name, owner_id=current_user.id)
    db.session.add(returned)
    try:
        db.session.commit()
    except IntegrityError:
        error_abort('Added suite will result in a naming conflict',
                    code=requests.codes.conflict)
    return returned


@API(require_real_login=True)
def get_suite_items(suite_id: int):
    return {
        'items': [
            render_api_object(item)
            for item in SuiteItem.query.filter(SuiteItem.suite_id == suite_id).order_by(SuiteItem.position)
        ]
    }
