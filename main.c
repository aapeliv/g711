#include <stdio.h>

#include "g711.h"
#include "decode.h"

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
