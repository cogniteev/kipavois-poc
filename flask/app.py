# -*- coding: utf-8 -*-
from flask import (
    Flask,
    request,
)

import kipavois

app = Flask(__name__)


def authorize_header_user():
    authorization = request.headers.get('Authorization', '')
    if authorization.startswith('Basic '):
        userpass = authorization[len('Basic '):]
        user = base64.b64decode(userpass)
        userpass = user.split(':')
        if len(userpass) == 2:
            return userpass[0]


def host_referer():
    server = request.headers.get('Host', 'localhost:5000')
    return 'http://{}'.format(server)


app.register_blueprint(
    kipavois.flask_blueprint(
        get_user=authorize_header_user,
        kibana_addr='http://kibana:5601',
        get_referer=host_referer)
)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
