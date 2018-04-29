import errno
import flux
from flask import current_app
import itertools
import logbook
import os
from .main import queue, needs_app_context
from .. import models


_logger = logbook.Logger(__name__)

@queue.task
@needs_app_context
def delete_discarded_sessions(ignore_date=False):
    query = models.Session.query
    if ignore_date:
        query = query.filter(models.Session.delete_at != None)
    else:
        query = query.filter(models.Session.delete_at <= flux.current_timeline.time())
    while True:
        session = query.first()
        if not session:
            return
        tests = models.Test.query.filter(models.Test.session_id == session.id)
        for error in itertools.chain(session.errors, (error for t in tests for error in t.errors)):
            if not error.traceback_url:
                continue
            traceback_uuid = error.traceback_url.rsplit('/', 1)[-1]
            traceback_filename = os.path.join(
                current_app.config['TRACEBACK_DIR'], traceback_uuid[:2], traceback_uuid + '.gz')
            _logger.debug('Deleting error {.id} ({})', error, traceback_filename)
            try:
                os.unlink(traceback_filename)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
        _logger.debug('Deleting session {0.id} (Logical id {0.logical_id})', session)
        models.db.session.execute('DELETE FROM SESSION WHERE id = :id', {'id': session.id})
        models.db.session.commit()
