"""Python bindings"""

from cffi import FFI
ffibuilder = FFI()


# Definitions for the functions we wish to create Python bindings for
ffibuilder.cdef("""
void  alaw_compress (long lseg, short *linbuf, short *logbuf);
void  alaw_expand (long lseg, short *logbuf, short *linbuf);
void  ulaw_compress (long lseg, short *linbuf, short *logbuf);
void  ulaw_expand (long lseg, short *logbuf, short *linbuf);
""")

INCLUDE_DIRS = ('.',)

SOURCES = ('g711.c',)

ffibuilder.set_source(
    '_g711',
    """
    #include "g711.h"
    """,
    include_dirs=INCLUDE_DIRS,
    sources=SOURCES
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
