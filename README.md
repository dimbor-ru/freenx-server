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

- Pulseaudio sound: direct, tunnelled, with or without resampling;

- Localization of windows sharenames;

- Control of rootles sessions ending: based on application-process
internal customizable map.

- ...

Thats all worked with [opennx ce](https://github.com/dimbor-ru/opennx) liux/windows client, but original nxclient
basicaly alive too (with restrictions).

Debian package home-maded for Devuan ASCII now. There is a suspicion that
under Debian Stretch everything will be fine.

dimbor. 2019.
