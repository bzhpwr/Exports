# Copyright (C) 2006 Samuel Abels, http://debain.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import os
from urllib import quote

class Url(object):
    """
    Represents an URL, retrieve via the request handler API.
    """

    def __init__(self, request, path = ''):
        """
        Constructor.

        @type  request: Request
        @param request: The associated request.
        @type  path: str
        @param path: The initial path, passed to set_path().
        """
        self.request = request
        self.vars    = []
        self.rewrite = self.request.get_data().get_bool('rewrite')
        self.set_path(path)
        if self.rewrite:
            self.set_var('rewrite', 1)


    def set_path(self, path):
        """
        @type  path: str
        @param path: The initial path, passed to set_path().
        """
        self.path = str(path)


    def find_var(self, key, value = None):
        for pos, (my_key, my_value) in enumerate(self.vars):
            if my_key != key:
                continue
            if value is not None and my_value != value:
                continue
            return pos
        return -1


    def set_var(self, key, value):
        key, value = str(key), str(value)
        pos = self.find_var(key)
        if pos >= 0 and value is None:
            del self.vars[pos]
        elif pos >= 0:
            self.vars[pos] = (key, value)
        elif value is not None:
            self.vars.append((key, value))


    def get_string(self):
        """
        Returns the URL as a string. Note that the object is mod_rewrite
        aware, and depending on whether the rewrite GET variable is set,
        appends either a path or query variables to the path.

        @rtype:  string
        @return: The URL.
        """
        if len(self.vars) == 0:
            return self.path
        vars = []
        for key, value in self.vars:
            vars.append('%s=%s' % (quote(key), quote(value)))
        if self.rewrite:
            return self.path + '/' + '/'.join(vars) #FIXME: Improve rewriting.
        return self.path + '?' + '&'.join(vars)
