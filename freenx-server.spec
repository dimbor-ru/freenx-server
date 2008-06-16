Name: freenx-server
Version: 0.7.2
Release: alt1

Summary: Freenx application/thin-client server
Group: Networking/Remote access
License: GPLv2
URL: http://freenx.berlios.de

Packager: Boris Savelev <boris@altlinux.org>

Source0: http://download.berlios.de/freenx/%name-%version.tar.gz
#Source0: %name-%version.tar.bz2

# ALT
Patch10: freenx-alt-luser.patch
Patch11: freenx-alt-openssh.patch
Patch12: freenx-alt-disable-adduser-and-group.patch
Patch13: freenx-alt-foomatic-ppdfile.patch
Patch16: freenx-alt-ld_library_path.patch
Patch18: freenx-centos-dbus.patch
Patch19: freenx-alt-Xsession.patch

Obsoletes: freenx
Provides: freenx = %version

Requires: nx
Requires: openssl
Requires: netcat
Requires: foomatic-db-engine
Requires: dbus-tools-gui

# Automatically added by buildreq on Fri Jun 13 2008
BuildRequires: imake xorg-cf-files

%description
Freenx is an application/thin-client server based on nx technology. 
NoMachine nx is the next-generation X compression and roundtrip suppression
scheme. It can operate remote X11 sessions over 56k modem dialup links
or anything better. This package contains a free (GPL) implementation
of the nxserver component.

%prep
%setup -q
#patch0 -p0

%patch10 -p1
%patch11 -p1
%patch12 -p0
%patch13 -p1
%patch16 -p0
%patch18 -p1
%patch19 -p0

%build
%make

%install
%makeinstall_std
mv -f %buildroot%_sysconfdir/nxserver/node.conf.sample %buildroot%_sysconfdir/nxserver/node.conf
mkdir -p %buildroot%_initdir
install -m 755 init.d/%name %buildroot%_initdir

%pre
/usr/sbin/groupadd -r -f nx 2> /dev/null ||:
/usr/sbin/useradd -r -g nx -G utmp -d /var/lib/nxserver/home/ -s /usr/bin/nxserver \
        -c "NX System User" nx 2> /dev/null ||:
if [ ! -h /usr/share/fonts/misc ]
then
    ln -s /usr/share/fonts/bitmap/misc /usr/share/fonts/misc
fi

%post
%post_service %name

%preun
%preun_service %name

%files
%doc AUTHORS ChangeLog CONTRIB nxcheckload.sample node.conf.sample
%dir %_sysconfdir/nxserver
%config(noreplace) %_sysconfdir/nxserver/node.conf
%_initdir/%name
%_bindir/nx*
%_libdir/*.so.*
%_libdir/cups/backend/nx*
%changelog
* Fri Jun 13 2008 Boris Savelev <boris@altlinux.org> 0.7.2-alt1
- new version

* Mon Jan 14 2008 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt5.r430
- fix path for libXrender

* Sun Jan 06 2008 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt4.r430
- fix font path (#13830)

* Thu Jan 03 2008 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt3.r430
- update from svn

* Fri Dec 28 2007 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt2.r427
- mark /etc/nxserver/node.conf a config(noreplace)
- own /etc/nxserver dir
- add requires nx

* Mon Dec 24 2007 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt1.r427
- build for Sisyphus

