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
import yaml

logger = logging.getLogger(__name__)


def get_hosts(nodes_file):
    """:returns: {ip: {username=..., rsa_key_file=...}}"""
    logger.info('/all/heavy get_hosts')
    with open(nodes_file) as f:
        nodes = yaml.load(f)
    global_rsa = nodes.pop('rsa_key', None)
    global_username = nodes.pop('username', None)

    group = nodes.get('heavy')
    group_rsa = group.get('rsa_key', None)
    group_username = group.get('username', None)
    for host in group.get('hosts'):
        try:
            ip = host['ip']
        except KeyError:
            logger.debug('IP missing from host in {}'.nodes_file)
            continue
        rsa_key_file = host.get('rsa_key', group_rsa or global_rsa)
        if not rsa_key_file:
            logger.debug(
                'rsa_key_file unresolved for ip {ip} in {nodes_file}'.format(
                    ip=ip, nodes_file=nodes_file))
            continue
        username = host.get('username', group_username or global_username)
        if not username:
            logger.debug(
                'username unresolved for ip {ip} in {nodes_file}'.format(
                    ip=ip, nodes_file=nodes_file))
            continue
        yield dict(hostname=ip, rsa_key_file=rsa_key_file, username=username)
