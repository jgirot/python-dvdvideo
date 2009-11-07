import struct

class VMGHeader(object):
    _struct = struct.Struct('>12s I 12x IHI 58x Q 24x II 56x IIIIIIII 32x 1792x')

    def __init__(self, buf):
        data = self._struct.unpack(buf)

        (id,
                self.part_bup_end,
                self.part_ifo_end,
                version,
                category,
                pos,
                vmgi_mat_end,
                fp_pgc_start,
                self.part_menu_vob_start,
                vmgm1_start,
                vmgm2_start,
                vmgm3_start,
                vmgm4_start,
                vmgm5_start,
                vmgm6_start,
                vmgm7_start) = data

        if id != b'DVDVIDEO-VMG':
            raise RuntimeError

    @property
    def part_menu_vob_end(self):
        return self.part_bup_start - 1

    @property
    def part_bup_start(self):
        return self.part_bup_end - self.part_ifo_end
