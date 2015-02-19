import requests
from flask import abort
from models import Test, TestMetadata
from sqlalchemy import or_, func


def filter_test_metadata(query, field_name, value):
    field_name = field_name.replace('+', ' ')
    value = value.replace('+', ' ')
    splitted = field_name.split('.')

    # has to have at least metadata.XXX
    if len(splitted) < 2:
        abort(requests.codes.bad_request)
    if splitted[0] != 'metadata':
        abort(requests.codes.bad_request)

    if len(splitted) == 2:  # exactly 1 key
        key = splitted[1]
    else:
        key = tuple(splitted[1:])
    if value:
        return query.filter(Test.id == TestMetadata.test_id).filter(TestMetadata.metadata_item[key].astext == value)
    else:
        #wanted to use a nice has_key but it doesn't support nested keys
        expr = TestMetadata.metadata_item[key]
        return query.filter(Test.id == TestMetadata.test_id).filter(expr != None)


