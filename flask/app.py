# -*- coding: utf-8 -*-

import base64

from flask import (
    Flask,
    Response,
    request,
    stream_with_context,
)
import requests

app = Flask(__name__)

ALL_METHODS = [
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
]
MONITOR_SESSION = requests.Session()
CHUNK_SIZE = 16 * 1024

def chunked_response_iterator(resp, native_chunk_support, line_based):
    """
    Return stream with chunked encoding if native_chunk_support is True.
    """
    if line_based:
        for chunk in resp.iter_lines(1):
            chunk += '\n'
            if native_chunk_support:
                yield chunk
            else:
                yield hex(len(chunk))[2:] + '\r\n' + chunk + '\r\n'
        if not native_chunk_support:
            yield '0\r\n\r\n'
    else:
        for chunk in resp.iter_content(CHUNK_SIZE):
            if native_chunk_support:
                yield chunk
            else:
                yield hex(len(chunk))[2:] + '\r\n' + chunk + '\r\n'
        if not native_chunk_support:
            yield '0\r\n\r\n'


@app.route('/monitor', defaults={'url': ''}, methods=ALL_METHODS)
@app.route('/monitor/<path:url>', methods=ALL_METHODS)
def monitor_proxy(url):
    params = dict(request.args.items())
    headers = dict(request.headers.items())
    server = headers.get('Host', 'localhost:5000')
    authorization = headers.get('Authorization', '')
    if authorization.startswith('Basic '):
        userpass = authorization[len('Basic '):]
        user = base64.b64decode(userpass)
        userpass = user.split(':')
        if len(userpass) == 2:
            headers.update({
                'x-kibana-user': userpass[0],
            })
    headers.update({
        'Referer': 'http://{}/monitor/{}'.format(server, url)
    })
    addr = 'http://kibana:5601/' + url
    req = MONITOR_SESSION.request(
        request.method,
        addr,
        stream=True,
        headers=headers,
        params=params,
        data=request.data
    )
    # content_type = req.headers.get('Content-type', '')
    # line_based = content_type.startswith(('text/', 'application/json'))
    # gunicorn/werkzeug supports chunked encoding, no need to
    # encode it manually
    # native_chunk_support = (
    #     'gunicorn' in request.environ['SERVER_SOFTWARE'] or
    #     'Werkzeug' in request.environ['SERVER_SOFTWARE']
    # )
    headers = dict(req.headers)
    if headers.get('transfer-encoding', None) == 'chunked':
        stream_reader = chunked_response_iterator(req, True, False)
        # do not pass the gzip header if provided by kibana
        # because content is uncompressed when reading the stream.
        headers.pop('content-encoding', None)
    else:
        stream_reader = stream_with_context(req.iter_content())
    return Response(stream_reader, headers=headers,
                    direct_passthrough=True, status=req.status_code)


@app.route('/monitor/', methods=ALL_METHODS)
def monitor_proxy_home():
    return monitor_proxy('')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
