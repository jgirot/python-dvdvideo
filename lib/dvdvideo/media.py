import os
import stat

from .volume import VmgUdf, VtsUdf


class Media(object):
    pass


class MediaUdf(Media):
    class File(object):
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

    def file(self, name):
        f = self.video_dir[name]

        if len(f.entry.ad) > 1:
            raise NotImplementedError

        return f

    def vmg(self):
        return VmgUdf(self)

    def vts(self, titleset):
        return VtsUdf(self, titleset)
