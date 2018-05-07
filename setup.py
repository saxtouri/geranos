#!/usr/bin/env python

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

from setuptools import setup
from geranos import __version__

setup(
    name='geranos',
    version=__version__,
    description=('A REST API to handle docker containers froma distance'),
    long_description=open('README.md').read(),
    url='',
    download_url='',
    license='GPLv3',
    author='Stavros Sachtouris',
    author_email='saxtouri@admin.grnet.gr',
    maintainer='Stavros Sachtouris',
    maintainer_email='saxtouri@admin.grnet.gr',
    packages=['geranos', ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'geranos-server = geranos.daemon:cli',
        ]
    },
    install_requires=['paramiko', 'Flask', 'PyYAML', ]
)
