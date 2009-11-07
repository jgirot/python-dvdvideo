import os

from .volume import Volume

class Media(object):
    def __init__(self, filename):
        self._media = open(filename, 'rb')

    def read_sector(self, sector, count=2048):
        count_align = (count + 2047) & ~2047
        # TODO
        self._media.seek(sector * 2048)
        return self._media.read(count_align)

    @property
    def volume(self):
        return Volume(self)
