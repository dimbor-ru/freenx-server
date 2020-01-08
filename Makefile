.PHONY: all install clean nxenv_install suid_install

SHELL = /bin/bash

# helpers for "install" target
INSTALL_DIR=install -d -m 755
INSTALL_FILE=install -m 644 -C
INSTALL_PROGRAM=install -m 755
INSTALL_SYMLINK=ln -s -f

NX_ETC_DIR      ?= /etc/nxserver
PREFIX          ?= /usr
PATH_BIN        ?= $(PREFIX)/bin
PATH_LIB        ?= $(PREFIX)/lib
CUPS_BACKEND    ?= $(PREFIX)/lib/cups/backend
PATH_SHARE      ?= $(PREFIX)/share

NX_VERSION=`cat VERSION 2>/dev/null`

SUBDIRS=nxredir nxviewer-passwd nxserver-helper nxserver-suid nx-session-launcher
PROGRAMS=nxacl.sample nxacl.app nxcheckload.sample nxcups-gethost nxdesktop_helper nxdialog.freenx nxkeygen nxloadconfig nxnode nxnode-login nxprint nxserver nxsetup nxviewer_helper nx-session-launcher/nx-session-launcher nxserver-usermode
PROGRAMS_BIN=nxserver-helper/nxserver-helper nxviewer-passwd/nxpasswd/nxpasswd nx-session-launcher/nx-session-launcher-suid nxserver-suid/nxserver-suid

all:
	cd nxviewer-passwd && xmkmf && make Makefiles && make depend
	export PATH_BIN PATH_LIB CUPS_BACKEND NX_VERSION NX_ETC_DIR &&\
	for i in $(SUBDIRS) ; \
	do\
		echo "making" all "in $$i..."; \
	        $(MAKE) -C $$i all || exit 1;\
	done

suid_install:
	chown nx:root $(DESTDIR)/$(PATH_BIN)/nxserver-suid
	chmod 4755 $(DESTDIR)/$(PATH_BIN)/nxserver-suid
	chown nx:root $(DESTDIR)/$(PATH_BIN)/nx-session-launcher-suid
	chmod 4755 $(DESTDIR)/$(PATH_BIN)/nx-session-launcher-suid
	chown :users $(DESTDIR)/$(NX_ETC_DIR)/ppd
	chmod 775 $(DESTDIR)/$(NX_ETC_DIR)/ppd
	chown nx:nx $(DESTDIR)/var/lib/nxserver/home/
	chown nx:nx  $(DESTDIR)/var/lib/nxserver/db/


nxenv_install:
	$(INSTALL_DIR) $(DESTDIR)/$(PATH_BIN)/
	$(INSTALL_DIR) $(DESTDIR)/$(PATH_LIB)/freenx-server/
	$(INSTALL_DIR) $(DESTDIR)/$(NX_ETC_DIR)/
	$(INSTALL_FILE) conf/node.conf $(DESTDIR)/$(NX_ETC_DIR)/
	$(INSTALL_FILE) data/Xkbmap $(DESTDIR)/$(NX_ETC_DIR)/
	$(INSTALL_PROGRAM) data/fixkeyboard $(DESTDIR)/$(NX_ETC_DIR)/
	$(INSTALL_PROGRAM) data/Xsession $(DESTDIR)/$(NX_ETC_DIR)/
	$(INSTALL_DIR) $(DESTDIR)/$(NX_ETC_DIR)/node.conf.d/
	$(INSTALL_FILE) conf/conf.d/* $(DESTDIR)/$(NX_ETC_DIR)/node.conf.d/
	$(INSTALL_DIR) $(DESTDIR)/$(NX_ETC_DIR)/acls/
	$(INSTALL_FILE) conf/acls/* $(DESTDIR)/$(NX_ETC_DIR)/acls/
	install -m775 -gusers -d  $(DESTDIR)/$(NX_ETC_DIR)/ppd/
	$(INSTALL_DIR) $(DESTDIR)/$(PATH_SHARE)/freenx-server/node.conf.def
	$(INSTALL_FILE) conf/conf.d/* $(DESTDIR)/$(PATH_SHARE)/freenx-server/node.conf.def/
	$(INSTALL_DIR) $(DESTDIR)/$(CUPS_BACKEND)/
	$(INSTALL_DIR) $(DESTDIR)/etc/logrotate.d/
	$(INSTALL_FILE) data/logrotate $(DESTDIR)/etc/logrotate.d/freenx-server
	$(INSTALL_DIR) $(DESTDIR)/etc/sudoers.d/
	install -m400 data/sudoers.conf $(DESTDIR)/etc/sudoers.d/nxserver
	$(INSTALL_DIR) $(DESTDIR)/etc/dbus-1/system.d/
	$(INSTALL_FILE) nx-session-launcher/ConsoleKit-NX.conf $(DESTDIR)/etc/dbus-1/system.d/
	$(INSTALL_DIR) $(DESTDIR)/var/lib/nxserver/
	install -m2750 -d $(DESTDIR)/var/lib/nxserver/home/
	install -m2770 -d $(DESTDIR)/var/lib/nxserver/db/
	for i in $(PROGRAMS) ;\
	do\
	        $(INSTALL_PROGRAM) $$i $(DESTDIR)/$(PATH_BIN)/ || exit 1;\
	done
	for i in $(PROGRAMS_BIN) ;\
	do\
	        $(INSTALL_PROGRAM) -s $$i $(DESTDIR)/$(PATH_BIN)/ || exit 1;\
	done
	sed -i -e 's|NX_VERSION=.*|NX_VERSION='$(NX_VERSION)'|' \
			 -e 's|^PATH_LIB=.*|PATH_LIB='$(PATH_LIB)'|' $(DESTDIR)/$(PATH_BIN)/nxloadconfig
	$(MAKE) -C nxredir install
	#$(MAKE) suid_install

clean:
	for i in $(SUBDIRS) ; \
	do\
		echo "making" clean "in $$i..."; \
		if test -e "$$i/Makefile"; \
		then $(MAKE) -C $$i clean || exit 1;\
		else echo ignoring $$i;\
		fi;\
	done
	rm -f nxviewer-passwd/Makefile.back
	rm -f nxviewer-passwd/Makefile
	rm -f nxviewer-passwd/nxpasswd/Makefile
	rm -f nxviewer-passwd/libvncauth/Makefile

install:
	export PATH_BIN PATH_LIB CUPS_BACKEND NX_VERSION NX_ETC_DIR &&\
	$(MAKE) nxenv_install
