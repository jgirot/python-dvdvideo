import struct

from .general import DescriptorTag, OSTACompressedUnicode, LongAD, ShortAD


class LongADPartition(LongAD):
    def __init__(self, buf, volume):
        super().__init__(buf)
        partition = volume.partitions[self.partition]
        self.location_absolute = partition.location + self.location


class ShortADPartition(ShortAD):
    def __init__(self, buf, volume, partition_nr):
        super().__init__(buf)
        partition = volume.partitions[partition_nr]
        self.location_absolute = partition.location + self.location


class ICBTag(object):
    _struct = struct.Struct('<8x3xB6xH')

    def __init__(self, buf):
        data = self._struct.unpack(buf)
        self.filetype, self.flags = data

    def __repr__(self):
        return '<ICBTag with filetype: %d; flags: %x>' % (
                self.filetype,
                self.flags,
                )


class FileSet(object):
    _lazy = 'root',
    _struct = struct.Struct('<16x384x16s')

    def __init__(self, media, volume, partition_nr, tag, buf):
        self._media = media
        self._volume = volume
        self._partition_nr = partition_nr
        self.tag = tag
        if tag.identifier != 256:
            raise RuntimeError

        data = self._struct.unpack(buf[:416])
        self.root_icb = LongADPartition(data[0], volume)

    def __getattr__(self, key):
        if key in self._lazy:
            self._populate()
        return super().__getattribute__(key)

    def _populate(self):
        location = self.root_icb.location_absolute
        length = self.root_icb.length

        buf = self._media.read_sector(location, length)
        tag = DescriptorTag(buf)
        self.root = FileEntry(self._media, self._volume, self._partition_nr, tag, buf)


class FileEntry(object):
    _lazy = 'tree',
    _struct = struct.Struct('<16x20s20xQ104xII')

    def __init__(self, media, volume, partition_nr, tag, buf):
        self._media = media
        self._volume = volume
        self._partition_nr = partition_nr
        self.tag = tag
        if tag.identifier != 261:
            raise RuntimeError

        data = self._struct.unpack(buf[:176])
        icb, self.length, length_ea, length_ad = data

        self.icb = ICBTag(icb)

        ad = []

        buf = buf[176 + length_ea:176 + length_ea + length_ad]

        desc_type = self.icb.flags & 3
        cur = 0
        while cur < len(buf):
            if desc_type == 0:
                ad.append(ShortADPartition(buf[cur:cur + ShortAD.size], self._volume, self._partition_nr))
                cur += ShortAD.size
            else:
                raise NotImplementedError

        self.ad = tuple(ad)

    def __getattr__(self, key):
        if key in self._lazy:
            self._populate()
        return super().__getattribute__(key)

    def __repr__(self):
        return '<FileEntry with icbtag: %r; ad: %r>' % (
                self.icb,
                self.ad,
                )

    def _populate(self):
        tree = None

        if self.icb.filetype == 4:
            tree = {}

            for ad in self.ad:
                location = ad.location_absolute
                length = ad.length

                buf = self._media.read_sector(location, length)
                tag = DescriptorTag(buf)

                cur = 0
                while cur < length:
                    if tag.identifier == 257:
                        f = FileIdentifier(self._media, self._volume, self._partition_nr, tag, buf[cur:])
                        tree[f.name] = f
                        cur += f.descriptor_length
                    else:
                        raise RuntimeError
        else:
            raise NotImplementedError

        self.tree = tree


class FileIdentifier(object):
    _lazy = 'entry',
    _struct = struct.Struct('<16x3xB16sH')

    def __init__(self, media, volume, partition_nr, tag, buf):
        self._media = media
        self._volume = volume
        self._partition_nr = partition_nr
        self.tag = tag
        if tag.identifier != 257:
            raise RuntimeError

        data = self._struct.unpack(buf[:38])
        length_fi, icb, length_iu = data

        self.icb = LongADPartition(icb, volume)

        # From libdvdread
        self.descriptor_length = 4 * ((38 + length_fi + length_iu + 3) // 4)

        if length_fi:
            self.name = OSTACompressedUnicode(buf[38 + length_iu:38 + length_iu + length_fi])
        else:
            self.name = ''

    def __getattr__(self, key):
        if key in self._lazy:
            self._populate()
        return super().__getattribute__(key)

    def _populate(self):
        location = self.icb.location_absolute
        length = self.icb.length

        buf = self._media.read_sector(location, length)
        tag = DescriptorTag(buf)
        self.entry = FileEntry(self._media, self._volume, self._partition_nr, tag, buf)
