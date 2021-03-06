# Copyright 2018 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, request, jsonify, make_response
import yaml
from traceback import print_exc
from functools import wraps
from geranos import errors
import logging

app = Flask(__name__)
geranos_logger = logging.getLogger('geranos')

# Server variables
CREDENTIALS = '/etc/geranos/credentials.yaml'
NODES = '/etc/geranos/nodes.yaml'

# Common methods


@app.errorhandler(errors.Forbidden)
@app.errorhandler(errors.BadRequest)
def handle_errors(error):
    response = jsonify(dict(message='{}'.format(error.message)))
    response.status_code = error.status_code
    return response


def authenticate(func):
    """Check api key in headers before call"""
    @wraps(func)
    def wrap(*args, **kw):
        api_key = request.headers.get('X-API-KEY')
        if api_key:
            with open(CREDENTIALS) as f:
                credentials = yaml.load(f.read())
            try:
                actual_key = credentials.get('api-key')
            except KeyError:
                app.logger.info('No api-key in {}'.format(CREDENTIALS))
                raise errors.APIError()
            if actual_key == api_key:
                return func(*args, **kw)
        raise errors.Forbidden('Access forbidden')
    return wrap


# API
@app.route('/all/docker/logs', methods=['GET', ])
@authenticate
def all_docker_logs():
    """GET /all/docker/logs?container=<...>[&arg=value[...]]
    Header:
        X-API-KEY: <api key>
    Responses:
        200: OK
        403: FORBIDDEN
        400: BAD REQUEST
        500: Internal Server Error
    """
    app.logger.info('GET /all/docker/logs')
    from geranos.hooks.all.docker.logs import get
    try:
        r = get(NODES, request)
    except errors.APIError:
        raise
    except Exception as e:
        print_exc(e)
        raise errors.APIError()

    return make_response(jsonify(r), 200)


@app.route('/all/docker/pull', methods=['POST', 'PUT', 'GET'])
@authenticate
def all_docker_pull():
    """POST /all/docker/pull?image=<...>[&arg=value[...]]
    Header:
        X-API-KEY: <api key>
    Responses:
        200: OK
        403: FORBIDDEN
        400: BAD REQUEST
        500: Internal Server Error
    """
    app.logger.info('POST /all/docker/pull')
    if request.method == 'POST':
        from geranos.hooks.all.docker.pull import post as method
    elif request.method == 'PUT':
        from geranos.hooks.all.docker.pull import put as method
    elif request.method == 'GET':
        from geranos.hooks.all.docker.pull import get as method
    try:
        r = method(NODES, request)
    except Exception as e:
        if isinstance(e, errors.APIError):
            raise
        print_exc(e)
        raise errors.APIError()

    return make_response(jsonify(r), 201)


@app.route('/all/docker/ps', methods=['GET', ])
@authenticate
def all_docker_ps():
    """GET /all/docker/ps
    Header:
        X-API-KEY: <api key>
    Responses:
        200: OK
        403: FORBIDDEN
        400: BAD REQUEST
        500: Internal Server error
    """
    app.logger.info('GET /all/docker/logs')
    from geranos.hooks.all.docker.ps import get
    try:
        r = get(NODES, request)
    except errors.APIError:
        raise
    except Exception as e:
        print_exc(e)
        raise errors.APIError()

    return make_response(jsonify(r), 200)


@app.route('/all/cleanup', methods=['POST', ])
@authenticate
def all_cleanup():
    """POST /all/cleanup
    Header:
        X-API-KEY: <api key>
    Responses:
        200: OK
        403: FORBIDDEN
        400: BAD REQUEST
        500: Internal Server error
    """
    app.logger.info('GET /all/docker/logs')
    from geranos.hooks.all import cleanup
    r = dict()
    try:
        r['containers'] = cleanup.delete_old_containers(NODES, request)
        r['images'] = cleanup.delete_unused_images(NODES, request)
    except errors.APIError:
        raise
    except Exception as e:
        print_exc(e)
        raise errors.APIError()

    return make_response(jsonify(r), 200)


@app.route('/heavy/docker/pull', methods=['POST', 'PUT', 'GET'])
@authenticate
def heavy_docker_pull():
    """POST /heavy/docker/pull?image=<...>[&arg=value[...]]
    Header:
        X-API-KEY: <api key>
    Responses:
        200: OK
        403: FORBIDDEN
        400: BAD REQUEST
        500: Internal Server Error
    """
    app.logger.info('POST /heavy/docker/pull')
    if request.method == 'POST':
        from geranos.hooks.heavy.docker.pull import post as method
    elif request.method == 'PUT':
        from geranos.hooks.heavy.docker.pull import put as method
    elif request.method == 'GET':
        from geranos.hooks.heavy.docker.pull import get as method
    try:
        r = method(NODES, request)
    except Exception as e:
        if isinstance(e, errors.APIError):
            raise
        print_exc(e)
        raise errors.APIError()

    return make_response(jsonify(r), 201)


@app.route('/heavy/docker/ps', methods=['GET', ])
@authenticate
def heavy_docker_ps():
    """GET /heavy/docker/ps
    Header:
        X-API-KEY: <api key>
    Responses:
        200: OK
        403: FORBIDDEN
        400: BAD REQUEST
        500: Internal Server error
    """
    app.logger.info('GET /heavy/docker/logs')
    from geranos.hooks.heavy.docker.ps import get
    try:
        r = get(NODES, request)
    except errors.APIError:
        raise
    except Exception as e:
        print_exc(e)
        raise errors.APIError()

    return make_response(jsonify(r), 200)


# For testing
if __name__ == '__main__':
    CREDENTIALS = 'credentials.yaml'
    NODES = 'nodes.yaml'
    app.config.from_object(__name__)
    app.run(debug=True, host='localhost', port='8080')
else:
    # Support better GUnicorn logs
    gunicorn_logger = logging.getLogger('gunicorn.error')
    geranos_logger.handlers = gunicorn_logger.handlers
    geranos_logger.setLevel(gunicorn_logger.level)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
