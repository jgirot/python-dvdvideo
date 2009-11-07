import struct


class DescriptorTag(object):
    _struct = struct.Struct('<HHBxHHHI')

    def __init__(self, buf):
        data = self._struct.unpack(buf[:16])
        (self.identifier, self.version, self.checksum, serial_number,
                crc, self.crc_length, self.location) = data

    def __repor__(self):
        return '<DescriptorTag with identifier %d, version %d, location %d' % (
                self.identifier,
                self.version,
                self.location,
                )


class OSTACompressedUnicode(str):
    def __new__(self, buf):
        type = buf[0]

        if type == 8:
            s = []
            for i in buf[1:]:
                s.append(chr(i))
            return str(''.join(s))
        elif type == 16:
            raise NotImplementedError
        raise RuntimeError


class ExtentAD(object):
    _struct = struct.Struct('<II8xH2x')
    size = _struct.size

    def __init__(self, buf):
        data = self._struct.unpack(buf)
        length, self.location, self.partition = data
        self.length = length & 0x3fffffff
        self.flags = length >> 30

    def __repr__(self):
        return '<ExtentAD with location %d, length %d, flags %d, partition %d' % (
                self.location,
                self.length,
                self.flags,
                self.partition,
                )


class LongAD(object):
    _struct = struct.Struct('<IIH6x')
    size = _struct.size

    def __init__(self, buf):
        data = self._struct.unpack(buf)
        length, self.location, self.partition = data
        self.length = length & 0x3fffffff
        self.flags = length >> 30

    def __repr__(self):
        return '<LongAD with location %d, length %d, flags %d, partition %d' % (
                self.location,
                self.length,
                self.flags,
                self.partition,
                )


class ShortAD(object):
    _struct = struct.Struct('<II')
    size = _struct.size

    def __init__(self, buf):
        data = self._struct.unpack(buf)
        length, self.location = data
        self.length = length & 0x3fffffff
        self.flags = length >> 30

    def __repor__(self):
        return '<ShortAD with location %d, length %d, flags %d' % (
                self.location,
                self.length,
                self.flags,
                )
