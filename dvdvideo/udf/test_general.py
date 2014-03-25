"""
@copyright: 2014 Bastian Blank <waldi@debian.org>
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

import pytest

from .general import *


class TestOSTACompressedUnicode:
    def test_stype_8(self):
        i = b'\x08test'
        assert OSTACompressedUnicode(i) == 'test'

    def test_stype_16(self):
        i = b'\x10\00t\00e\00s\00t'
        assert OSTACompressedUnicode(i) == 'test'

    def test_stype_16_truncated(self):
        pytest.xfail('Truncated string allowed by OSTA Compressed Unicode')
        i = b'\x10\00t\00e\00s\00t\00'
        assert OSTACompressedUnicode(i) == 'test\00'

    def test_stype_invalid(self):
        i = b'\x01test'
        with pytest.raises(ValueError):
            OSTACompressedUnicode(i)


class TestExtentAD:
    def test_size(self):
        assert ExtentAD.size == 20

    def test_decode_0(self):
        e = ExtentAD(b'\x00'*ExtentAD.size)
        assert e.flags == 0
        assert e.length == 0
        assert e.location == 0
        assert e.partition == 0

    def test_decode_1(self):
        e = ExtentAD(b'\xff'*ExtentAD.size)
        assert e.flags == 0x3
        assert e.length == 0x3fffffff
        assert e.location == 0xffffffff
        assert e.partition == 0xffff


class TestLongAD:
    def test_size(self):
        assert LongAD.size == 16

    def test_decode_0(self):
        e = LongAD(b'\x00'*LongAD.size)
        assert e.flags == 0
        assert e.length == 0
        assert e.location == 0
        assert e.partition == 0

    def test_decode_1(self):
        e = LongAD(b'\xff'*LongAD.size)
        assert e.flags == 0x3
        assert e.length == 0x3fffffff
        assert e.location == 0xffffffff
        assert e.partition == 0xffff


class TestShortAD:
    def test_size(self):
        assert ShortAD.size == 8

    def test_decode_0(self):
        e = ShortAD(b'\x00'*ShortAD.size)
        assert e.flags == 0
        assert e.length == 0
        assert e.location == 0

    def test_decode_1(self):
        e = ShortAD(b'\xff'*ShortAD.size)
        assert e.flags == 0x3
        assert e.length == 0x3fffffff
        assert e.location == 0xffffffff

