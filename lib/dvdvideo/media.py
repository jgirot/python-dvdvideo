from .volume import VMG as _VMG

class Media(object):
    pass


class MediaUDF(Media):
    def __init__(self, filename):
        from .udf.media import Media

        self.udf = Media(filename)
        self._dir = self.udf.volume.partitions[0].fileset.root.tree['VIDEO_TS'].entry.tree

    class VMG(_VMG):
        pass

    def vmg(self):
        entry = self._dir['VIDEO_TS.IFO'].entry

        header = self.udf.read_sector(entry.ad[0].location_absolute, 2048)
        return self.VMG(header)
