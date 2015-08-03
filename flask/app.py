# -*- coding: utf-8 -*-

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

@app.route('/monitor', defaults={'url': ''}, methods=ALL_METHODS)
@app.route('/monitor/<path:url>', methods=ALL_METHODS)
def monitor_proxy(url):
    params = dict(request.args.items())
    headers = dict(request.headers.items())
    addr = 'http://kibana:5601/' + url
    req = requests.get(
        addr,
        stream=True,
        headers=headers,
        params=params,
        data=request.data
    )
    return Response(
        stream_with_context(req.iter_content()),
        content_type=req.headers['content-type']
    )

@app.route('/monitor/', methods=ALL_METHODS)
def monitor_proxy_home():
    return monitor_proxy('')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
