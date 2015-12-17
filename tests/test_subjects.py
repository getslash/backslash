import functools
import requests
import pytest

from .utils import model_for


def test_start_session_with_subjects(client, subjects):
    session = client.report_session_start(
        subjects=subjects
    )
    _sorted = functools.partial(sorted, key=lambda d: d['name'])
    assert _sorted(session.refresh().subjects) == _sorted(dict(s) for s in subjects)


def test_add_subject(started_session, subjects, flask_app):
    started_session.add_subject(**subjects[0])

    with flask_app.app_context():
        session = model_for(started_session)
        assert len(session.subject_instances) == 1
        assert session.subject_instances[0].subject.name == subjects[0]['name']
        assert session.subject_instances[
            0].revision.product_version.product.name == subjects[0]['product']


def test_product_rendered_field(started_session, subjects):
    started_session.add_subject(**subjects[0])
    started_session.refresh()
    assert started_session.subjects == [subjects[0]]


@pytest.mark.parametrize('field_name', ['product', 'version', 'revision'])
def test_add_subject_deduplication(started_session, flask_app, field_name):
    first_subject = {'name': 'some_subject',
                     'product': 'car', 'version': '1', 'revision': 'a'}
    started_session.add_subject(**first_subject)
    second_subject = first_subject.copy()
    second_subject[field_name] = 'new_field_value'
    started_session.add_subject(**second_subject)

    with flask_app.app_context():
        session = model_for(started_session)
        assert len(session.subject_instances) == 2
        prod1, prod2 = [x.revision.product_version.product.id for x in session.subject_instances]
        ver1, ver2 = [x.revision.product_version.id for x in session.subject_instances]
        rev1, rev2 = [x.revision.id for x in session.subject_instances]

        if field_name == 'product':
            assert prod1 != prod2
            assert ver1 != ver2
            assert rev1 != rev2
        elif field_name == 'version':
            assert prod1 == prod2
            assert ver1 != ver2
            assert rev1 != rev2
        elif field_name == 'revision':
            assert prod1 == prod2
            assert ver1 == ver2
            assert rev1 != rev2
        else:
            raise NotImplementedError()  # pragma: no cover


def test_query_sessions_by_subjects(client, subjects):
    session1 = client.report_session_start(
        subjects=[subjects[0]]
    )
    session2 = client.report_session_start(
        subjects=[subjects[1]]
    )

    assert subjects[0].name != subjects[1].name

    _get = lambda subject: requests.get(client.api.url.add_path('rest/sessions').add_query_param('subject_name', subject.name)).json()['sessions']

    [s1] = _get(subjects[0])
    assert s1['id'] == session1.id

    [s2] = _get(subjects[1])
    assert s2['id'] == session2.id
