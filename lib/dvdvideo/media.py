from .volume import VmgUdf, VtsUdf


class Media(object):
    pass


class MediaUdf(Media):
    def __init__(self, filename):
        from .udf.media import Media

        self.udf = Media(filename)
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
