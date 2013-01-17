#!/usr/bin/python3
"""
@copyright: 2009-2013 Bastian Blank <waldi@debian.org>
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

from distutils.core import setup

version = open('debian/changelog').readline().split(' ', 2)[1].lstrip('(').rstrip(')').rsplit('-', 1)[0]

setup(
        name='python-dvdvideo',
        version=version,
        author='Bastian Blank',
        author_email='waldi@debian.org',
        packages=[
            'dvdvideo',
            'dvdvideo.udf',
        ],
        scripts=[
            'dvdvideo-backup-image'
        ],
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        ],
)
