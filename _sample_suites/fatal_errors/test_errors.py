import slash


def test_1():
    global first_error
    first_error = slash.add_error('First error')


def test_2():
    pass


def test_3():
    first_error.mark_fatal()


def test_4():
    pass
