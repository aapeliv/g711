#include <stdlib.h>

void alaw_encode(size_t length, int16_t *in_buf, int8_t *out_buf);
void alaw_decode(size_t length, int8_t *in_buf, int16_t *out_buf);
void ulaw_encode(size_t length, int16_t *in_buf, int8_t *out_buf);
void ulaw_decode(size_t length, int8_t *in_buf, int16_t *out_buf);