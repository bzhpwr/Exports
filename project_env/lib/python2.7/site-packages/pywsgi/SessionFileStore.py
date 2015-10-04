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
import tempfile, os, os.path, time
from SessionStore import SessionStore
from ConfigParser import RawConfigParser

class SessionFileStore(SessionStore):
    """
    A session store that saves the sessions on a filesystem.
    """

    def __init__(self, directory = None):
        """
        Constructor.

        @type  directory: string
        @param directory: The directory in which sessions are stored. The
                          default directory is tempfile.tempdir.
        """
        if directory is None:
            directory = tempfile.gettempdir()
        if not os.path.isdir(directory):
            raise Exception('No such directory: %s' % directory)
        self.directory = directory


    def _get_session_filename(self, session):
        sid      = session.get_id()
        filename = ''
        for n in range(0, len(sid), 2):
            filename = os.path.join(filename, sid[n:n+2])
        return os.path.join(self.directory, filename + '.session')


    def _save(self, session):
        # Create a directory for the session.
        filename = self._get_session_filename(session)
        dirname  = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Save the session.
        rcparser = RawConfigParser()
        try:
            rcparser.add_section('session')
        except:
            pass # Duplicate section.
        for key, value in session.data():
            rcparser.set('session', key, value)
        rcparser.write(open(filename, 'w'))


    def _load(self, session):
        filename = self._get_session_filename(session)
        if not os.path.exists(filename):
            return False
        if os.path.getmtime(filename) < time.time() - session.lifetime:
            return False
        rcparser = RawConfigParser()
        try:
            rcparser.read(filename)
        except:
            return False
        data = {}
        for option in rcparser.options('session'):
            data[option] = rcparser.get('session', option)
        session._clear_data(data)
        return True


    def _delete(self, session):
        filename = self._get_session_filename(session)
        if not os.path.exists(filename):
            return
        os.remove(filename)
