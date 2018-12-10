from g711 import ffibuilder

BUFFER_SIZE = 8192

def decode_file():
    output_buf = ffi.new("int[]", BUFFER_SIZE)
    ffibuilder.decode()
    #