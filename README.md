# Evolution of classic nx technology - FreeNX

All these years, the classic nx was not as dead as it seemed ;)
It is used in production and develops as fast as it can.

I am very grateful to the developers of the [ArcticaProject/nx-libs](https://github.com/ArcticaProject/nx-libs) for maintaining backward
compatibility and the opportunity to use their libraries instead
of self-assembly.

Compared to the original freenx new features added by community:

- CUPS Server mode: servers's system CUPS used directlty (witch sudo)
and remote printers can be share between users;

- NXACLS in user mode: control of starting specific applications and
their substitution for users and groups;

- Printers and shares multimount: in case multiply sessions from one
client's computer try shares leave while there is at least one running
session;

- Pulseaudio sound: tunnelled, with or without resampling;

- Localization of windows sharenames;

- Control of rootles sessions ending: based on application-process
internal customizable map;

- Reduced connection time;

- Used nxsetting sqlite db (nxsetup --reload or nxsetup --mkdb for update).
Everything got even a little faster;

- vnc and rdp over nx modes running;

- Shadow mode worked also;

- nxshadowacl script functionality moved to existing acl.


Many thanks to Djelf for long consultations on sqlite.

Thats all worked with [opennx ce](https://github.com/dimbor-ru/opennx) liux/windows client, but original nxclient
basicaly alive too (with restrictions).

Debian package home-maded for Devuan ASCII now. There is a suspicion that
under Debian Stretch everything will be fine.

On modern systems with glibc >= 2.28 to run nxclient you must apply [solution](https://github.com/dimbor-ru/freenx-server/issues/5#issuecomment-579694048)
from Djelf (on nxclient side of course).

Code from him to install nxclient 32/64:
#!/bin/sh
mkdir nxclient
cd nxclient
wget http://debian.rot13.org/binary/64.34.161.181/download/3.5.0/Linux/nxclient_3.5.0-7_amd64.deb
#wget http://debian.rot13.org/binary/64.34.161.181/download/3.5.0/Linux/nxclient_3.5.0-7_i386.deb
wget https://github.com/dimbor-ru/freenx-server/files/4128228/nxfixglibc1190.tar.gz
dpkg -i ./nxclient_3.5.0-7_amd64.deb
find /usr/NX/lib -name "libz*" -delete
tar -xvf nxfixglibc1190.tar.gz
#cp ./nxfixglibc1190/x32/nxfixglibc1190.so /usr/NX/lib/nxfixglibc1190.so
cp ./nxfixglibc1190/x64/nxfixglibc1190.so /usr/NX/lib/nxfixglibc1190.so
cp /usr/NX/bin/nxclient /usr/NX/bin/nxclient.bin
echo '#!/bin/sh' > /usr/NX/bin/nxclient
echo 'LD_PRELOAD=/usr/NX/lib/nxfixglibc1190.so /usr/NX/bin/nxclient.bin /$@' >> /usr/NX/bin/nxclient

Solution to use Arctica nx-libs:
#!/bin/sh
find /usr/NX/lib -name "libjpeg*" -delete
find /usr/NX/lib -name "libXcomp*" -delete
ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/NX/lib/libjpeg.so.62
ln -s /usr/lib/x86_64-linux-gnu/libXcomp.so.3 /usr/NX/lib/libXcomp.so

Archives of old nx stuff you can find [here](http://ftp.disconnected-by-peer.at/NX/)

dimbor. 2022
