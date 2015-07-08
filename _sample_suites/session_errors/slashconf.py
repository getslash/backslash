import slash

@slash.hooks.after_session_start.register
def callback(**_):
    raise Exception()
