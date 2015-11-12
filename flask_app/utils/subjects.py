from .. import models
from .caching import cache
from .db_utils import get_or_create

def get_or_create_subject_instance(name, product, version, revision):
    return models.SubjectInstance.query.get(
        _get_or_create_subject_instance_id(name, product, version, revision))

@cache.cache_on_arguments()
def _get_or_create_subject_instance_id(name, product, version, revision):
    return get_or_create(models.SubjectInstance, subject_id=_get_or_create_subject_id(name), revision_id=_get_or_create_revision_id(product, version, revision)).id

@cache.cache_on_arguments()
def _get_or_create_subject_id(name):
    return get_or_create(models.Subject, name=name).id

@cache.cache_on_arguments()
def _get_or_create_revision_id(product, version, revision):
    return get_or_create(models.ProductRevision, revision=revision, product_version_id=_get_or_create_version_id(product, version)).id

@cache.cache_on_arguments()
def _get_or_create_version_id(product, version):
    return get_or_create(models.ProductVersion, product_id=_get_or_create_product_id(product), version=version).id

@cache.cache_on_arguments()
def _get_or_create_product_id(product):
    return get_or_create(models.Product, name=product).id
