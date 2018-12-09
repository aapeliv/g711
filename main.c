#include <stdio.h>

#include "g711.h"

void decode(long length, char *in_buf, short *out_buf) {
    short temp_buf[length];
    for (int i = 0; i < length; i++) {
        temp_buf[i] = ((short) in_buf[i]) & 0x00FF;
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

    char  c_buffer[BUFFER_SIZE];
    short o_buffer[BUFFER_SIZE];

    int bytes_read = 0;
    while ((bytes_read = fread(c_buffer, sizeof(char), BUFFER_SIZE, fp)) != 0) {
        decode(bytes_read, c_buffer, o_buffer);
        fwrite(o_buffer, sizeof(short), bytes_read, fo);
    }
    return 0;
}