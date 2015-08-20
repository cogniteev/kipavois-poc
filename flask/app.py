# -*- coding: utf-8 -*-
import base64

from flask import (
    Flask,
    request,
)

import kipavois

app = Flask(__name__)


def authorize_header_user():
    """Retrieve user name in the 'Authorization' HTTP header.
    If the user is 'admin', then return `None`, meaning that the user
    has administrative permissions, and there is no restriction.
    """
    authorization = request.headers.get('Authorization', '')
    if authorization.startswith('Basic '):
        userpass = authorization[len('Basic '):]
        user = base64.b64decode(userpass)
        userpass = user.split(':')
        if len(userpass) == 2:
            user = userpass[0]
            if user != 'admin':
                return user


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
