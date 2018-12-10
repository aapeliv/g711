"""Python bindings"""

from cffi import FFI
ffibuilder = FFI()


# Definitions for the functions we wish to create Python bindings for
ffibuilder.cdef("""
void alaw_encode(size_t length, int16_t *in_buf, int8_t *out_buf);
void alaw_decode(size_t length, int8_t *in_buf, int16_t *out_buf);
void ulaw_encode(size_t length, int16_t *in_buf, int8_t *out_buf);
void ulaw_decode(size_t length, int8_t *in_buf, int16_t *out_buf);
""")

INCLUDE_DIRS = ('.',)

SOURCES = ('g711.c', 'coder.c', 'main.c')

ffibuilder.set_source(
    '_g711',
    """
    #include "coder.h"
    """,
    include_dirs=INCLUDE_DIRS,
    sources=SOURCES
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
