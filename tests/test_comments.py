def test_comment(client, commentable, real_login):
    comment = 'comment here'
    commentable.post_comment(comment)
    [c] = _get_comments(client, commentable)
    assert c['comment'] == comment
    assert commentable.refresh().num_comments == 1

def test_delete_comment(client, commentable, real_login):
    comment = 'comment here'
    commentable.post_comment(comment)
    [c] = _get_comments(client, commentable)
    client.api.delete('/rest/comments/{}'.format(c['id']))
    assert commentable.refresh().num_comments == 0
    assert _get_comments(client, commentable) == []



def _get_comments(client, commentable):
    returned = client.api.get('/rest/comments', params={
        type(commentable).__name__.lower() + '_id': commentable.id
    })
    return returned['comments']
