from flask import jsonify


def API_RESPONSE(rv=None, metadata=None, error=None):
    return jsonify({
        'error': error,
        'result': rv,
    })

API_SUCCESS = API_RESPONSE
