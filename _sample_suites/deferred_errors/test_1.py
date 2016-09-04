import slash

def test_1():
    result = slash.context.result
    def cleanup():
        result.add_error('this is a deferred error from test_1')
    slash.add_cleanup(cleanup, scope='module')

def test_2():
    pass

def test_3():
    pass
