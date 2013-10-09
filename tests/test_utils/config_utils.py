from testconfig import config

_YES_VALUES = {"y", "yes", "true"}
_NO_VALUES = {"n", "no", "false"}

def get_config_int(key, default):
    return int(config.get(key, default))

def get_config_boolean(key, default):
    value = config.get(key, None)
    if value is None:
        return default
    value = value.lower()
    assert value in _YES_VALUES or value in _NO_VALUES, "Invalid boolean value"
    return value in _YES_VALUES
