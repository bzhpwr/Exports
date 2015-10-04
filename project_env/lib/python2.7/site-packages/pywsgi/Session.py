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
import os, os.path, sha, time
from Table import Table

class Session(object):
    """
    Represents a session, retrieve via the request handler API.
    """

    def __init__(self, request, **kwargs):
        """
        Should not be called directly. Retrieve the session object by calling
        request.get_session() instead.

        @type  request: Request
        @param request: The associated request.
        @type  kwargs: dict
        @param kwargs: The following arguments are supported:
            - lifetime:   The maximum lifetime of the session (in seconds).
            - on_destroy: A callback, called after destroy() was called.
        """
        self.request    = request
        self.sid        = None
        self.lifetime   = kwargs.get('lifetime', 60*60)
        self.on_destroy = kwargs.get('on_destroy')
        self._clear_data()
        self._start()


    def _clear_data(self, init = None):
        self.the_data = Table(init,
                              allow_duplicates = False,
                              callback         = self._on_data_changed)


    def _on_data_changed(self):
        """
        Called by the self.the_data table to inform us that its content
        changed.
        """
        self.request._save_session(self)


    def _create_session(self):
        import sha, time
        self.sid = sha.new(str(time.time())).hexdigest()
        self.request.set_cookie('sid', self.sid, 0)
        self.request._save_session(self)


    def _start(self):
        """
        May raise an exception on failure.
        """
        if self.sid is not None:
            raise Exception('Session already started.')
        self.sid = self.request.cookies().get_first('sid')
        if self.sid is None:
            return self._create_session()
        if not self.request._load_session(self):
            self.destroy()
            return self._create_session()


    def get_id(self):
        """
        Returns the session id.

        @rtype:  string
        @return: The session id.
        """
        return self.sid


    def destroy(self):
        """
        Removes all session data and ends the session.
        """
        self.request._delete_session(self)
        self._clear_data()
        self.sid = None
        self.request.set_cookie('sid', '', 0)
        if self.on_destroy is not None:
            self.on_destroy()


    def data(self):
        """
        Returns the data that is associated with the session.
        The returned table is a read/write object, so it is also used for
        storing values in the session.

        @rtype:  Table
        @return: The session data.
        """
        return self.the_data
