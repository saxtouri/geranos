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
from geranos import errors
from geranos.utils import ssh_exec, pop_rsa_key, pop_argument

logger = logging.getLogger(__name__)


def _run(nodes_file, request, cmd):
    args, results = request.args.to_dict(), dict()
    container = pop_argument(args, 'container')
    cmd = cmd.format(
        container=container,
        args=' '.join(['--{}={}'.format(a, args[a]) for a in args]))

    with open(nodes_file) as f:
        nodes = yaml.load(f)
    rsa_key_file = pop_rsa_key(nodes)

    ips = []
    for ip_lists in nodes.values():
        ips += ip_lists
    for ip in set(ips):
        print(ip)
        try:
            results[ip] = ssh_exec(
                hostname=ip, username='root',
                rsa_key_file=rsa_key_file, cmd=cmd)
        except Exception as e:
            logger.info('Failed with {} {}'.format(type(e), e))
            results[ip] = dict(
                status=1, stdout='', stderr='Connection error', cmd=cmd)
    return results


def get(nodes_file, request):
    """Return the logs"""
    return _run(nodes_file, request, 'docker logs {container} {args}')
