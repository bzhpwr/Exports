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

class RequestHandler(object):
    """
    A handler that automatically selects a supported request adapter.
    """

    def __init__(self, func, **kwargs):
        self.func          = func
        self.session_store = kwargs.get('session_store')
        if self.supports_wsgi():
            import wsgiref.handlers
            wsgiref.handlers.CGIHandler().run(self._handle_wsgi_request)
        elif self.supports_mod_python():
            pass # ModPythonRequest should be used directly by a hook.
        elif self.supports_cgi():
            self._handle_cgi_request()
        else:
            raise Exception('Unsupported client adapter.')


    def supports_wsgi(self):
        try:
            import wsgiref.handlers
        except:
            return False
        return True


    def supports_cgi(self):
        try:
            import cgi
        except:
            return False
        return True


    def supports_mod_python(self):
        try:
            from mod_python import apache
        except:
            return False
        return True


    def _handle_wsgi_request(self, environment, start_response):
        from WsgiRequest import WsgiRequest
        request = WsgiRequest(environment,
                              start_response,
                              session_store = self.session_store)
        return request.handle(self.func)


    def _handle_mod_python_request(self, req):
        from ModPythonRequest import ModPythonRequest
        request = ModPythonRequest(req, session_store = self.session_store)
        request.handle(self.func)


    def _handle_cgi_request(self):
        from CgiRequest import CgiRequest
        request = CgiRequest(session_store = self.session_store)
        request.handle(self.func)
