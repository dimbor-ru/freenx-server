Name: freenx-server
Version: 0.7.4
Release: alt3

Summary: Freenx application/thin-client server
Group: Networking/Remote access
License: GPLv2
Url: http://freenx.berlios.de

Packager: Boris Savelev <boris@altlinux.org>

Source: %name-%version.tar.bz2
Source1: %name.init
Source2: %name.outformat

Obsoletes: freenx
Provides: freenx = %version

Requires: nx
Requires: openssl
Requires: netcat
Requires: expect
Requires: foomatic-db-engine
%if %_vendor == "alt"
Requires: dbus-tools-gui
Requires: binutils
%endif
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

mkdir -p %_var/lib/nxserver

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
%_var/lib/nxserver

%changelog
* Tue Nov 11 2008 Boris Savelev <boris@altlinux.org> 0.7.4-alt3
- add /var/lib/nxserver

* Fri Sep 05 2008 Boris Savelev <boris@altlinux.org> 0.7.4-alt2
- Fixed non-encrypted session mode. You might need to set EXTERNAL_PROXY_IP in node.conf.

* Thu Aug 28 2008 Boris Savelev <boris@altlinux.org> 0.7.4-alt1
- Opened the 0.7.4 development.
- Fixed missing export of NX_ETC_DIR in Makefile, so node.conf.sample is installed correctly.
- Fixed broken round-robin load balance algorithm.
- Fixed --terminate|--suspend|--force-terminate for load balancing case.
- Fixed --terminate|--suspend|--force-terminate for usermode case.

* Sat Aug 23 2008 Boris Savelev <boris@altlinux.org> 0.7.3-alt3
- Changed type for external agents to windows-helper or vnc-helper so that those sessions can be mirrored / shadowed as well.
- Added nxshadowacl.sample component to be able to shadow foreign sessions.
- Prepared shadowing foreign users for VNC-shadowing.
- Added shadow support to --listsession command.
- Added shadow mode as nxagent target.
- Fixed shadow mode and made it usable.

* Mon Aug 18 2008 Boris Savelev <boris@altlinux.org> 0.7.3-alt2
- Build from git
- Finally checked for all service ports. (cups, media, samba) and also checked it on the host where the load balancing actually leads to.
- Fixed broken fallback logic if SSH_CLIENT variables cannot be read correctly.
- Overhauled the usermode:
- There are now two modes of operation.
- One statically setting the ENABLE_USERMODE_AUTHENTICATION key in node.conf. (old behavior)
- Or using nxserver-usermode as startup binary, which directly goes into the 103 stage.
- Fixed using commandline parameters like --cleanup for static usermode.
- Enabled the root commandline parameters in usermode.
- Fixed usage of "nx" user as normal user in usermode.
- Disabled slave mode and load balancing for usermode.
- Fixed creation of the logfile directory.
- Fixed nxnode usage of SSH_CLIENT using fallback mechanism.
- Added disabled nxserver-suid wrapper with help from Google. To enable it uncomment the suid_install target in Makefile.
- Automatically disabled slave mode, when load balancing is activated.
- Made ENABLE_SLAVE_MODE="1" the new default as its faster and more reliable. If you encounter any problems with it, disable it in node.conf.

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

