class ProgressStream(object):
    def __init__(self, stream, total=-1, count=0):
        self.stream = stream
        self.total = total
        self.count = count

        self.meter_ticks = 60

        self._display()

    def _clear(self):
        self.stream.write(chr(27) + '[M')
        self.stream.write(chr(27) + '[G')

    def _display(self):
        value = int(self.count / self.total * self.meter_ticks)

        meter = ['[%s>%s]' % ('-' * value, ' ' * (self.meter_ticks - value))]

        if self.total > 0:
            perc = self.count / self.total * 100
            meter.append('%d/%d %d%%' % (self.count, self.total, perc))
        else:
            meter.append('%d' % self.count)

        self.stream.write(' '.join(meter))
        self.stream.flush()

    def close(self):
        self._clear()

    def set(self, count):
        self.count = min(count, self.total)
        self._clear()
        self._display()

    def set_total(self, total):
        self.total = total
        self._clear()
        self._display()

    def update(self, count):
        self.set(self.count + count)

    def write(self, str):
        self._clear()
        self.stream.write(str)
        if str[-1] != '\n':
            self.stream.write('\n')
        self._display()

