"""
@copyright: 2009 Bastian Blank <waldi@debian.org>
@license: GNU GPL-3
"""
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class ProgressMeter(object):
    def __init__(self, stream, total, count=0):
        self.stream = stream
        self.total = total
        self.count = count

        self.meter_ticks = 60

        stream.set_meter(self)

    def clear(self):
        self.stream.write_real(chr(27) + '[M' + chr(27) + '[G')

    def display(self):
        value = int(self.count / self.total * self.meter_ticks)

        meter = ['[%s>%s]' % ('-' * value, ' ' * (self.meter_ticks - value))]
        meter.append('%d/%d %d%%' % (self.count, self.total, self.count / self.total * 100))

        self.stream.write_real(' '.join(meter))
        self.stream.flush()

    def set(self, count):
        self.count = min(count, self.total)
        self.clear()
        self.display()

    def update(self, count):
        self.set(self.count + count)

    def write(self, str):
        self.clear()
        self.stream.write_real(str)
        self.display()


class ProgressStream(object):
    def __init__(self, stream):
        self.stream = stream

        self._meter = None

    def clear_meter(self):
        self.set_meter(None)

    def flush(self):
        self.stream.flush()

    def set_meter(self, meter):
        if self._meter:
            self._meter.clear()
        self._meter = meter
        if self._meter:
            self._meter.display()

    def write(self, str):
        if self._meter:
            self._meter.write(str)
        else:
            self.stream.write(str)

    def write_real(self, str):
        return self.stream.write(str)
