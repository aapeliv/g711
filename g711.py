__all__ = ['alaw_encode', 'alaw_decode', 'ulaw_encode', 'ulaw_decode', 'g711_read', 'g711_write', 'open']

from _g711.lib import alaw_encode as _alaw_encode, alaw_decode as _alaw_decode, ulaw_encode as _ulaw_encode, ulaw_decode as _ulaw_decode

import builtins

from cffi import FFI
ffi = FFI()


class Error(Exception):
    pass


def _apply(bytes_in, func, encode):
    if encode and len(bytes_in) % 2 != 0:
        raise Error("Number of bytes to be encoded must be even as each sample requires two bytes")
    div = 2 if encode else 1
    in_buf = ffi.new("int16_t[]" if encode else "int8_t[]", len(bytes_in) // div)
    ot_buf = ffi.new("int8_t[]" if encode else "int16_t[]", len(bytes_in) // div)

    ffi.buffer(in_buf)[:] = bytes_in
    func(len(bytes_in) // div, in_buf, ot_buf)
    return bytes(ffi.buffer(ot_buf))

def alaw_encode(bytes_in):
    return _apply(bytes_in, _alaw_encode, True)

def alaw_decode(bytes_in):
    return _apply(bytes_in, _alaw_decode, False)

def ulaw_encode(bytes_in):
    return _apply(bytes_in, _ulaw_encode, True)

def ulaw_decode(bytes_in):
    return _apply(bytes_in, _ulaw_decode, False)


class g711_read:
    def __init__(self, file, law):
        self._opened = False
        if isinstance(file, str):
            file = builtins.open(file, 'rb')
            self._opened = True
        self.file = file
        if law != 'alaw' and law != 'ulaw':
            raise Error("Law must be either ulaw or alaw")
        self.law = law

    def readsamples(self, number=None):
        if self.law == 'alaw':
            return alaw_decode(self.file.read(number))
        else:
            return ulaw_decode(self.file.read(number))

    def close(self):
        if self._opened:
            self.file.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class g711_write:
    def __init__(self, file, law):
        self._opened = False
        if isinstance(file, str):
            file = builtins.open(f, 'wb')
            self._opened = True
        self.file = file
        if law != 'ulaw' and law != 'alaw':
            raise Error("Law must be either ulaw or alaw")
        self.law = law

    def writesamples(self, samples):
        if self.law == 'alaw':
            self.file.write(alaw_encode(samples))
        else:
            self.file.write(ulaw_encode(samples))

    def close(self):
        if self._opened:
            self.file.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def open(filename, mode, law):
    if mode in ('r', 'rb', 'r+b'):
        return g711_read(filename, law)
    elif mode in ('w', 'wb', 'w+b'):
        return g711_write(filename, law)
    else:
        raise Error("Invalid mode, expecting one of 'r', 'rb', 'r+b', 'w', 'wb', and 'w+b'.")