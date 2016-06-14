import slash

@slash.hooks.session_end.register
def callback(**_):
    raise Exception()
