from ctypes import CDLL, CFUNCTYPE, c_char_p, c_int, c_void_p, create_string_buffer

try:
    _libdvdcss = CDLL('libdvdcss.so.2')
except OSError:
    raise ImportError

_dvdcss_open = CFUNCTYPE(c_void_p, c_char_p)(('dvdcss_open', _libdvdcss))
_dvdcss_close = CFUNCTYPE(c_int, c_void_p)(('dvdcss_open', _libdvdcss))
_dvdcss_seek = CFUNCTYPE(c_int, c_void_p, c_int, c_int)(('dvdcss_seek', _libdvdcss))
_dvdcss_read = CFUNCTYPE(c_int, c_void_p, c_void_p, c_int, c_int)(('dvdcss_read', _libdvdcss))


class DvdCssFile(object):
    def __init__(self, filename):
        self._handle = _dvdcss_open(filename)
        if not self._handle:
            raise RuntimeError
        self._cur = 0

    def read(self, count):
        return self.read_sector(count // 2048)

    def read_sector(self, count):
        buf = create_string_buffer(count * 2048)
        ret = _dvdcss_read(self._handle, buf, count, 1)
        if ret < 0:
            raise IOError
        self._cur += ret
        if ret != count:
            # Short read, libdvdcss does a weird seek in this case, fix it
            self.seek_sector(self._cur)
            return buf[:ret * 2048]
        return buf

    def seek(self, offset):
        self.seek_sector(offset // 2048)

    def seek_sector(self, offset, in_vob=False):
        ret = _dvdcss_seek(self._handle, offset, in_vob and 1 or 0)
        if ret < 0 or ret != offset:
            raise RuntimeError
        self._cur = ret

    def tell(self, offset):
        return self.tell_sector() * 2048

    def tell_sector(self):
        return self._cur
