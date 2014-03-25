"""
@copyright: 2009 Bastian Blank <waldi@debian.org>
@license: GNU GPL-3
"""
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .volume import Volume


class Media:
    def __init__(self, file):
        self._file = file
        self._sector_size = 2048

    def read(self, count):
        count_align = (count + self._sector_size - 1) & ~(self._sector_size - 1)
        return self._file.read(count_align)

    def read_sector(self, offset, count=2048):
        offset_bytes = offset * self._sector_size
        self._file.seek(offset_bytes)
        return self.read(count)

    @property
    def volume(self):
        return Volume(self)
