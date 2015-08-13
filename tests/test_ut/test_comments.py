import pytest


def test_post_comment(commentable, real_login):
    commentable.post_comment('some_text')

def test_delete_comment(commentable, real_login, client):
    resp = commentable.post_comment('some_text')
    client.delete_comment(comment_id=resp['id'])
    comments = list(commentable.get_comments())
    assert len(comments) == 1
    assert comments[0].deleted
    assert not comments[0].comment

@pytest.fixture(params=['session', 'test'])
def commentable(request, ended_session, ended_test):
    if request.param == 'session':
        return ended_session
    if request.param == 'test':
        return ended_test

    raise NotImplementedError() # pragma: no cover
