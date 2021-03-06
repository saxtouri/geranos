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
from functools import wraps
from geranos import errors
from paramiko import SSHClient, RSAKey, AutoAddPolicy

logger = logging.getLogger(__name__)


def log_func(func):
    @wraps(func)
    def wrap(*args, **kw):
        func_name = func.__name__
        args_str = ' '.join(['{}'.format(a) for a in args])
        kw_str = ' '.join(['{k}={v}'.format(k=k, v=v) for k, v in kw.items()])
        logger.debug('{}: {} {}'.format(func_name, args_str, kw_str))
        print('  {}: {} {}'.format(func_name, args_str, kw_str))
        return func(*args, **kw)
    return wrap


@log_func
def ssh_exec(cmd, hostname, username, rsa_key_file):
    try:
        pkey = RSAKey.from_private_key_file(rsa_key_file)
    except Exception as e:
        logger.info('Failed to read RSA Key, {} {}'.format(type(e), e))
        raise
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy)
    logger.info('ssh -i {rsa_key_file} {username}@{hostname} {cmd}'.format(
        rsa_key_file=rsa_key_file, hostname=hostname, username=username,
        cmd=cmd))
    ssh.connect(hostname=hostname, username=username, pkey=pkey)
    _in, _out, _err = ssh.exec_command(cmd)
    status = _out.channel.recv_exit_status()
    results = dict(
        status=status, stdout=_out.read(), stderr=_err.read(), command=cmd)
    ssh.close()
    return results


@log_func
def pop_argument(args, argument):
    try:
        return args.pop(argument)
    except KeyError:
        raise errors.BadRequest('No {} on URL arguments'.format(argument))


@log_func
def format_args(args):
    return ' '.join(['--{}{}'.format(
        a, '={}'.format(args[a]) if args[a] else '') for a in args])
