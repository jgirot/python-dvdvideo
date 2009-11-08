from .volume import VmgUdf, VtsUdf


class Media(object):
    pass


class MediaUdf(Media):
    def __init__(self, filename):
        from .udf.media import Media

        self._file = open(filename, 'rb')
        self.udf = Media(self._file)
        self.video_dir = self.udf.volume.partitions[0].fileset.root.tree['VIDEO_TS'].entry.tree

    def file(self, name):
        f = self.video_dir[name]

        if len(f.entry.ad) > 1:
            raise NotImplementedError

        return f

    def read(self, count):
        return self._file.read(count * 2048)

    def seek(self, offset):
        self._file.seek(offset * 2048)

    def tell(self):
        return self._file.tell() // 2048

    def vmg(self):
        return VmgUdf(self)

    def vts(self, titleset):
        return VtsUdf(self, titleset)
