PREFIX          ?= /usr
PATH_BIN        ?= $(PREFIX)/bin
PATH_LIB        ?= $(PREFIX)/lib
CUPS_BACKEND    ?= $(PREFIX)/lib/cups/backend

all: libnxredir.so

CC=gcc
CFLAGS=-g -O2 -Wall -fPIC
LIBNAME=libnxredir.so
VERSION=0

libnxredir.so: nxredir.o
	$(CC) -fPIC $(CFLAGS) -nostdlib -shared -Wl,-soname,$(LIBNAME).$(VERSION) -o $(LIBNAME).$(VERSION) nxredir.o -ldl -lc

clean:
	rm -f $(LIBNAME)
	rm -f $(LIBNAME).$(VERSION)
	rm -f *.o

install:
	install -m755 -s $(LIBNAME).$(VERSION) $(DESTDIR)/$(PATH_LIB)/
	install -m755 nxredir $(DESTDIR)/$(PATH_BIN)/
	install -m755 nxsmb $(DESTDIR)/$(CUPS_BACKEND)/
	sed -i -e 's|PATH_LIB=.*|PATH_LIB='$(PATH_LIB)'|' $(DESTDIR)/$(PATH_BIN)/nxredir
	sed -i -e 's|PATH_LIB=.*|PATH_LIB='$(PATH_LIB)'|' $(DESTDIR)/$(CUPS_BACKEND)/nxsmb
	sed -i -e 's|CUPS_BACKEND=.*|CUPS_BACKEND='$(CUPS_BACKEND)'|' $(DESTDIR)/$(CUPS_BACKEND)/nxsmb

.PHONY: clean install
