__all__ = ['alaw_encode', 'alaw_decode', 'ulaw_encode', 'ulaw_decode', 'g711_read', 'g711_write', 'open']

from _g711.lib import alaw_encode as _alaw_encode, alaw_decode as _alaw_decode, ulaw_encode as _ulaw_encode, ulaw_decode as _ulaw_decode

import builtins

from cffi import FFI
ffi = FFI()


def _apply(bytes_in, func, encode):
    """
    Transforms bytes_in into a C buffer of the right type and applies func to it,
    encode is either True for encoding or False for decoding, and changes the 
    underlying C buffer types.

    :param bytes_in: Python bytes object containing the data to be encoded or decoded
    :param func: one of _alaw_encode, _alaw_decode, _ulaw_encode, or _ulaw_decode to 
        apply to the bytes
    :param encode: binary flag of whether we're encoding or decoding
    :returns: bytes containing the encoded or decoded samples
    :raises ValueError: the number of bytes supplied was not a multiple of two when
        encoding
    """
    if encode and len(bytes_in) % 2 != 0:
        raise ValueError("Number of bytes to be encoded must be even as each sample requires two bytes")
    div = 2 if encode else 1

    # If we encode, we take 16-bit PCM samples (although we only use either 13 or 14
    # bits of them) and transform them into 8-bit G.711 encoded samples.
    # In the other direction, we take 8-bit G.711 encoded samples and transform them
    # into 16-bit PCM samples. However, Python bytes are always 8-bits each, so need
    # to divide by 2 if we're encoding (as each sample takes 2 bytes).
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
        if law not in ('alaw', 'ulaw'):
            raise ValueError("Law must be either ulaw or alaw")
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
        if law not in ('alaw', 'ulaw'):
            raise ValueError("Law must be either ulaw or alaw")
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
        raise ValueError("Invalid mode '{}', expecting one of 'r', 'rb', 'r+b', 'w', 'wb', and 'w+b'.".format(mode))