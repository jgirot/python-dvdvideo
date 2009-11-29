class ProgressStream(object):
    def __init__(self, stream, total, count=0):
        self.stream = stream
        self.total = total
        self.count = 0

        self.meter_ticks = 60
        self.meter_division = self.total / self.meter_ticks

        self.update(count)

    def _clear(self):
        self.stream.write(chr(27) + '[M')
        self.stream.write(chr(27) + '[G')

    def _display(self):
        value = int(self.count / self.meter_division)
        bar = '-' * value
        pad = ' ' * (self.meter_ticks - value)
        perc = self.count / self.total * 100
        meter = '[%s>%s] %d/%d %d%%' % (bar, pad, self.count, self.total, perc)

        self.stream.write(meter)
        self.stream.flush()

    def close(self):
        self._clear()

    def update(self, count):
        self.count = min(self.count + count, self.total)
        self._clear()
        self._display()

    def write(self, str):
        self._clear()
        self.stream.write(str)
        if str[-1] != '\n':
            self.stream.write('\n')
        self._display()

