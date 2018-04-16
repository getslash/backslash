import flux
from .blueprint import API

from ...models import Replication, db
from ...utils.api_utils import requires_role
from ...tasks.replications import do_elasticsearch_replication

NoneType = type(None)


@API
@requires_role('admin')
def create_replication(url: str, username: (str, NoneType)=None, password: (str, NoneType)=None):
    returned = Replication(
        url=url, username=username, password=password)
    db.session.add(returned)
    db.session.commit()
    return returned


@API
@requires_role('admin')
def delete_replication(id: int):
    obj = Replication.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()


@API
@requires_role('admin')
def start_replication(id: int):
    obj = Replication.query.get_or_404(id)
    obj.paused = False
    obj.last_chunk_finished = flux.current_timeline.time()
    obj.last_error = None
    db.session.commit()
    do_elasticsearch_replication.delay(obj.id)

@API
@requires_role('admin')
def pause_replication(id: int):
    obj = Replication.query.get_or_404(id)
    obj.paused = True
    db.session.commit()

@API
@requires_role('admin')
def reset_replication(id: int):
    obj = Replication.query.get_or_404(id)
    obj.reset()
    db.session.commit()
