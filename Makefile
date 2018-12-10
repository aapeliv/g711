build: coder.o g711.o
	cc main.c -o g711 coder.o g711.o

coder: g711.o
	cc coder.c -o coder.o g711.o

g711:
	cc g711.h -o g711.o
