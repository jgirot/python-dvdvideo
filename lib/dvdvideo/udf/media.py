from .volume import Volume

class Media(object):
    def __init__(self, file):
        self._file = file
        self._sector_size = 2048

    def read(self, count):
        count_align = (count + self._sector_size - 1) & ~(self._sector_size - 1)
        return self._file.read(count_align)

    def read_sector(self, offset, count=2048):
        self.seek(offset)
        return self.read(count)

    def seek(self, offset):
        return self._file.seek(offset * self._sector_size)

    @property
    def volume(self):
        return Volume(self)
