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

import struct

from .general import DescriptorTag, ExtentAD


class AnchorVolumeDescriptorPointer(object):
    _struct = struct.Struct('<16x20s20s')

    def __init__(self, tag, buf):
        self.tag = tag
        if tag.identifier != 2:
            raise RuntimeError('Anchor Volume Descriptor Pointer illegal')

        data = self._struct.unpack(buf[:56])
        self.main_descriptor_extent = ExtentAD(data[0])
        self.reserve_descriptor_extent = ExtentAD(data[1])


def _DescriptorSequence(media, location, length):
    buf = media.read_sector(location, length)

    cur = 0
    while cur < length:
        tag = DescriptorTag(buf[cur:cur + 16])
        if tag.identifier == 8:
            break

        yield tag, buf[cur:cur + 2048]

        cur += 2048


class Volume(object):
    _lazy = 'partitions',

    def __init__(self, media):
        self._media = media

        buf = media.read_sector(256)
        tag = DescriptorTag(buf)
        self.anchor = AnchorVolumeDescriptorPointer(tag, buf)

    def __getattr__(self, key):
        if key in self._lazy:
            self._populate()
        return super().__getattribute__(key)

    def _read_descriptors(self, extent):
        seq = _DescriptorSequence(self._media, extent.location, extent.length)

        partitions = {}

        for tag, buf in seq:
            if tag.identifier == 5:
                p = Partition(self._media, self, tag, buf)
                partitions[p.number] = p
            elif tag.identifier == 6:
                # TODO
                pass

        if partitions:
            return partitions
        raise RuntimeError

    def _populate(self):
        try:
            data = self._read_descriptors(self.anchor.main_descriptor_extent)
        except RuntimeError:
            data = self._read_descriptors(self.anchor.reserve_descriptor_extent)
        self.partitions = data


class Partition(object):
    _lazy = 'fileset'
    _struct = struct.Struct('<16x4xHH164xII316x')

    def __init__(self, media, volume, tag, buf):
        self._media = media
        self._volume = volume

        self.tag = tag
        if tag.identifier != 5:
            raise RuntimeError('Partition Descriptor illegal')

        data = self._struct.unpack(buf[:512])
        self.flags, self.number, self.location, self.length = data

    def __getattr__(self, key):
        if key in self._lazy:
            self._populate()
        return super().__getattribute__(key)

    def _populate(self):
        from .filesystem import FileSet

        seq = _DescriptorSequence(self._media, self.location, self.length)

        for tag, buf in seq:
            if tag.identifier == 256:
                self.fileset = FileSet(self._media, self._volume, self.number, tag, buf)
