import json


def sanitize_json(json_dict, max_item_length=100):
    """Sanitizes json objects for safe storage in Postgres
    """
    if json_dict is None:
        return None

    returned = json.dumps(json_dict)
    returned = returned.replace('\\u0000', '\\\\x00')
    returned = json.loads(returned)
    for key, value in list(returned.items()):
        if isinstance(value, (str, bytes)) and len(value) > max_item_length:
            remainder = 5
            value = value[:max_item_length - remainder - 3] + '...' + value[-remainder:]
            returned[key] = value

    return returned
