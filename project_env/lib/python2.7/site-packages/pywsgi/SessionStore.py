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

class SessionStore(object):
    """
    Base class for backends that save, load, and manage sessions in secondary.
    """

    def __init__(self):
        """
        Constructor.
        """
        pass


    def _save(self, session):
        """
        Saves the session data.
        Returns True on success, False otherwise.
        """
        raise Exception('Not implemented')


    def _load(self, session):
        """
        Loads the session data.
        Returns True on success, False otherwise.
        """
        raise Exception('Not implemented')


    def _delete(self, session):
        """
        Deletes the session data.
        Returns True on success, False otherwise.
        """
        raise Exception('Not implemented')
