import os

import slash

_current = 0

@slash.fixture(autouse=True)
def interrupt():
    global _current
    _current += 1
    if _current == 5:
        os._exit(0)


def test_1():
    pass

def test_2():
    pass

def test_3():
    pass

def test_4():
    pass

def test_5():
    pass

def test_6():
    pass

def test_7():
    pass

def test_8():
    pass

def test_9():
    pass

def test_10():
    pass
