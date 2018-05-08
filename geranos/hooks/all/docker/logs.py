# Copyright (C) 2018 GRNET S.A.
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
import yaml
import logging

logger = logging.getLogger(__name__)


def get(nodes_file, request):
    """Return the logs"""
    args = dict(request.args.items())
    try:
        container = args.pop('container')
    except KeyError:
        raise KeyError('No container on URL arguments')

    with open(nodes_file) as f:
        nodes = yaml.load(f)
        for _, ips in nodes.items():
            for ip in ips:
                print('ssh root@{ip} docker logs {container}'.format(
                    ip=ip, container=container))
        return '{}'.format(nodes)

    return 'docker logs {}'.format(container)

