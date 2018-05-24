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
import logging
from geranos.utils import ssh_exec, pop_argument, log_func, format_args
from geranos.hooks.heavy import get_hosts

logger = logging.getLogger(__name__)


@log_func
def _run(nodes_file, request, cmd):
    args, results = request.args.to_dict(), dict()
    cmd = cmd.format(args=format_args(args))

    for host in get_hosts(nodes_file):
        try:
            results[host['hostname']] = ssh_exec(cmd, **host)
        except Exception as e:
            logger.info('Failed {} with {} {}'.format(host, type(e), e))
            results[host['hostname']] = dict(
                status=1, stdout='', stderr='Connection error', cmd=cmd)
    return results


@log_func
def get(nodes_file, request):
    """Return the logs"""
    return _run(nodes_file, request, 'docker ps {args}')
