Name: freenx-server
Version: 0.7.3
Release: alt1

Summary: Freenx application/thin-client server
Group: Networking/Remote access
License: GPLv2
Url: http://freenx.berlios.de

Packager: Boris Savelev <boris@altlinux.org>

Source: %name-%version.tar.bz2
Source1: %name.init
Source2: %name.outformat

# ALT
Patch10: freenx-alt-luser.patch
Patch11: freenx-alt-openssh.patch
Patch12: freenx-alt-disable-adduser-and-group.patch
Patch13: freenx-alt-foomatic-ppdfile.patch
Patch16: freenx-alt-ld_library_path.patch
Patch18: freenx-centos-dbus.patch
Patch19: freenx-alt-Xsession.patch
Patch20: freenx-alt-nxnode.patch

Obsoletes: freenx
Provides: freenx = %version

Requires: nx
Requires: openssl
Requires: netcat
Requires: expect
Requires: foomatic-db-engine

BuildPreReq: rpm-build-compat
BuildRequires: imake xorg-cf-files gccmakedep

%description
Freenx is an application/thin-client server based on nx technology.
NoMachine nx is the next-generation X compression and roundtrip suppression
scheme. It can operate remote X11 sessions over 56k modem dialup links
or anything better. This package contains a free (GPL) implementation
of the nxserver component.

%prep
%setup -q

%patch10 -p1
%patch11 -p0
%patch12 -p0
%patch13 -p1
%patch16 -p0
%patch18 -p1
%patch19 -p0
%patch20 -p0

%build
%make_build

%install
# wrong install path
sed -i "s|/usr/lib|%_libdir|g" nxredir/Makefile
# install use nxloadconfig
sed -i "s|/usr/lib|%_libdir|g" nxloadconfig
sed -i "s|\$NX_DIR/lib|%_libdir|g" nxloadconfig
export NX_ETC_DIR=%_initdir/%name
%makeinstall_std
mv -f %buildroot%_sysconfdir/nxserver/node.conf.sample %buildroot%_sysconfdir/nxserver/node.conf
mkdir -p %buildroot%_initdir
install -m 755 %SOURCE1 %buildroot%_initdir/%name
%if %_vendor == "alt"
%else
install -m 755 %SOURCE2 %buildroot%_initdir
%endif
sed -i "s|/usr/lib|%_libdir|g" %buildroot%_bindir/nxredir
sed -i "s|/usr/lib|%_libdir|g" %buildroot%_libdir/cups/backend/nxsmb

%pre
%groupadd nx 2> /dev/null ||:
%useradd -g nx -G utmp -d /var/lib/nxserver/home/ -s %_bindir/nxserver \
        -c "NX System User" nx 2> /dev/null ||:
if [ ! -d %_datadir/fonts/misc ] && [ ! -e %_datadir/fonts/misc ] && [ -d %_datadir/fonts/bitmap/misc ]
then
    ln -s %_datadir/fonts/bitmap/misc %_datadir/fonts/misc
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
%if %_vendor == "alt"
%else
%_initdir/%name.outformat
%endif
%_bindir/nx*
%_libdir/*.so.*
%_libdir/cups/backend/nx*
%changelog
* Mon Aug 11 2008 Boris Savelev <boris@altlinux.org> 0.7.3-alt1
- svn update to r565
- fix x86_64 build

* Tue Jul 15 2008 Boris Savelev <boris@altlinux.org> 0.7.2-alt2
- svn update to r546

* Fri Jun 13 2008 Boris Savelev <boris@altlinux.org> 0.7.2-alt1
- new version
- fix altbug #16049
- new init-script

* Mon Jan 14 2008 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt5.r430
- fix path for libXrender

* Sun Jan 06 2008 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt4.r430
- fix font path (#13830)

* Thu Jan 03 2008 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt3.r430
- update from svn

* Fri Dec 28 2007 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt2.r427
- mark %_sysconfdir/nxserver/node.conf a config(noreplace)
- own %_sysconfdir/nxserver dir
- add requires nx

* Mon Dec 24 2007 Igor Zubkov <icesik@altlinux.org> 0.7.2-alt1.r427
- build for Sisyphus

