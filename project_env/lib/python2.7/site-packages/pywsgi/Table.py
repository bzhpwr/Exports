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

class Table(object):
    """
    Container type used to represent GET, POST, and session data as well
    as cookies.
    """

    def __init__(self,
                 init             = None,
                 allow_duplicates = True,
                 readonly         = False,
                 callback         = None):
        """
        Constructor.

        @type  init: list|dict
        @param init: A sequence or dictionary to populate the table.
        @type  allow_duplicates: boolean
        @param allow_duplicates: Whether duplicate rows are allowed.
        @type  callback: function
        @param callback: Called whenever the content changes.
        """
        self.allow_duplicates = allow_duplicates
        self.readonly         = readonly
        self.data_dict        = {}
        self.callback         = callback
        if init is None:
            self.data_list = []
        elif isinstance(init, list):
            for key, value in init:
                self.add(key, value)
        elif isinstance(init, dict):
            self.data_list = init.items()
            self.data_dict = dict([(k, [v]) for k, v in self.data_list])
        else:
            raise TypeError('Invalid argument type for init argument.')


    def __iter__(self):
        return self.data_list.__iter__()


    def __len__(self):
        return len(self.data_list)


    def _emit_changed(self):
        if self.callback is None:
            return
        self.callback()


    def remove_any(self, key):
        """
        Removes all rows that have the given key from the table.

        @type  key: string
        @param key: The name of the attribute.
        """
        if self.readonly:
            raise Exception('Attempt to modify read-only table.')
        if not self.data_dict.has_key(key):
            return
        old_values = self.data_dict.get(key)
        del self.data_dict[key]
        for value in old_values:
            self.data_list.remove((key, value))
        self._emit_changed()


    def add(self, key, value):
        """
        Adds the given key/value pair.
        If the allow_duplicates argument is True, duplicate keys are allowed.
        If allow_duplicates is False, this method is equivalent to set().

        @type  key: string
        @param key: The name of the attribute.
        @type  value: object
        @param value: The value of the attribute.
        """
        if self.readonly:
            raise Exception('Attempt to modify read-only table.')
        if not self.allow_duplicates:
            return self.set(key, value)
        self.data_list.append((key, value))
        if self.data_dict.has_key(key):
            self.data_dict[key].append(value)
        else:
            self.data_dict[key] = [value]
        self._emit_changed()


    def set(self, key, value):
        """
        Defines the value of the given key. Any existing rows with the same
        key are removed from the table, regardless of what was passed to the
        allow_duplicates argument of the table constructor.

        @type  key: string
        @param key: The name of the attribute.
        @type  value: string
        @param value: The value of the attribute.
        """
        if self.readonly:
            raise Exception('Attempt to modify read-only table.')
        self.remove_any(key)
        self.data_dict[key] = [value]
        self.data_list.append((key, value))
        self._emit_changed()


    def has_key(self, key):
        """
        Returns True if the given key is in the table, False otherwise.

        @type  key: string
        @param key: The name of the attribute.
        @rtype:  boolean
        @return: True if the key was found, False otherwise.
        """
        return self.data_dict.has_key(key)


    def get(self, key, default = None):
        """
        Returns a list of all values that have the given key.
        If no such row is found, the given default value is returned.

        @type  key: string
        @param key: The name of the attribute.
        @type  default: object
        @param default: The value that is returned when no match was found.
        @rtype:  list[string]|object
        @return: The list of values, or the default value.
        """
        return self.data_dict.get(key, default)


    def get_first(self, key, default = None):
        """
        Returns the value of the first pair that has the given key.

        @type  key: string
        @param key: The name of the attribute.
        @type  default: object
        @param default: The value that is returned when no match was found.
        @rtype:  string|object
        @return: The first value, or the default value.
        """
        if not self.data_dict.has_key(key):
            return default
        for k, v in self.data_list:
            if k == key:
                return v
        assert False  # Not reached


    def get_str(self, key, default = None):
        """
        Convenience wrapper around get_first() that casts the value to str
        before returning it.

        @type  key: string
        @param key: The name of the attribute.
        @type  default: string
        @param default: The value that is returned when no match was found.
        @rtype:  str
        @return: The first value, or the default value.
        """
        value = self.get_first(key, default)
        if value is None:
            return None
        return str(value)


    def get_int(self, key, default = 0):
        """
        Convenience wrapper around get_first() that casts the value to int
        before returning it.

        @type  key: string
        @param key: The name of the attribute.
        @type  default: int
        @param default: The value that is returned when no match was found.
        @rtype:  int
        @return: The first value, or the default value.
        """
        return int(self.get_first(key, default))


    def get_bool(self, key, default = False):
        """
        Convenience wrapper around get_first() that casts the value to bool
        before returning it.

        @type  key: string
        @param key: The name of the attribute.
        @type  default: boolean
        @param default: The value that is returned when no match was found.
        @rtype:  boolean
        @return: The first value, or the default value.
        """
        return bool(self.get_first(key, default))


    def items(self):
        return self.data_dict
