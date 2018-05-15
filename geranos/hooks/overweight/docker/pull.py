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
from geranos.utils import ssh_exec, pop_argument
from geranos.hooks.overweight import get_hosts

logger = logging.getLogger(__name__)


def _run(nodes_file, request, cmd):
    args, results = request.args.to_dict(), dict()
    image = pop_argument(args, 'image')
    cmd = cmd.format(
        image=image,
        args=' '.join(['--{}={}'.format(a, args[a]) for a in args]))

    for host in get_hosts(nodes_file):
        try:
            results[host['hostname']] = ssh_exec(cmd, **host)
        except Exception as e:
            logger.info('Failed {} with {} {}'.format(host, type(e), e))
            results[host['hostname']] = dict(
                status=1, stdout='', stderr='Connection error', cmd=cmd)
    return results


def post(nodes_file, request):
    """perform a docker pull"""
    return _run(nodes_file, request, 'docker pull {image} {args}')


def put(nodes_file, request):
    """run a docker pull, let it run without waiting for it to finish"""
    return _run(nodes_file, request, 'docker pull {image} {args}&')


def get(nodes_file, request):
    """Check the status of a docker pull
    No information about the results of the pull, just if it is stull running
    Possible states:
        ACTIVE: the image is being pulled currently
        INACTIVE: the particular image in not pulled
    """
    r = _run(nodes_file, request,
        cmd='ps aux|grep "docker pull {image}"|grep -v "grep"')
    print(r)
    return r
