from .. import models
from .caching import cache
from sqlalchemy.orm.exc import NoResultFound

def get_or_create_subject_instance(name, product, version, revision):
    return _get_or_create_subject_instance(name, product, version, revision)

@cache.cache_on_arguments()
def _get_or_create_subject_instance(name, product, version, revision):
    return _get_or_create(models.SubjectInstance, subject_id=_get_or_create_subject_id(name), revision_id=_get_or_create_revision_id(product, version, revision))

@cache.cache_on_arguments()
def _get_or_create_subject_id(name):
    return _get_or_create(models.Subject, name=name).id

@cache.cache_on_arguments()
def _get_or_create_revision_id(product, version, revision):
    return _get_or_create(models.ProductRevision, revision=revision, product_version_id=_get_or_create_version_id(product, version)).id

@cache.cache_on_arguments()
def _get_or_create_version_id(product, version):
    return _get_or_create(models.ProductVersion, product_id=_get_or_create_product_id(product), version=version).id

@cache.cache_on_arguments()
def _get_or_create_product_id(product):
    return _get_or_create(models.Product, name=product).id

def _get_or_create(model, **kwargs):
    try:
        returned = model.query.filter_by(**kwargs).one()
    except NoResultFound:
        returned = model(**kwargs)
        models.db.session.add(returned)
        models.db.session.commit()
    return returned
