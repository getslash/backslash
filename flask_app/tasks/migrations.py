import logbook
from .main import queue, needs_app_context
from .. import models
from ..utils import get_current_time

_logger = logbook.Logger(__name__)


@queue.task
@needs_app_context
def start_live_migrations():
    pending = models.BackgroundMigration.query.filter_by(started=False).all()
    started = models.BackgroundMigration.query.filter_by(started=True, finished=False).all()
    if pending and not started:
        do_live_migrate.delay()


@queue.task
@needs_app_context
def do_live_migrate():
    for migration in models.BackgroundMigration.query\
                                             .filter_by(finished=False)\
                                             .order_by(models.BackgroundMigration.id.asc()).all():
        if not migration.started:
            migration.started = True
            migration.started_time = get_current_time()
            num_rows = models.db.session.execute(migration.remaining_num_items_query).scalar()
            migration.remaining_num_objects = num_rows
            migration.total_num_objects = num_rows
            models.db.session.commit()

        num_objects = migration.remaining_num_objects

        _logger.debug('Running migration: {.name}...', migration)

        while True:
            result = models.db.session.execute(migration.update_query,
                                               {'batch_size': migration.batch_size})
            if result.rowcount == 0:
                migration.remaining_num_objects = 0
                migration.finished = True
                migration.finished_time = get_current_time()
            else:
                num_objects = max(0, num_objects - result.rowcount)
                migration.remaining_num_objects = num_objects

            models.db.session.commit()
            if result.rowcount == 0:
                break
