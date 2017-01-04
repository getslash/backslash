import gossip


@gossip.register('slash.session_start')
def session_start():
    raise KeyboardInterrupt()


def test_1():
    pass
