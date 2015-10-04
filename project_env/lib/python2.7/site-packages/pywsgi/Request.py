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
from Url              import Url
from Session          import Session
from SessionFileStore import SessionFileStore
from Table            import Table

class Request(object):
    """
    Base class for all request adapters.
    """

    def __init__(self, **kwargs):
        """
        Constructor.

        @type  kwargs: dict
        @param kwargs: The following arguments are supported:
            - session_store: The session storage backend.
        """
        self.status        = 200;
        self.content_type  = 'text/html; charset=utf-8'
        self.data          = ''
        self.session_store = kwargs.get('session_store')
        self.session       = None
        if self.session_store is None:
            self.session_store = SessionFileStore()


    def _save_session(self, session):
        return self.session_store._save(session)


    def _load_session(self, session):
        return self.session_store._load(session)


    def _delete_session(self, session):
        return self.session_store._delete(session)


    def _on_session_destroy(self):
        self.session = None


    def get_name(self):
        """
        Returns a human readable name of the adapter.
        For example, this may return 'mod_python', 'CGI, or 'WSGI'.

        @rtype:  string
        @return: The adapter name.
        """
        raise Exception('get_name() not implemented...')


    def set_status(self, status):
        """
        Defines the HTTP status value (e.g. 404 for File not found).

        @type  status: int
        @param status: The status id.
        """
        self.status = status


    def set_content_type(self, type):
        """
        Defines the content type for the HTTP header field. For example:
        'text/plain'. If a content type is not defined, the request
        defaults to 'text/html; charset=utf-8'.

        @type  type: str
        @param type: The content type.
        """
        self.content_type = type


    def add_header(self, key, value):
        """
        Defines a field for the HTTP header.

        @type  key: str
        @param key: The name of the field.
        @type  value: str
        @param value: The value of the field.
        """
        raise Exception('add_header() not implemented...')


    def get_headers(self):
        """
        Returns a list of all HTTP header fields that are sent to the client.

        @rtype:  list[(str, str)]
        @return: The HTTP headers.
        """
        raise Exception('get_headers() not implemented...')


    def write(self, data):
        """
        Write into the output buffer. This is not actually sent to the client
        until flush() is called.

        @type  data: str
        @param data: The data that is appended to the output buffer.
        """
        self.data += data


    def flush(self):
        """
        Flush the output buffer, and send it to the client. Also,
        if HTTP headers were not already sent, send them first.
        """
        raise Exception('flush() not implemented...')


    def get_url(self, path = '', **kwargs):
        """
        Returns an URL object that points to the given path, with the query
        variables initialized to the given kwargs.

        @type  path: str
        @param path: The (relative or absolute) path to which to URL points.
        @type  kwargs: dict
        @param kwargs: A dict of query variables.
        @rtype:  Url
        @return: A new Url object.
        """
        return Url(self, path, **kwargs)


    def get_current_url(self, **kwargs):
        """
        Returns an URL object that points to the requested path, with the
        query variables initialized to the given kwargs.

        @type  kwargs: dict
        @param kwargs: A dict of query variables.
        @rtype:  Url
        @return: A new Url object.
        """
        # Extract variables from the current URL.
        url = self.get_url()
        for key, value in self.get_data():
            url.set_var(key, value)
        for key, value in kwargs.iteritems():
            url.set_var(key, value)
        return url


    def set_session_store(self, store):
        """
        Defines the session storage backend.

        @type  store: SessionStore
        @param store: The storage backend.
        """
        self.session_store = store


    def start_session(self):
        """
        Starts a new session. Does nothing if the session was already started.

        @rtype:  Session
        @return: The new session.
        """
        if not self.session:
            self.session = Session(self, on_destroy = self._on_session_destroy)
        return self.session


    def get_session(self):
        """
        Returns the current session, or None if no session was started.

        @rtype:  Session
        @return: The current session.
        """
        return self.session


    def get_env(self, key):
        """
        Returns the value of the variable with the given name from the
        environment.

        @type  key: str
        @param key: The name of the environment variable.
        @rtype:  string
        @return: The value of the environment variable.
        """
        raise Exception('get_env() not implemented...')


    def get_data(self):
        """
        Returns a table object that contains the GET data.

        @rtype:  Table
        @return: The GET data.
        """
        raise Exception('get_data() not implemented...')


    def has_post_data(self):
        """
        Returns True if any POST data exists, False otherwise.

        @rtype:  boolean
        @return: Whether the request has any POST data.
        """
        raise Exception('has_post_data() not implemented...')


    def post_data(self):
        """
        Returns a table object that contains the POST data.

        @rtype:  Table
        @return: The POST data.
        """
        raise Exception('post_data() not implemented...')


    def set_cookie(self, key, value, expires = None):
        """
        Set a cookie with the given key/value and optionally with an
        expiration time (as returned by time.time()).

        @type  key: str
        @param key: The name of the cookie.
        @type  value: str
        @param value: The value of the cookie.
        @type  expires: int
        @param expires: The time at which the cookie expires.
        """
        raise Exception('set_cookie() not implemented...')


    def cookies(self):
        """
        Returns a table object that contains all cookies.

        @rtype:  Table
        @return: The cookies.
        """
        raise Exception('cookies() not implemented...')


    def handle_exception(self):
        """
        Prints the current exception in a way that shows them to the client
        according to the environment.
        """
        raise Exception('run() not implemented...')
