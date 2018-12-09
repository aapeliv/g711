build: g711.o
	cc main.c -o decoder g711.o

g711:
	cc g711.h -o g711.o
