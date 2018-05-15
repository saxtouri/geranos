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


class APIError(Exception):
    """Internal Server Error"""
    status_code = 500

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message if message is not None else self.__doc__
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload or dict()


class Forbidden(APIError):
    """Forbidden"""
    status_code = 403


class BadRequest(APIError):
    """Bad request"""
    status_code = 400
