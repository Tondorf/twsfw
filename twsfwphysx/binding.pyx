cdef extern from "twsfwphysx/twsfwphysx.h":
    const char* twsfwphysx_version()


cdef class Engine():
    def __init__(self):
        pass

    @property
    def __version__(self):
        cdef const char* version = twsfwphysx_version()
        return version.decode("utf-8")
