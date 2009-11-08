class MenuVob(object):
    def __init__(self, file):
        self._file = file

    def dump(self):
        return self._file.dump(),


class TitleVob(object):
    def __init__(self, files):
        self._files = files

    def dump(self):
        for file in self._files:
            yield file.dump()
