# python-dvdvideo

I (jgirot) am not the original author of this software or the following information about it.

The following was copied from http://bblank.thinkmo.de/blog/archive/2010/08/29/new-software-python-dvdvideo on Sept 13, 2016 so that the code might be better understood in that context. Also, it was copied here for posterity in case the original source is removed or otherwise unavailable.

Begin Original Blog post:

python-dvdvideo is a library to read DVD-Video images. It includes a tool to dump encrypted DVD-Video images. It is implemented in Python 3.

After a long time, I decided to write again. I decided to start with software I wrote for my own usage that could be usefull for other people. I'll start with python-dvdvideo, a DVD-Video reader written in Python 3, and the reference tool dvd-video-backup-image, a generic DVD-Video dumper. Lets see, if this blog will see more postings in the future.

Intention

I started to write this software, because libdvdread was often unable to decipher my newly purchased video DVDs. libdvdread expects a rather valid structure of the filesystem and other metadata on the disk. It will forcefully bail out on several error conditions. So I often ended patching libdvdread to make dvdbackup able to read the new disks.

Usually there are two ways to create backups of such DVDs, as files or complete images. Dumping them as files have large problems if there are certain defects in the filesystem, like some space is referenced in several titlesets. I have a disk that produces 25GiB of output during such a dump. So the less problematic way to do that is to dump the complete image. That is the way I used in the tool I built on top of this.

Parts

The software is devided into several parts. First a small UDF reader. On top of this comes a DVD video reader. It makes use of libdvdcss wrapper. All of this is used to implement a small tool to dump whole images. I will describe this parts here.

UDF reader

The UDF reader implements a minimal set of features. I implemented only the stuff I found as needed and used in the available DVDs. This reader allows to read the lowlevel UDF, used as base of all video DVDs.

DVD video reader

The dvd video reader uses the UDF reader to get the necessary information from the disk. Again this reader is quiet smallish. It only trusts the UDF for the starts of titlesets and expects that anything else is listed in the info files. This allows to read even discs with broken filesystems, which are really common.

libdvdcss wrapper

The libdvdcss wrapper is implemented using ctypes. The ctypes library allows easy access to functions defines in shared object. The library allows calling of the functions and maps arguments and return values to the Python datatypes. This wrapper allows me to read also encrypted DVDs.

Image dumper

This tool allows to dump a encrypted video DVD into a file. It tries to detect encrypted (video/vob files) and unencrypted (info files, otherwise used space) parts of the disk. This way it is able to dump anything, as long as it can read the filesystem and info files. However, some discs contains overlapping areas, which can't be that easily deguised.

The tool includes a small conflict resolver that handles overlapping parts. It uses a set of rules to allow some types to coexist and some to be modified. On of the rules relabels things included in an info files but also a title vob as always unencrypted. With this resolver, most of the problems can be handled and we get a playable result.

License and distribution

This package is licensed GPL 3 or later. It is for new distributed via Alioth (git://git.debian.org/users/waldi/python-dvdvideo.git)

Conclusion

This tool allows me to dump all video DVDs I got my hands on in the last time. It allows me to watch the videos on my notebook that have no optical disc reader on its own. Maybe someone may need such a tool also.
