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

import collections.abc
import os
import stat

from .volume import VmgUdf, VtsUdf


class MediaUdf(collections.abc.Mapping):
    class File:
        def __init__(self, filename):
            f = open(filename, 'rb')
            self.close = f.close
            self.read = f.read
            self.seek = f.seek
            self.tell = f.tell

        def read_sector(self, count, **kw):
            return self.read(count * 2048)

        def seek_sector(self, offset, **kw):
            self.seek(offset * 2048)

        def tell_sector(self):
            return self.tell() // 2048

    def __init__(self, filename):
        from .udf.media import Media
        try:
            from .libdvdcss import DvdCssFile
        except ImportError:
            DvdCssFile = self.File

        s = os.stat(filename)
        if stat.S_ISREG(s.st_mode):
            f = self.File(filename)
        elif stat.S_ISBLK(s.st_mode):
            f = DvdCssFile(filename)
        else:
            raise RuntimeError

        self.read = f.read_sector
        self.seek = f.seek_sector
        self.tell = f.tell_sector

        self._file = f
        self.udf = Media(f)
        self.video_dir = self.udf.volume.partitions[0].fileset.root.tree['VIDEO_TS'].entry.tree

    def __getitem__(self, name):
        f = self.video_dir[name]
        if len(f.entry.ad) > 1:
            raise NotImplementedError
        return f

    def __iter__(self):
        return iter(self.video_dir)

    def __len__(self):
        return len(self.video_dir)

    def vmg(self):
        return VmgUdf(self)

    def vts(self, titleset):
        return VtsUdf(self, titleset)
