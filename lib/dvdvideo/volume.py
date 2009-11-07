from .ifo import VMGHeader

class VMG(object):
    def __init__(self, buf):
        self.header = VMGHeader(buf)
