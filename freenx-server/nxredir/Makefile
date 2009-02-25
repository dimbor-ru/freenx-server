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

ifneq ($(NX_VERSION),)
install: all
	install -m755 $(LIBNAME).$(VERSION) $(DESTDIR)/$$PATH_LIB/freenx-server/
	install -m755 nxredir $(DESTDIR)/$$PATH_BIN/
	install -m755 nxsmb $(DESTDIR)/$$CUPS_BACKEND/
	perl -pi -e "s,PATH_LIB=.*,PATH_LIB=\"$$PATH_LIB\",g" $(DESTDIR)/$$PATH_BIN/nxredir
	perl -pi -e "s,PATH_LIB=.*,PATH_LIB=\"$$PATH_LIB\",g" $(DESTDIR)/$$CUPS_BACKEND/nxsmb
	perl -pi -e "s,CUPS_BACKEND=.*,CUPS_BACKEND=\"$$CUPS_BACKEND\",g" $(DESTDIR)/$$CUPS_BACKEND/nxsmb
else
install: all
	install -m755 $(LIBNAME).$(VERSION) $(DESTDIR)/usr/lib/freenx-server/
	install -m755 nxredir $(DESTDIR)/usr/bin
	install -m755 nxsmb $(DESTDIR)/usr/lib/cups/backend/
endif

.PHONY: clean install
