import json

def sanitize_json(json_dict):
    """Sanitizes json objects for safe storage in Postgres
    """
    returned = json.dumps(json_dict)
    returned = returned.replace('\\u0000', '\\\\x00')
    return json.loads(returned)
