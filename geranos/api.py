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

from flask import Flask, request, jsonify
import logging
import yaml
from geranos import errors

app = Flask(__name__)

# Server variables
CREDENTIALS = '/etc/geranos/credentials.yaml'
NODES = '/etc/geranos/nodes.yaml'

#Error handling

@app.errorhandler(errors.Forbidden)
@app.errorhandler(errors.BadRequest)
def handle_errors(error):
    response = jsonify(dict(message='{}'.format(error.message)))
    response.status_code = error.status_code
    return response


# utils
def _authenticate():
    """Check secret in headers"""
    api_key = request.headers.get('X-API-KEY')
    if api_key:
        with open(CREDENTIALS) as f:
            credentials = yaml.load(f.read())
        for credential in credentials:
            if credential.get('api-key') == api_key:
                return True
    raise errors.Forbidden('Access forbidden')

# API
@app.route('/nodes/all/docker/logs', methods=['GET', ])
def docker_logs():
    """GET /nodes/all/docker/logs
    Header:
        X-Auth-Secret: 
    Responses:
        200: OK
        403: FORBIDDEN
        400: BAD REQUEST
    """
    app.logger.info('GET /nodes/all/docker/logs')
    _authenticate()

    raise Exception("Not implemented", 501)


# For testing
if __name__ == '__main__':
    CREDENTIALS = 'credentials.yaml'
    NODES = 'nodes.yaml'
    app.config.from_object(__name__)
    app.run(debug=True, host='localhost', port='8080')
