import click
import hashlib
from flask import Flask, request, jsonify
import gzip
from io import BytesIO


app = Flask(__name__)

@app.route('/code/<int:code>')
def code(code):
    return (f"code is {code}", code, {})


@app.route('/do_checksum', methods=['POST', 'PUT'])
def do_checksum():
    stream = request.stream
    if request.headers.get('Content-encoding') == 'gzip':
        stream = BytesIO(gzip.decompress(stream.read()))
    return checksum(stream)


def checksum(stream):
    # no need for actual security, just correctness
    sha = hashlib.sha1()
    while True:
        data = stream.read(1024 * 1024)
        if not data:
            break
        sha.update(data)
    return jsonify({
        "sha1": sha.hexdigest()
    })



@click.command()
@click.argument('port')
def main(port):
    app.run(port=port)

if __name__ == '__main__':
    main()
