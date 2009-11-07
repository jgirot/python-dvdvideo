from .volume import VmgUdf

class Media(object):
    pass


class MediaUdf(Media):
    def __init__(self, filename):
        from .udf.media import Media

        self.udf = Media(filename)
        self._dir = self.udf.volume.partitions[0].fileset.root.tree['VIDEO_TS'].entry.tree

    def vmg(self):
        return VmgUdf(self.udf, self._dir)

        header = self.udf.read_sector(entry.ad[0].location_absolute, 2048)
        r = _VmgUdf(header)

        header = self.udf.read_sector(entry.ad[0].location_absolute + r.header.part_bup_start, 2048)
        print(header)
