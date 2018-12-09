void decode(long length, char *in_buf, short *out_buf) {
    short temp_buf[length];
    for (int i = 0; i < length; i++) {
        temp_buf[i] = ((short) in_buf[i]) & 0x00FF;
    }
    ulaw_expand(length, temp_buf, out_buf);
}
