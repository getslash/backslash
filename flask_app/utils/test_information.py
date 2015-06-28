from .. import models
from .caching import cache
from .db_utils import get_or_create

def get_or_create_test_information_id(*, file_name, class_name, name):
    return _get_or_create_test_information_id(file_name, class_name, name)

@cache.cache_on_arguments()
def _get_or_create_test_information_id(file_name, class_name, name):
    return get_or_create(models.TestInformation, file_name=file_name, class_name=class_name, name=name).id
