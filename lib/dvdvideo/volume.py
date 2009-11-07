from .ifo import VmgIfo


class Vmg(object):
    pass


class VmgUdf(Vmg):
    class File(object):
        def __init__(self, udf, dir, name):
            self._udf = udf
            self._location = dir[name].entry.ad[0].location_absolute

        def read(self, sector, count=1):
            return self._udf.read_sector(self._location + sector, count * 2048)

    def __init__(self, media):
        self.file_ifo = media.file('VIDEO_TS.IFO')
        self.file_vob = media.file('VIDEO_TS.VOB')
        self.file_bup = media.file('VIDEO_TS.BUP')

        self.ifo = VmgIfo(self.file_ifo)
        self.bup = VmgIfo(self.file_bup)
