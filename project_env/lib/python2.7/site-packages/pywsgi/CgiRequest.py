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
import os, cgi
from Request import Request
from Table   import Table

class CgiRequest(Request):
    """
    This adapter implements a bridge to plain old mod_cgi.
    """

    def __init__(self, **kwargs):
        Request.__init__(self, **kwargs)
        self.headers       = []
        self.headers_sent  = False
        self.the_get_data  = self.__read_get_data()
        self.the_post_data = self.__read_post_data()
        self.the_cookies   = self.__read_cookies()


    def get_name(self):
        return 'mod_cgi'


    def __read_get_data(self):
        query = cgi.parse_qs(self.get_env('QUERY_STRING'))
        data  = {}
        for key, value in query.iteritems():
            data[key] = value[0]
        return Table(data, allow_duplicates = False, readonly = True)


    def __unpack_post_value(self, value):
        if type(value) == type(''):
            return value
        elif type(value) != type([]):
            return value.value
        return [self.__unpack_post_value(v) for v in value]


    def __read_post_data(self):
        input  = cgi.FieldStorage()
        output = {}
        for key in input:
            output[key] = self.__unpack_post_value(input[key])
        return Table(output, allow_duplicates = False, readonly = True)


    def __read_cookies(self):
        from Cookie import SimpleCookie
        cookies_raw = SimpleCookie(self.get_env('HTTP_COOKIE'))
        cookies     = {}
        for key, field in cookies_raw.iteritems():
            cookies[key] = field.value
        return Table(cookies, allow_duplicates = False, readonly = True)


    def get_env(self, key):
        return os.environ[key]


    def get_data(self):
        return self.the_get_data


    def has_post_data(self):
        return len(self.the_post_data) > 0


    def post_data(self):
        return self.the_post_data


    def set_cookie(self, key, value, expires = None):
        self.add_header('Set-Cookie', '%s=%s; path=/' % (key, value))


    def cookies(self):
        return self.the_cookies


    def add_header(self, key, value):
        self.headers.append((key, value))


    def get_headers(self):
        return self.headers


    def _send_headers(self):
        self.headers_sent = True
        if self.status != 200:
            print "HTTP/1.1 %s unknown\r\n" % self.status
        print "Content-Type: %s\r\n" % self.content_type
        for key, value in self.headers:
            print "%s: %s\r\n" % (key, value)
        print


    def flush(self):
        if not self.headers_sent:
            self._send_headers()
        data = self.data
        self.data = ''
        print data
        return [data]


    def handle_exception(self):
        print 'Content-Type: text/plain; charset=utf-8'
        print
        print 'Caught by %s' % self.get_name()
        import traceback, sys
        traceback.print_exc(file = sys.stdout)


    def handle(self, func):
        try:
            func(self)
            self.flush()
        except:
            self.handle_exception()
