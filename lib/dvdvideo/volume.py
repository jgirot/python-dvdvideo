import itertools

from .ifo import VmgIfo, VtsIfo
from .vob import MenuVob, TitleVob


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

        self.file_menu_vob = media.file('VIDEO_TS.VOB')
        self.menu_vob = MenuVob(self.file_menu_vob)

    def dump(self):
        return itertools.chain(
                self.ifo.dump(),
                self.bup.dump(),
                self.menu_vob.dump(),
                )


class VtsUdf(Vmg):
    def __init__(self, media, titleset):
        prefix = 'VTS_%02d' % titleset

        self.file_ifo = media.file('%s_0.IFO' % prefix)
        self.file_bup = media.file('%s_0.BUP' % prefix)

        self.ifo = VtsIfo(self.file_ifo)
        self.bup = VtsIfo(self.file_bup)

        try:
            self.file_menu_vob = media.file('%s_0.VOB' % prefix)
            self.menu_vob = MenuVob(self.file_menu_vob)
        except KeyError:
            self.file_menu_vob = None
            self.menu_vob = None

        self.file_title_vob = []

        for i in range(1, 10):
            try:
                vob = media.file('%s_%d.VOB' % (prefix, i))
                self.file_title_vob.append(vob)
            except KeyError:
                break

        self.title_vob = TitleVob(self.file_title_vob)

    def dump(self):
        return itertools.chain(
                self.ifo.dump(),
                self.bup.dump(),
                self.menu_vob.dump(),
                self.title_vob.dump(),
                )
