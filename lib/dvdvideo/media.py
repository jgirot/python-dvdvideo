from .volume import VmgUdf, VtsUdf

class Media(object):
    pass


class FileUdf(object):
    def __init__(self, udf, dir, name):
        self._udf = udf
        self.name = name

        self.location = dir[name].entry.ad[0].location_absolute

    def __repr__(self):
        return '<FileUdf %r; location %d>' % (self.name, self.location)

    def read(self, sector, count=1):
        return self._udf.read_sector(self.location + sector, count * 2048)


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
