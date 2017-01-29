import gossip


@gossip.register('slash.test_end')
def session_start():
    raise KeyboardInterrupt()


def test_1():
    pass
