#include <stdlib.h>

#include "g711.h"

void alaw_encode(size_t length, int16_t *in_buf, int8_t *out_buf) {
    int16_t temp_buf[length];
    alaw_compress(length, in_buf, temp_buf);
    for (size_t i = 0; i < length; i++) {
        out_buf[i] = (int8_t) (temp_buf[i] & 0xFF);
    }
}

void alaw_decode(size_t length, int8_t *in_buf, int16_t *out_buf) {
    int16_t temp_buf[length];
    for (size_t i = 0; i < length; i++) {
        temp_buf[i] = ((int16_t) in_buf[i]) & 0xFF;
    }
    alaw_expand(length, temp_buf, out_buf);
}

void ulaw_encode(size_t length, int16_t *in_buf, int8_t *out_buf) {
    int16_t temp_buf[length];
    ulaw_compress(length, in_buf, temp_buf);
    for (size_t i = 0; i < length; i++) {
        out_buf[i] = (int8_t) (temp_buf[i] & 0xFF);
    }
}

void ulaw_decode(size_t length, int8_t *in_buf, int16_t *out_buf) {
    int16_t temp_buf[length];
    for (size_t i = 0; i < length; i++) {
        temp_buf[i] = ((int16_t) in_buf[i]) & 0xFF;
    }
    ulaw_expand(length, temp_buf, out_buf);
}