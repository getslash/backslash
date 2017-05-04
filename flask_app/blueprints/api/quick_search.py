from sqlalchemy.sql import text

from flask import current_app

from .blueprint import API

from ...models import db


@API(generates_activity=False)
def quick_search(term: str):
    term = term.strip()
    num_hits = 10
    query = text(
        """SELECT * from
             ((select name as key, name, 'subject' as type from subject) UNION

              (select email as key, CASE WHEN first_name is NULL THEN email
                          ELSE (first_name || ' ' || last_name || ' (' || email || ')') END as name, 'user' as type from "user")) u
        where u.name ilike :term limit :num_hits""").params(
            term='%{}%'.format(term),
            num_hits=num_hits,
    )
    returned = []
    for res in db.session.execute(query):
        returned.append({
            'type': res['type'],
            'key': res['key'],
            'name': res['name'],
            'route': 'user.sessions' if res['type'] == 'user' else res['type']})
    return returned
