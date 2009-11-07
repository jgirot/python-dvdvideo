from .volume import VmgUdf, VtsUdf

class Media(object):
    pass


class FileUdf(object):
    def __init__(self, udf, dir, name):
        self._udf = udf
        self.name = name

        entry = dir[name].entry

        if len(entry.ad) > 1:
            raise NotImplementedError

        self.ad = entry.ad[0]

    def __repr__(self):
        return '<FileUdf %r; ad %r>' % (self.name, self.ad)

    def _dump_iter(self, length):
        real_length = max(length, self.ad.length // 2048)
        cur = 0
        while cur < real_length:
            toread = min(1000, real_length - cur)
            yield self.read(cur, toread)
            cur += toread

    def dump(self, length=0):
        return self.name, self._dump_iter(length)

    def read(self, sector, count=1):
        return self._udf.read_sector(self.ad.location_absolute + sector, count * 2048)


class MediaUdf(Media):
    def __init__(self, filename):
        from .udf.media import Media

        self.udf = Media(filename)
        self._dir = self.udf.volume.partitions[0].fileset.root.tree['VIDEO_TS'].entry.tree

    def file(self, name):
        return FileUdf(self.udf, self._dir, name)

    def vmg(self):
        return VmgUdf(self)

    def vts(self, titleset):
        return VtsUdf(self, titleset)
