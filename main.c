#include <stdio.h>
#include <string.h>

#include "coder.h"

#define BUFFER_SIZE 8192

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Not enough arguments, need -d or -e followed by alaw or ulaw, as well as input and output file names\n");
        return 1;
    }

    int mode = 0;

    if (strcmp(argv[1], "-d") == 0) {
        mode = 0;
    } else if (strcmp(argv[1], "-e") == 0) {
        mode = 2;
    } else {
        printf("Please specify either -e or -d for encoding or decoding, respectively\n");
        return 1;
    }

    if (strcmp(argv[2], "alaw") == 0) {
        mode += 1;
    } else if (strcmp(argv[2], "ulaw") == 0) {
        mode += 0;
    } else {
        printf("Please specify either alaw or ulaw\n");
        return 1;
    }

    FILE *fp = fopen(argv[3], "r");

    if (fp == NULL) {
        printf("Failed to open input file (%s) for reading\n", argv[3]);
        return 1;
    }

    FILE *fo = fopen(argv[4], "w+");

    if (fo == NULL) {
        printf("Failed to open output file (%s) for reading\n", argv[4]);
        return 1;
    }

    if (mode == 0 || mode == 1) {
        int8_t  c_buffer[BUFFER_SIZE];
        int16_t o_buffer[BUFFER_SIZE];

        int bytes_read = 0;
        while ((bytes_read = fread(c_buffer, sizeof(int8_t), BUFFER_SIZE, fp)) != 0) {
            if (mode == 0) {
                ulaw_decode(bytes_read, c_buffer, o_buffer);
            } else {
                alaw_decode(bytes_read, c_buffer, o_buffer);
            }
            fwrite(o_buffer, sizeof(int16_t), bytes_read, fo);
        }
    } else {
        int16_t  c_buffer[BUFFER_SIZE];
        int8_t o_buffer[BUFFER_SIZE];

        int bytes_read = 0;
        while ((bytes_read = fread(c_buffer, sizeof(int16_t), BUFFER_SIZE, fp)) != 0) {
            if (mode == 0) {
                ulaw_encode(bytes_read, c_buffer, o_buffer);
            } else {
                alaw_encode(bytes_read, c_buffer, o_buffer);
            }
            fwrite(o_buffer, sizeof(int8_t), bytes_read, fo);
        }
    }

    return 0;
}
