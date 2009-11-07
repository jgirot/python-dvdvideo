from .ifo import VmgIfo


class Vmg(object):
    def __init__(self):
        pass


class VmgUdf(Vmg):
    class File(object):
        def __init__(self, udf, dir, name):
            self._udf = udf
            self._location = dir[name].entry.ad[0].location_absolute

        def read(self, sector, count=1):
            return self._udf.read_sector(self._location + sector, count * 2048)

    def __init__(self, udf, dir):
        self._udf = udf
        self.file_ifo = self.File(udf, dir, 'VIDEO_TS.IFO')
        self.file_vob = self.File(udf, dir, 'VIDEO_TS.VOB')
        self.file_bup = self.File(udf, dir, 'VIDEO_TS.BUP')

        self.ifo = VmgIfo(self.file_ifo)
        self.bup = VmgIfo(self.file_bup)
