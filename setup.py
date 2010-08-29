#!/usr/bin/python3

from distutils.core import setup

setup(
        name='python-dvdvideo',
        version='0.1',
        author='Bastian Blank',
        author_email='waldi@debian.org',
        packages=('dvdvideo', 'dvdvideo.udf'),
        package_dir = {'': 'lib'},
        scripts=('bin/dvdvideo-backup-image', ),
)
