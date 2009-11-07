from .volume import VmgUdf

class Media(object):
    pass


class FileUdf(object):
    def __init__(self, udf, entry):
        self._udf = udf
        self._location = entry.ad[0].location_absolute

    def read(self, sector, count=1):
        return self._udf.read_sector(self._location + sector, count * 2048)


class MediaUdf(Media):
    def __init__(self, filename):
        from .udf.media import Media

        self.udf = Media(filename)
        self._dir = self.udf.volume.partitions[0].fileset.root.tree['VIDEO_TS'].entry.tree

    def file(self, name):
        return FileUdf(self.udf, self._dir[name].entry)

    def vmg(self):
        return VmgUdf(self)
