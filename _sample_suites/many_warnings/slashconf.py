import slash

@slash.hooks.after_session_start.register
def callback(**_):
    for i in range(100):
        slash.logger.warning('session warning #{}', i)
