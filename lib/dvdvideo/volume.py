from .ifo import VmgIfo, VtsIfo


class Vmg(object):
    pass


class Vts(object):
    pass


class VmgUdf(Vmg):
    def __init__(self, media):
        self.file_ifo = media.file('VIDEO_TS.IFO')
        self.file_bup = media.file('VIDEO_TS.BUP')

        self.ifo = VmgIfo(self.file_ifo)
        self.bup = VmgIfo(self.file_bup)

        self.file_vob = media.file('VIDEO_TS.VOB')


class VtsUdf(Vmg):
    def __init__(self, media, titleset):
        prefix = 'VTS_%02d' % titleset

        self.file_ifo = media.file('%s_0.IFO' % prefix)
        self.file_bup = media.file('%s_0.BUP' % prefix)

        self.ifo = VtsIfo(self.file_ifo)
        self.bup = VtsIfo(self.file_bup)

        try:
            self.file_menu_vob = media.file('%s_0.VOB' % prefix)
        except KeyError:
            self.file_menu_vob = None

        self.file_title_vobs = []

        for i in range(1, 10):
            try:
                vob = media.file('%s_%d.VOB' % (prefix, i))
                self.file_title_vobs.append(vob)
            except KeyError:
                break
