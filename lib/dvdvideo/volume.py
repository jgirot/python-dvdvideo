import itertools

from .ifo import VmgIfo, VtsIfo
from .vob import MenuVob, TitleVob


class Vmg(object):
    pass


class Vts(object):
    pass


class VmgUdf(Vmg):
    def __init__(self, media):
        file_ifo = media.file('VIDEO_TS.IFO')
        file_bup = media.file('VIDEO_TS.BUP')
        file_vob = media.file('VIDEO_TS.VOB')

        self.fileset = FileSetUdf(media, file_ifo, file_bup, file_vob)

        self.ifo = VmgIfo(self.fileset.ifo)
        self.bup = VmgIfo(self.fileset.bup)
        self.menu_vob = MenuVob(self.fileset.menu_vob)

    def dump(self):
        return iter(self.fileset)


class VtsUdf(Vmg):
    def __init__(self, media, titleset):
        prefix = 'VTS_%02d' % titleset

        file_ifo = media.file('%s_0.IFO' % prefix)
        file_bup = media.file('%s_0.BUP' % prefix)

        try:
            file_menu_vob = media.file('%s_0.VOB' % prefix)
        except KeyError:
            file_menu_vob = None

        file_title_vob = []
        for i in range(1, 10):
            try:
                vob = media.file('%s_%d.VOB' % (prefix, i))
                file_title_vob.append(vob)
            except KeyError:
                break

        self.fileset = FileSetUdf(media, file_ifo, file_bup, file_menu_vob, file_title_vob)

        self.ifo = VtsIfo(self.fileset.ifo)
        self.bup = VtsIfo(self.fileset.bup)

        if file_menu_vob:
            self.menu_vob = MenuVob(self.fileset.menu_vob)
        else:
            self.menu_vob = None

        self.title_vob = TitleVob(self.fileset.title_vob)

    def dump(self):
        return iter(self.fileset)


class FileSetUdf(object):
    class File(object):
        def __init__(self, media, name, location, length):
            self._media, self.name, self._location, self.length = media, name, location, length

        def __iter__(self):
            cur = 0
            self.seek(0)
            while cur < self.length:
                toread = min(512, self.length - cur)
                yield self.read(toread)
                cur += toread

        def __repr__(self):
            return '<File with name: %r; location: %d; length: %d>' % (
                    self.name,
                    self._location,
                    self.length,
                    )

        def read(self, count=1):
            sector = self._media.tell()
            if sector < self._location:
                raise RuntimeError
            if sector - self._location + count > self.length:
                raise RuntimeError
            return self._media.read(count)

        def read_sector(self, offset, count=1):
            self.seek(offset)
            return self.read(count)

        def seek(self, offset):
            if offset > self.length:
                raise RuntimeError
            return self._media.seek(self._location + offset)

    def __init__(self, media, ifo, bup, menu_vob, title_vob=[]):
        input = [ifo, bup]

        if menu_vob:
            input.insert(1, menu_vob)

        input[-1:-1] = title_vob

        files = []

        for i, j in itertools.zip_longest(input[:-1], input[1:]):
            ad_i = i.entry.ad[0]
            ad_j = j.entry.ad[0]

            location = ad_i.location_absolute
            length = ad_j.location_absolute - location

            files.append(self.File(media, i.name, location, length))

        i = input[-1]
        ad_i = i.entry.ad[0]
        location = ad_i.location_absolute
        length = files[0].length

        files.append(self.File(media, i.name, location, length))

        self.list = files[:]

        self.ifo = files.pop(0)
        self.bup = files.pop(-1)
        if menu_vob:
            self.menu_vob = files.pop(0)
        else:
            self.menu_vob = None
        self.title_vob = files

    def __iter__(self):
        for i in self.list:
            yield i.name, i
