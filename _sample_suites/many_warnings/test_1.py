import slash

def test_1():
    for i in range(100):
        slash.logger.warning('warning {}', i)
