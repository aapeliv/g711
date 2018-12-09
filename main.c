#include <stdio.h>

#include "g711.h"

void decode(size_t length, int8_t *in_buf, int16_t *out_buf) {
    int16_t temp_buf[length];
    for (size_t i = 0; i < length; i++) {
        temp_buf[i] = ((int16_t) in_buf[i]) & 0x00FF;
    }
    ulaw_expand(length, temp_buf, out_buf);
}

#define BUFFER_SIZE 8192

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Not enough arguments, need input and output files\n");
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    FILE *fo = fopen(argv[2], "w+");

    int8_t  c_buffer[BUFFER_SIZE];
    int16_t o_buffer[BUFFER_SIZE];

    int bytes_read = 0;
    while ((bytes_read = fread(c_buffer, sizeof(int8_t), BUFFER_SIZE, fp)) != 0) {
        decode(bytes_read, c_buffer, o_buffer);
        fwrite(o_buffer, sizeof(int16_t), bytes_read, fo);
    }
    return 0;
}