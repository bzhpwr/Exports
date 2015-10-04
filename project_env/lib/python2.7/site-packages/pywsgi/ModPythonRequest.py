# Copyright (C) 2008 Samuel Abels, http://debain.org
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
import cgi
from Request import Request
from Table   import Table

class ModPythonRequest(Request):
    """
    This adapter implements a bridge to mod_python.
    """

    def __init__(self, request, **kwargs):
        from mod_python      import apache, Cookie
        from mod_python.util import FieldStorage
        Request.__init__(self, **kwargs)
        self.cookie_mod    = Cookie
        self.request       = request
        self.env           = apache.build_cgi_env(request)
        self.the_get_data  = self.__read_get_data()
        self.the_post_data = self.__read_post_data()
        self.the_cookies   = self.__read_cookies()


    def get_name(self):
        return 'mod_python'


    def __unpack_data(self, data):
        result = {}
        for key, field in data.items():
            result[key] = field.value
        return result


    def __read_get_data(self):
        query = cgi.parse_qs(self.get_env('QUERY_STRING'))
        data  = {}
        for key, value in query.iteritems():
            data[key] = value[0]
        return Table(data, allow_duplicates = False, readonly = True)


    def __read_post_data(self):
        return Table(self.__unpack_data(self.request.form),
                     allow_duplicates = False,
                     readonly         = True)


    def __read_cookies(self):
        data = self.__unpack_data(self.cookie_mod.get_cookies(self.request))
        return Table(data, allow_duplicates = False, readonly = True)


    def get_env(self, key):
        return self.env[key]


    def get_data(self):
        return self.the_get_data


    def has_post_data(self):
        return self.request.method == 'POST'


    def post_data(self):
        return self.the_post_data


    def set_cookie(self, key, value, expires = None):
        cookie = self.cookie_mod.Cookie(key, value)
        if expires:
            cookie.expires = expires
        self.cookie_mod.add_cookie(self.request, cookie)


    def cookies(self):
        return self.the_cookies


    def add_header(self, key, value):
        return self.request.headers_out.add(key, value)


    def get_headers(self):
        return self.request.headers_out.items()


    def flush(self):
        self.request.content_type = self.content_type
        self.request.write(self.data)
        data = self.data
        self.data = ''
        return [data]


    def handle_exception(self):
        raise


    def handle(self, func):
        func(self)
        self.flush()
