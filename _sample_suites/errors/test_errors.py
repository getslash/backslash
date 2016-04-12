import slash

def test_1():
    for i in range(30):
        slash.logger.warning('Warning number {}', i)

def test_2():
    f()

def test_3():
    for i in range(30):
        slash.add_error('sample error #{}'.format(i))

def test_4():
    raise Exception('this is a very long message ' * 100)

def f():
    var = 2
    g()

def g():
    var = 3
    h()

def h():
    1/0
