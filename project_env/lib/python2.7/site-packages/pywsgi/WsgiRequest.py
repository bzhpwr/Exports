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
from CgiRequest import CgiRequest

class WsgiRequest(CgiRequest):
    """
    This adapter implements a bridge to mod_swgi.
    """

    def __init__(self, environment, start_response, **kwargs):
        self.environment    = environment
        self.start_response = start_response
        CgiRequest.__init__(self, **kwargs)


    def get_name(self):
        return 'mod_wsgi'


    def get_env(self, key):
        return self.environment.get(key)


    def _send_headers(self):
        if self.headers_sent:
            return
        self.headers_sent = True
        headers = [('Content-type', self.content_type)]
        for key, value in self.headers:
            headers.append((key, value))
        self.start_response(str(self.status) + ' ', headers)


    def flush(self):
        self._send_headers()
        data = self.data
        self.data = ''
        return [data]


    def handle_exception(self):
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        self.start_response('200 OK', headers)
        import traceback, sys
        return ["Caught by %s:\n" % self.get_name(), traceback.format_exc()]


    def handle(self, func):
        try:
            func(self)
            output = self.flush()
        except:
            output = self.handle_exception()
        return output
