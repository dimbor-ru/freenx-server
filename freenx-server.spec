%define cups_root %_prefix/lib
Name: freenx-server
Version: 0.7.4
Release: alt10

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

# Debian based distr haven't /var/lock/subsys
if [ -d %_var/lock/subsys ] ; then
    LOCKDIR=%_var/lock/subsys
else
    LOCKDIR=%_var/lock
fi

# wrong install path
sed -i "s|/usr/lib|%_libdir|g" nxredir/Makefile
sed -i "s|%_libdir/cups|%cups_root/cups|g" Makefile
# install use nxloadconfig
sed -i "s|/usr/lib|%_libdir|g" nxloadconfig
sed -i "s|%_libdir/cups|%cups_root/cups|g" nxloadconfig
sed -i "s|\$NX_DIR/lib|%_libdir|g" nxloadconfig
# nxredir nxsmb
sed -i "s|/usr/lib|%_libdir|g" nxredir/nxredir
sed -i "s|/usr/lib|%_libdir|g" nxredir/nxsmb
sed -i "s|%_libdir/cups|%cups_root/cups|g" nxredir/nxsmb

export NX_ETC_DIR=%_initdir/%name
%makeinstall_std
mv -f %buildroot%_sysconfdir/nxserver/node.conf.sample %buildroot%_sysconfdir/nxserver/node.conf
mkdir -p %buildroot%_initdir
install -m 755 %SOURCE1 %buildroot%_initdir/%name
sed -i "s|~LOCKDIR~|$LOCKDIR|g" %buildroot%_initdir/%name
%if %_vendor == "alt"
%else
install -m 755 %SOURCE2 %buildroot%_initdir
%endif

mkdir -p %buildroot%_var/lib/nxserver/home
mkdir -p %buildroot%_var/lib/nxserver/db
mkdir -p %buildroot%_sysconfdir/nxserver/node.conf.d
mkdir -p %buildroot%_datadir/%name/node.conf.d
mkdir -p %buildroot%_sysconfdir/logrotate.d
mkdir -p %buildroot%_sysconfdir/dbus-1/system.d/
cp -p data/logrotate %buildroot%_sysconfdir/logrotate.d/freenx-server
cp -p nx-session-launcher/ConsoleKit-NX.conf %buildroot%_sysconfdir/dbus-1/system.d/
mv nx-session-launcher/README nx-session-launcher/README.suid

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
%doc AUTHORS ChangeLog CONTRIB nxcheckload.sample node.conf.sample nx-session-launcher/README.suid
%dir %_sysconfdir/nxserver
%dir %_sysconfdir/nxserver/node.conf.d
%config(noreplace) %_sysconfdir/nxserver/node.conf
%config %_sysconfdir/logrotate.d/freenx-server
%config %_sysconfdir/dbus-1/system.d/ConsoleKit-NX.conf
%_initdir/%name
%if %_vendor == "alt"
%else
%_initdir/%name.outformat
%endif
%attr(4711,nx,root) %_bindir/nx-session-launcher-suid
%_bindir/nx*
%_libdir/*.so.*
%cups_root/cups/backend/nx*
%attr(2750,nx,nx) %_var/lib/nxserver/home
%attr(2750,root,nx) %_var/lib/nxserver/db
%dir %_datadir/%name/node.conf.d

%changelog
* Sun Feb 22 2009 Boris Savelev <boris@altlinux.org> 0.7.4-alt10
- logrotate rule.
- add LSB header.
- patches from Ubuntu.
- implementation of guest login.
- nx-session-launcher:
    + add DBUS rules
    + fix permission on nx-session-launcher-suid
    + add README for nx-session-launcher

* Fri Feb 20 2009 Boris Savelev <boris@altlinux.org> 0.7.4-alt9
- fix nxloadconfig for Etersoft SHARE_FAST_MOUNT

* Thu Feb 19 2009 Boris Savelev <boris@altlinux.org> 0.7.4-alt8
- fix eterbug #3226 (patch from horch)
- add sleeping wait for valid display (fixkeyboard fails)

* Thu Jan 08 2009 Boris Savelev <boris@altlinux.org> 0.7.4-alt7
- fix path to cups backends on x86_64 (alt bug #18462)
- fix path to LOCKDIR on Debian (eter bug #3094)

* Tue Dec 16 2008 Boris Savelev <boris@altlinux.org> 0.7.4-alt6
- fix path to cups
- run "numlockx on" on session start

* Sun Nov 23 2008 Boris Savelev <boris@altlinux.org> 0.7.4-alt5
- fix permission on nx homedir

* Sat Nov 22 2008 Boris Savelev <boris@altlinux.org> 0.7.4-alt4
- add support nx 3.3

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

